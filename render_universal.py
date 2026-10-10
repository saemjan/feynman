#!/usr/init/env python3
"""
Elite Mobile-Optimized 1-Minute Physics Rendering Engine (3b1b & Feynman Style).
Fully paced for 60-second audio scripts with full vertical screen utilization (1080x1920).
"""

import os
import json
import numpy as np
from manim import *

PALETTE = {
    "BG": "#0a0a0c",
    "PRIMARY": "#ECE6E2",
    "ACCENT_BLUE": "#38bdf8",
    "ACCENT_GOLD": "#fbbf24",
    "ACCENT_CORAL": "#f87171",
    "ACCENT_GREEN": "#4ade80",
    "MUTED": "#64748b",
    "PANEL_BG": "#1e1e24"
}

config.background_color = PALETTE["BG"]
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30


class ElitePhysicsScene(MovingCameraScene):
    """60-Second Mobile-Optimized Physics Short Animation Scene with Full Vertical Layout & Pacing."""

    def construct(self):
        video_id = os.environ.get("CURRENT_VIDEO_ID", "feynman_day2_01")
        title_str = os.environ.get("CURRENT_TITLE", "Advanced Physics Analysis")
        eq_json = os.environ.get("EQUATIONS_JSON", "[]")

        # 1. TOP HEADER ZONE (Spaced at UP * 3.5)
        title = Tex(title_str, color=PALETTE["ACCENT_BLUE"], font_size=42).to_edge(UP, buff=1.2)
        underline = Line(LEFT * 4.5, RIGHT * 4.5, color=PALETTE["MUTED"], stroke_width=2).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=DOWN * 0.3), Create(underline), run_time=1.0)

        # 2. CENTER SIMULATION & BOTTOM PANEL (Dispatched per topic with continuous pacing)
        if "time_dilation" in video_id or "muon" in video_id:
            self.render_space_time_dilation_layout()
        elif "emc2" in video_id:
            self.render_mass_energy_layout()
        elif "space_time" in video_id:
            self.render_light_cone_layout()
        elif "gyroscope" in video_id:
            self.render_gyroscopic_layout()
        elif "fermat" in video_id:
            self.render_fermat_layout()
        elif "quantum" in video_id or "two_slit" in video_id:
            self.render_quantum_layout()
        elif "ratchet" in video_id:
            self.render_ratchet_layout()
        elif "moment_of_inertia" in video_id:
            self.render_moment_of_inertia_layout()
        else:
            self.render_generic_layout(eq_json)

    def show_bottom_derivation_panel(self, latex_str: str):
        """Anchors the main JEE formula in the bottom safe-zone panel with generous padding."""
        eq = MathTex(latex_str, color=PALETTE["ACCENT_GOLD"], font_size=36)
        box = SurroundingRectangle(eq, color=PALETTE["ACCENT_BLUE"], buff=0.4, corner_radius=0.2, stroke_width=2.5)
        box.set_fill(PALETTE["PANEL_BG"], opacity=0.95)
        panel = VGroup(box, eq).to_edge(DOWN, buff=1.5)
        self.play(GrowFromCenter(panel), run_time=1.2)
        return panel

    def render_space_time_dilation_layout(self):
        mirror_top = Line(LEFT * 2.5, RIGHT * 2.5, color=PALETTE["ACCENT_BLUE"], stroke_width=6).shift(UP * 2.5)
        mirror_bot = Line(LEFT * 2.5, RIGHT * 2.5, color=PALETTE["ACCENT_BLUE"], stroke_width=6].shift(DOWN * 2.0)
        photon = Dot(mirror_bot.get_center(), color=PALETTE["ACCENT_GOLD"], radius=0.22)
        
        clock_group = VGroup(mirror_top, mirror_bot, photon)
        self.play(Create(clock_group), run_time=1.2)

        # Spread out photon bouncing across the explanation timeline
        for _ in range(4):
            self.play(photon.animate.shift(UP * 4.5), run_time=1.5, rate_func=rate_functions.linear)
            self.play(photon.animate.shift(DOWN * 4.5), run_time=1.5, rate_func=rate_functions.linear)

        path_line = Line(mirror_bot.get_center(), mirror_top.get_center() + RIGHT * 3.5, color=PALETTE["ACCENT_CORAL"], stroke_width=3, stroke_opacity=0.8)
        self.play(Create(path_line), run_time=2.0)

        self.show_bottom_derivation_panel(r"\Delta t_{\text{obs}} = \frac{\Delta t_0}{\sqrt{1 - v^2/c^2}} = \gamma \Delta t_0")
        self.wait(15)

    def render_mass_energy_layout(self):
        m_box = Square(side_length=1.8, color=PALETTE["ACCENT_CORAL"]).shift(UP * 0.5 + LEFT * 2.5)
        m_lbl = MathTex("m_0", color=PALETTE["PRIMARY"], font_size=44).move_to(m_box.get_center())
        
        arrow = Arrow(LEFT * 1.3, RIGHT * 1.3, color=PALETTE["ACCENT_GOLD"], stroke_width=5).shift(UP * 0.5)
        arrow_lbl = MathTex("c^2", color=PALETTE["ACCENT_GOLD"], font_size=40).next_to(arrow, UP, buff=0.3)

        e_box = Circle(radius=1.1, color=PALETTE["ACCENT_BLUE"]).shift(UP * 0.5 + RIGHT * 2.5)
        e_lbl = MathTex("E", color=PALETTE["PRIMARY"], font_size=44).move_to(e_box.get_center())

        self.play(Create(m_box), Write(m_lbl), run_time=1.2)
        self.play(GrowArrow(arrow), Write(arrow_lbl), run_time=1.5)
        self.play(Create(e_box), Write(e_lbl), run_time=1.2)

        # Continuous gentle pulsing to keep visual engagement high
        for _ in range(3):
            self.play(e_box.animate.scale(1.15), m_box.animate.scale(0.85), run_time=1.0)
            self.play(e_box.animate.scale(1.0), m_box.animate.scale(1.0), run_time=1.0)

        self.show_bottom_derivation_panel(r"E = \sqrt{p^2 c^2 + m_0^2 c^4}, \quad E_{\text{rest}} = m_0 c^2")
        self.wait(15)

    def render_light_cone_layout(self):
        line1 = Line(DL * 4.5 + UP * 0.5, UR * 4.5 + UP * 0.5, color=PALETTE["ACCENT_GOLD"], stroke_width=3.5)
        line2 = Line(UL * 4.5 + UP * 0.5, DR * 4.5 + UP * 0.5, color=PALETTE["ACCENT_GOLD"], stroke_width=3.5)
        origin = Dot(UP * 0.5, color=PALETTE["ACCENT_CORAL"], radius=0.2)
        lbl_o = MathTex("O", color=PALETTE["ACCENT_CORAL"], font_size=38).next_to(origin, DOWN, buff=0.2)

        self.play(Create(line1), Create(line2), FadeIn(origin), FadeIn(lbl_o), run_time=1.5)
        
        # Expanding light wavefront rings spaced out
        for _ in range(3):
            ring = Circle(radius=0.2, color=PALETTE["ACCENT_BLUE"], stroke_width=2.5).move_to(UP * 0.5)
            self.play(ring.animate.scale(8).set_opacity(0), run_time=2.5, rate_func=rate_functions.ease_out_sine)

        self.show_bottom_derivation_panel(r"ds^2 = c^2 dt^2 - dx^2 - dy^2 - dz^2 \geq 0")
        self.wait(15)

    def render_gyroscopic_layout(self):
        wheel = Circle(radius=2.0, color=PALETTE["ACCENT_BLUE"], stroke_width=6).shift(UP * 0.5)
        axis = Line(LEFT * 3.5, RIGHT * 3.5, color=PALETTE["ACCENT_GOLD"], stroke_width=4.5).shift(UP * 0.5)
        l_vec = Arrow(UP * 0.5, UP * 3.5, color=PALETTE["ACCENT_GREEN"], stroke_width=6, buff=0)

        self.play(Create(wheel), Create(axis), GrowArrow(l_vec), run_time=1.5)
        
        # Continuous slow precession loop matching audio explanation
        for _ in range(4):
            self.play(Rotate(l_vec, angle=2 * PI, about_point=UP * 0.5, axis=OUT), run_time=2.0, rate_func=rate_functions.linear)

        self.show_bottom_derivation_panel(r"\vec{\tau} = \frac{d\vec{L}}{dt} = \vec{\Omega} \times \vec{L}")
        self.wait(15)

    def render_fermat_layout(self):
        interface = Line(LEFT * 5, RIGHT * 5, color=PALETTE["MUTED"], stroke_width=2.5).shift(UP * 0.5)
        ray_in = Arrow(UP * 4.0 + LEFT * 2.5, UP * 0.5, color=PALETTE["ACCENT_GOLD"], stroke_width=5, buff=0)
        ray_ref = Arrow(UP * 0.5, DOWN * 2.0 + RIGHT * 2, color=PALETTE["ACCENT_GREEN"], stroke_width=5, buff=0)

        self.play(Create(interface), GrowArrow(ray_in), GrowArrow(ray_ref), run_time=1.5)
        self.show_bottom_derivation_panel(r"\delta \int n \, ds = 0 \implies n_1 \sin\theta_1 = n_2 \sin\theta_2")
        self.wait(15)

    def render_quantum_layout(self):
        wall = Line(UP * 3.5, DOWN * 1.5, color=PALETTE["ACCENT_BLUE"], stroke_width=6).shift(LEFT * 2.5)
        screen = Line(UP * 4.0, DOWN * 2.0, color=PALETTE["ACCENT_GREEN"], stroke_width=4).shift(RIGHT * 3.5)
        wave = ParametricFunction(lambda t: np.array([t - 3.0, np.sin(t * 6) * 0.7 + 0.5, 0]), t_range=[0, 3.0], color=PALETTE["ACCENT_GOLD"], stroke_width=3.5)

        self.play(Create(wall), Create(screen), Create(wave), run_time=1.5)

        dots = VGroup(*[Dot(RIGHT * 3.5 + UP * y, color=PALETTE["ACCENT_CORAL"], radius=0.09) for y in np.linspace(-1.5, 3.5, 9)])
        self.play(FadeIn(dots, lag_ratio=0.15), run_time=2.0)

        self.show_bottom_derivation_panel(r"P_{12} = |\psi_1 + \psi_2|^2 = P_1 + P_2 + 2\sqrt{P_1 P_2}\cos(\delta)")
        self.wait(15)

    def render_ratchet_layout(self):
        gear = Circle(radius=2.2, color=PALETTE["ACCENT_BLUE"], stroke_width=6).shift(UP * 0.5)
        pawl = Arrow(UP * 4.0, UP * 2.7, color=PALETTE["ACCENT_CORAL"], stroke_width=6, buff=0)
        
        self.play(Create(gear), GrowArrow(pawl), run_time=1.5)
        for _ in range(3):
            self.play(Rotate(gear, angle=PI/3, about_point=UP * 0.5), run_time=1.0)
            self.play(Rotate(gear, angle=-PI/4, about_point=UP * 0.5), run_time=1.0)

        self.show_bottom_derivation_panel(r"\frac{\epsilon + L\theta}{T_1} = \frac{\epsilon}{T_2} \implies \text{No Perpetual Motion}")
        self.wait(15)

    def render_moment_of_inertia_layout(self):
        rod = Line(LEFT * 4.0, RIGHT * 4.0, color=PALETTE["ACCENT_BLUE"], stroke_width=9).shift(UP * 0.5)
        axis = Dot(LEFT * 4.0 + UP * 0.5, color=PALETTE["ACCENT_CORAL"], radius=0.28)
        axis_lbl = Tex("Pivot Axis", color=PALETTE["ACCENT_CORAL"], font_size=28).next_to(axis, DOWN, buff=0.25)

        self.play(Create(rod), FadeIn(axis), FadeIn(axis_lbl), run_time=1.2)
        for _ in range(3):
            self.play(Rotate(rod, angle=2 * PI, about_point=LEFT * 4.0 + UP * 0.5), run_time=2.0, rate_func=rate_functions.linear)

        self.show_bottom_derivation_panel(r"I = \int_{-L/2}^{L/2} x^2 dm = \frac{ML^2}{3}")
        self.wait(15)

    def render_generic_layout(self, eq_json_str: str):
        try:
            equations = json.loads(eq_json_str)
            eq_text = equations[0] if equations else r"E = mc^2"
        except Exception:
            eq_text = r"E = mc^2"
        self.show_bottom_derivation_panel(eq_text)
        self.wait(15)
