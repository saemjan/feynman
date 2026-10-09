#!/usr/bin/env python3
"""
Master 3Blue1Brown-style 9:16 Vertical Rendering Engine using Manim.
Renders physics scenes, LaTeX math, and title cards inside vertical canvas safe zones.
"""

import argparse
import json
import os
import re
import sys
from manim import *

# 9:16 Vertical Canvas Configuration
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0
config.frame_rate = 30
config.background_color = "#0B0C10"

# 3Blue1Brown Color Palette
COLOR_MAP = {
    "FIELD": "#3498DB",      # Electric/Magnetic fields
    "POSITIVE": "#FF4B4B",   # Positive charges / High energy
    "NEGATIVE": "#00D2FF",   # Negative charges / Velocity vectors
    "ACCENT": "#F1C40F",     # Highlights / Geometry guides
    "SUCCESS": "#2ECC71",    # Force vectors / Correct answers
    "WHITE": "#FFFFFF"
}


def safe_json_loads(val_str: str):
    """Sanitizes raw strings containing single-backslashed LaTeX for JSON parsing."""
    if not val_str or val_str.strip() == '""':
        return []
    cleaned = re.sub(r'(?<!\\)\\(?![\\"/bfnrtu])', r"\\\\", val_str)
    return json.loads(cleaned)


def to_3d_point(pos):
    """Ensures coordinates are formatted as a 3D float list [x, y, z]."""
    if len(pos) == 2:
        return [float(pos[0]), float(pos[1]), 0.0]
    return [float(pos[0]), float(pos[1]), float(pos[2])]


