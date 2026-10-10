#!/usr/bin/env python3
"""
Elite Mobile-Optimized 1-Minute Physics Rendering Engine (3b1b & Feynman Style).
Designed specifically for mobile vertical screens (1080x1920) to maintain high student engagement.
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
    """60-Second Mobile-Optimized Physics Short Animation Scene."""

    def construct(self):
        video_id = os.environ.get("CURRENT_VIDEO_ID", "feynman_day2_01")
        title_str = os.environ.get("CURRENT_TITLE", "Advanced Physics Analysis")
        eq_json = os.environ.get("EQUATIONS_JSON", "[]")

        # 1. Title Banner (Mobile Optimized Top Header)
        title = Tex(title_str, color=PALETTE["ACCENT_BLUE"], font_size=42).to_edge(UP, buff=1.2)
        underline = Line(LEFT * 4.5, RIGHT * 4.5, color=PALETTE["MUTED"], stroke_width=2).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=DOWN * 0.3), Create(underline), run_time=1.0)

        # 2. Topic-Specific 60-Second Visual Timeline
        if "time_dilation" in video_id or "muon" in video_id:
            self.animate_relativistic_time_dilation()
        elif "emc2" in video_id:
            self.animate_mass_energy_equivalence()
        elif "space_time" in video_id:
            self.animate_light_cone_spacetime()
        elif "gyroscope" in video_id:
            self.animate_gyroscopic_precession()
        elif "fermat" in video_id:
            self.animate_fermat_principle()
        elif "quantum" in video_id or "two_slit" in video_id:
            self.animate_quantum_interference()
        elif "ratchet" in video_id:
            self.animate_ratchet_and_pawl()
        elif "moment_of_inertia" in video_id:
            self.animate_moment_of_inertia_rod()
        else:
            self.animate_generic_physics_visual(eq_json)

    def show_persistent_derivation(self, latex_str: str):
        eq = MathTex(latex_str, color=PALETTE["ACCENT_GOLD"], font_size=36)
        box = SurroundingRectangle(eq, color=PALETTE["ACCENT_BLUE"], buff=0.3, corner_radius=0.15, stroke_width=2)
        box.set_fill(PALETTE["PANEL_BG"], opacity=0.95)
        panel = VGroup(box, eq).to_edge(DOWN, buff=1.5)
        self.play(GrowFromCenter(panel), run_time=1.0)
        return panel

    def animate_relativistic_time_dilation(self):
        # Step 1: Stationary Clock
        mirror_top = Line(LEFT * 1.5, RIGHT * 1.5, color=PALETTE["ACCENT_BLUE"], stroke_width=6).shift(UP * 2.5)
        mirror_bot = Line(LEFT * 1.5, RIGHT * 1.5, color=PALETTE["ACCENT_BLUE"], stroke_width=6).shift(DOWN * 0.5)
        photon = Dot(mirror_bot.get_center(), color=PALETTE["ACCENT_GOLD"], radius=0.18)
        clock_label = Tex("Stationary Frame", color=PALETTE["MUTED"], font_size=28).next_to(mirror_top, UP)

        self.play(Create(mirror_top), Create(mirror_bot), FadeIn(clock_label), FadeIn(photon), run_time=1.0)
        
        # Photon bouncing simulation
        for _ in range(2):
            self.play(photon.animate.shift(UP * 3), run_time=0.8, rate_func=rate_functions.linear)
            self.play(photon.animate.shift(DOWN * 3), run_time=0.8, rate_func=rate_functions.linear)

        # Step 2: Moving Spacecraft Light Path (Diagonal Zigzag)
        self.play(FadeOut(clock_label), run_time=0.5)
        moving_label = Tex("Moving Ship Frame ($v \approx c$)", color=PALETTE["ACCENT_CORAL"], font_size=28).next_to(mirror_top, UP)
        self.play(FadeIn(moving_label), run_time=0.5)

        path_line = Line(mirror_bot.get_center(), mirror_top.get_center() + RIGHT * 2, color=PALETTE["ACCENT_CORAL"], stroke_width=3, stroke_opacity=0.7)
        self.play(Create(path_line), run_time=1.5)

        # Step 3: Equation Reveal
        self.show_persistent_derivation(r"\Delta t_{\text{obs}} = \frac{\Delta t_0}{\sqrt{1 - v^2/c^2}} = \gamma \Delta t_0")
        self.wait(10)

    def animate_mass_energy_equivalence(self):
        m_box = Square(side_length=1.4, color=PALETTE["ACCENT_CORAL"]).shift(LEFT * 2.2)
        m_lbl = MathTex("m_0", color=PALETTE["PRIMARY"], font_size=36).move_to(m_box.get_center())
        
        arrow = Arrow(LEFT * 1.2, RIGHT * 1.2, color=PALETTE["ACCENT_GOLD"], stroke_width=4)
        arrow_lbl = MathTex(r"c^2", color=PALETTE["ACCENT_GOLD"], font_size=32).next_to(arrow, UP)

        e_box = Circle(radius=0.9, color=PALETTE["ACCENT_BLUE"]).shift(RIGHT * 2.2)
        e_lbl = MathTex("E", color=PALETTE["PRIMARY"], font_size=36).move_to(e_box.get_center())

        self.play(Create(m_box), Write(m_lbl), run_time=1.0)
        self.play(GrowArrow(arrow), Write(arrow_lbl), run_time=1.0)
        self.play(Create(e_box), Write(e_lbl), run_time=1.0)

        # Pulsing energy transformation
        self.play(e_box.animate.scale(1.2), m_box.animate.scale(0.8), run_time=0.8)
        self.play(e_box.animate.scale(1.0), m_box.animate.scale(1.0), run_time=0.8)

        self.show_persistent_derivation(r"E = \sqrt{p^2 c^2 + m_0^2 c^4} \implies E_{\text{rest}} = m_0 c^2")
        self.wait(10)

    def animate_light_cone_spacetime(self):
        line1 = Line(DL * 3.5, UR * 3.5, color=PALETTE["ACCENT_GOLD"], stroke_width=3)
        line2 = Line(UL * 3.5, DR * 3.5, color=PALETTE["ACCENT_GOLD"], stroke_width=3)
        origin = Dot(ORIGIN, color=PALETTE["ACCENT_CORAL"], radius=0.15)
        lbl_o = MathTex("O", color=PALETTE["ACCENT_CORAL"], font_size=32).next_to(origin, DOWN, buff=0.2)

        future_lbl = Tex("FUTURE", color=PALETTE["PRIMARY"], font_size=28).shift(UP * 2.5)
        past_lbl = Tex("PAST", color=PALETTE["PRIMARY"], font_size=28).shift(DOWN * 2.5)

        self.play(Create(line1), Create(line2), FadeIn(origin), FadeIn(lbl_o), run_time=1.2)
        self.play(FadeIn(future_lbl), FadeIn(past_lbl), run_time=0.8)

        # Expanding light wavefront rings
        ring = Circle(radius=0.2, color=PALETTE["ACCENT_BLUE"], stroke_width=2).move_to(ORIGIN)
        self.play(ring.animate.scale(8).set_opacity(0), run_time=2.0, rate_func=rate_functions.ease_out_sine)

        self.show_persistent_derivation(r"ds^2 = c^2 dt^2 - dx^2 - dy^2 - dz^2 \geq 0")
        self.wait(10)

    def animate_gyroscopic_precession(self):
        wheel = Circle(radius=1.5, color=PALETTE["ACCENT_BLUE"], stroke_width=5).shift(UP * 0.5)
        axis = Line(LEFT * 2.5, RIGHT * 2.5, color=PALETTE["ACCENT_GOLD"], stroke_width=4).shift(UP * 0.5)
        l_vec = Arrow(ORIGIN, UP * 2.5, color=PALETTE["ACCENT_GREEN"], stroke_width=5, buff=0)

        self.play(Create(wheel), Create(axis), GrowArrow(l_vec), run_time=1.2)
        
        # Precession rotation loop
        for _ in range(3):
            self.play(Rotate(l_vec, angle=2 * PI, about_point=ORIGIN, axis=OUT), run_time=1.5, rate_func=rate_functions.linear)

        self.show_persistent_derivation(r"\vec{\tau} = \frac{d\vec{L}}{dt} = \vec{\Omega} \times \vec{L}")
        self.wait(10)

    def animate_fermat_principle(self):
        interface = Line(LEFT * 5, RIGHT * 5, color=PALETTE["MUTED"], stroke_width=2)
        air_lbl = Tex("AIR ($n_1$)", color=PALETTE["ACCENT_BLUE"], font_size=26).to_edge(LEFT).shift(UP * 1.5)
        water_lbl = Tex("WATER ($n_2$)", color=PALETTE["ACCENT_GOLD"], font_size=26).to_edge(LEFT).shift(DOWN * 1.5)

        ray_in = Arrow(UP * 2.5 + LEFT * 2, ORIGIN, color=PALETTE["ACCENT_GOLD"], stroke_width=4, buff=0)
        ray_ref = Arrow(ORIGIN, DOWN * 2.5 + RIGHT * 1.5, color=PALETTE["ACCENT_GREEN"], stroke_width=4, buff=0)

        self.play(Create(interface), FadeIn(air_lbl), FadeIn(water_lbl), run_time=1.0)
        self.play(GrowArrow(ray_in), GrowArrow(ray_ref), run_time=1.2)

        self.show_persistent_derivation(r"\delta \int n \, ds = 0 \implies n_1 \sin\theta_1 = n_2 \sin\theta_2")
        self.wait(10)

    def animate_quantum_interference(self):
        wall = Line(UP * 2.5, DOWN * 2.5, color=PALETTE["ACCENT_BLUE"], stroke_width=6).shift(LEFT * 1.5)
        screen = Line(UP * 3, DOWN * 3, color=PALETTE["ACCENT_GREEN"], stroke_width=4).shift(RIGHT * 3)
        wave = ParametricFunction(lambda t: np.array([t - 2.5, np.sin(t * 6) * 0.5, 0]), t_range=[0, 2.5], color=PALETTE["ACCENT_GOLD"], stroke_width=3)

        self.play(Create(wall), Create(screen), Create(wave), run_time=1.2)

        # Highlight interference dots on screen
        dots = VGroup(*[Dot(RIGHT * 3 + UP * y, color=PALETTE["ACCENT_CORAL"], radius=0.08) for y in np.linspace(-2, 2, 7)])
        self.play(FadeIn(dots, lag_ratio=0.2), run_time=1.5)

        self.show_persistent_derivation(r"P_{12} = |\psi_1 + \psi_2|^2 = P_1 + P_2 + 2\sqrt{P_1 P_2}\cos(\delta)")
        self.wait(10)

    def animate_ratchet_and_pawl(self):
        gear = Circle(radius=1.8, color=PALETTE["ACCENT_BLUE"], stroke_width=5)
        pawl = Arrow(UP * 2.5, UP * 1.2, color=PALETTE["ACCENT_CORAL"], stroke_width=5, buff=0)
        
        self.play(Create(gear), GrowArrow(pawl), run_time=1.2)
        self.play(Rotate(gear, angle=PI/4, about_point=ORIGIN), run_time=0.8)
        self.play(Rotate(gear, angle=-PI/6, about_point=ORIGIN), run_time=0.8)

        self.show_persistent_derivation(r"\frac{\epsilon + L\theta}{T_1} = \frac{\epsilon}{T_2} \implies \text{No Perpetual Motion}")
        self.wait(10)

    def animate_moment_of_inertia_rod(self):
        rod = Line(LEFT * 3, RIGHT * 3, color=PALETTE["ACCENT_BLUE"], stroke_width=8)
        axis = Dot(LEFT * 3, color=PALETTE["ACCENT_CORAL"], radius=0.25)
        axis_lbl = Tex("Pivot Axis", color=PALETTE["ACCENT_CORAL"], font_size=26).next_to(axis, DOWN)

        self.play(Create(rod), FadeIn(axis), FadeIn(axis_lbl), run_time=1.0)
        self.play(Rotate(rod, angle=2 * PI, about_point=LEFT * 3), run_time=2.0, rate_func=rate_functions.linear)

        self.show_persistent_derivation(r"I = \int_{-L/2}^{L/2} x^2 dm = \frac{ML^2}{3}")
        self.wait(10)

    def animate_generic_physics_visual(self, eq_json_str: str):
        try:
            equations = json.loads(eq_json_str)
            eq_text = equations[0] if equations else r"E = mc^2"
        except Exception:
            eq_text = r"E = mc^2"
        self.show_persistent_derivation(eq_text)
        self.wait(10)