class UniversalPhysicsScene(Scene):
    def __init__(self, scene_kwargs=None, **kwargs):
        super().__init__(**kwargs)
        self.scene_kwargs = scene_kwargs or {}

    def construct(self):
        sk = self.scene_kwargs
        header_title = sk.get("header_title", "")
        tagline = sk.get("tagline", "")
        question_text = sk.get("question_text", "")
        options = sk.get("options", [])
        correct_answer = sk.get("correct_answer", "")
        equations = safe_json_loads(sk.get("equations_json", "[]"))
        visual_data = safe_json_loads(sk.get("visual_data_json", "[]"))
        target_duration = float(sk.get("duration", 15.0))

        # --- ZONE 1: Header Title & Tagline (Y: 6.0 to 7.2) ---
        header_group = VGroup()
        if header_title:
            title_mob = Text(header_title, font="sans-serif", weight=BOLD, font_size=32, color=WHITE)
            header_group.add(title_mob)
        if tagline:
            tag_mob = Text(tagline, font="sans-serif", font_size=22, color=COLOR_MAP["ACCENT"])
            header_group.add(tag_mob)
        header_group.arrange(DOWN, buff=0.15).move_to([0, 6.6, 0])
        self.add(header_group)

        # --- ZONE 2: Question (For PYQ Mode, Y: 4.2 to 5.6) ---
        if question_text:
            q_mob = Paragraph(*[question_text[i:i+40] for i in range(0, len(question_text), 40)],
                              font_size=20, line_spacing=0.2, color=WHITE)
            q_mob.move_to([0, 4.8, 0])
            self.add(q_mob)

        # --- ZONE 3: Visual Scene Container (Y: -1.5 to 3.2) ---
        visual_mobjects = VGroup()
        for item in visual_data:
            mob = self.build_visual_primitive(item)
            if mob:
                visual_mobjects.add(mob)

        if len(visual_mobjects) > 0:
            visual_mobjects.move_to([0, 0.8, 0])

        # --- ZONE 4: Equations / Options Card with 3b1b Background (Y: -7.0 to -2.5) ---
        card_contents = VGroup()
        if equations:
            eq_vgroup = VGroup()
            for eq_str in equations:
                try:
                    eq_tex = MathTex(eq_str, font_size=28, color=WHITE)
                    eq_vgroup.add(eq_tex)
                except Exception:
                    eq_tex = Text(eq_str, font_size=22, color=WHITE)
                    eq_vgroup.add(eq_tex)
            eq_vgroup.arrange(DOWN, buff=0.25)
            card_contents.add(eq_vgroup)

        if options and any(options):
            opts_vgroup = VGroup()
            for opt in options:
                if opt.strip():
                    opts_vgroup.add(Text(opt, font_size=20, color=WHITE))
            opts_vgroup.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            card_contents.add(opts_vgroup)

        if correct_answer:
            ans_mob = Text(correct_answer, font_size=22, weight=BOLD, color=COLOR_MAP["SUCCESS"])
            card_contents.add(ans_mob)

        card_group = VGroup()
        if len(card_contents) > 0:
            card_contents.arrange(DOWN, buff=0.35)
            bg_rect = RoundedRectangle(
                corner_radius=0.2,
                width=max(7.5, card_contents.width + 0.8),
                height=card_contents.height + 0.6,
                color="#1F2937",
                fill_color="#111827",
                fill_opacity=0.85,
                stroke_width=2
            )
            card_group.add(bg_rect, card_contents)
            card_group.move_to([0, -4.8, 0])

        # --- ANIMATION TIMELINE ---
        if len(visual_mobjects) > 0:
            self.play(Create(visual_mobjects), run_time=1.8)
        
        if len(card_group) > 0:
            self.play(FadeIn(card_group, shift=UP), run_time=1.2)

        elapsed = self.renderer.time
        remaining = max(1.0, target_duration - elapsed)
        self.wait(remaining)

    def build_visual_primitive(self, item: dict) -> Mobject:
        """Translates declarative JSON primitives into 3b1b Manim mobjects."""
        itype = item.get("type", "").lower()
        color_hex = item.get("color", COLOR_MAP.get(item.get("semantic", "").upper(), COLOR_MAP["FIELD"]))

        if itype == "field":
            direction = item.get("direction", "RIGHT")
            vector_field = VGroup()
            dir_vec = RIGHT if direction == "RIGHT" else LEFT if direction == "LEFT" else UP if direction == "UP" else DOWN
            for y in np.linspace(-1.5, 1.5, item.get("rows", 5)):
                for x in np.linspace(-2.5, 2.5, 5):
                    arrow = Arrow(start=[x, y, 0], end=[x + dir_vec[0]*0.6, y + dir_vec[1]*0.6, 0],
                                  buff=0, color=color_hex, max_tip_length_to_length_ratio=0.3, stroke_width=2)
                    arrow.set_opacity(item.get("opacity", 0.4))
                    vector_field.add(arrow)
            return vector_field

        elif itype == "charge":
            pos = to_3d_point(item.get("pos", [0, 0, 0]))
            radius = item.get("radius", 0.25)
            dot = Dot(point=pos, radius=radius, color=color_hex)
            # 3b1b Radial Glow Effect
            halo = Circle(radius=radius * 1.8, color=color_hex, fill_opacity=0.25, stroke_width=0)
            halo.move_to(pos)
            charge_grp = VGroup(halo, dot)
            if "label" in item:
                lbl = MathTex(item["label"], font_size=22, color=WHITE).next_to(dot, UP, buff=0.15)
                charge_grp.add(lbl)
            return charge_grp

        elif itype == "vector":
            start = to_3d_point(item.get("start", [0, 0, 0]))
            end = to_3d_point(item.get("end", [1, 0, 0]))
            arrow = Arrow(start=start, end=end, buff=0, color=color_hex, stroke_width=4)
            if "label" in item:
                lbl = MathTex(item["label"], font_size=22, color=color_hex).next_to(arrow.get_end(), RIGHT, buff=0.1)
                return VGroup(arrow, lbl)
            return arrow

        elif itype == "line":
            start = to_3d_point(item.get("start", [-1, 0, 0]))
            end = to_3d_point(item.get("end", [1, 0, 0]))
            if item.get("dashed", False):
                return DashedLine(start=start, end=end, color=color_hex)
            return Line(start=start, end=end, color=color_hex, stroke_width=3)

        elif itype == "arc":
            center = to_3d_point(item.get("center", [0, 0, 0]))
            arc = Arc(radius=item.get("radius", 0.8), start_angle=np.radians(item.get("start_angle", 0)),
                      angle=np.radians(item.get("angle", 60)), color=color_hex, arc_center=center)
            if "label" in item:
                lbl = MathTex(item["label"], font_size=20, color=color_hex).next_to(arc, RIGHT, buff=0.1)
                return VGroup(arc, lbl)
            return arc

        elif itype == "graph":
            try:
                axes = Axes(x_range=item.get("x_range", [0, 5]), y_range=item.get("y_range", [-2, 2]),
                            x_length=4, y_length=2.5, axis_config={"color": GRAY, "stroke_width": 2})
                expr = item.get("expression", "x")
                graph = axes.plot(lambda x: eval(expr, {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp}), color=color_hex)
                return VGroup(axes, graph)
            except Exception as e:
                print(f"[WARN] Failed to compile graph expression: {e}", file=sys.stderr)
                return None

        elif itype == "shape":
            kind = item.get("kind", "rectangle")
            pos = to_3d_point(item.get("pos", [0, 0, 0]))
            dims = item.get("dims", [2.0, 1.0])
            if kind == "rectangle":
                rect = Rectangle(width=dims[0], height=dims[1], color=color_hex, fill_opacity=item.get("fill_opacity", 0.2))
                rect.move_to(pos)
                return rect
            elif kind == "ellipse":
                ell = Ellipse(width=item.get("width", 3.0), height=item.get("height", 1.8), color=color_hex)
                ell.move_to(pos)
                return ell

        return None


def main():
    parser = argparse.ArgumentParser(description="Manim Universal Render Engine")
    parser.add_argument("--video_id", required=True)
    parser.add_argument("--header_title", default="")
    parser.add_argument("--tagline", default="")
    parser.add_argument("--question_text", default="")
    parser.add_argument("--options_json", default="[]")
    parser.add_argument("--correct_answer", default="")
    parser.add_argument("--equations_json", default="[]")
    parser.add_argument("--visual_data_json", default="[]")
    parser.add_argument("--duration", type=float, default=15.0)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    options = safe_json_loads(args.options_json)

    scene_kwargs = {
        "header_title": args.header_title,
        "tagline": args.tagline,
        "question_text": args.question_text,
        "options": options,
        "correct_answer": args.correct_answer,
        "equations_json": args.equations_json,
        "visual_data_json": args.visual_data_json,
        "duration": args.duration
    }

    scene = UniversalPhysicsScene(scene_kwargs=scene_kwargs)
    scene.render()

    rendered_file = config.get_dir("video_output_dir") / f"UniversalPhysicsScene.mp4"
    if os.path.exists(rendered_file):
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        os.replace(rendered_file, args.output)
        print(f"[SUCCESS] Rendered video saved to: {args.output}")
    else:
        print(f"[ERROR] Could not locate rendered output at {rendered_file}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
