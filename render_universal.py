#!/usr/bin/env python3
"""
Elite JEE Advanced & 3b1b-Grade Physics Rendering Engine.
Dynamic vector graphics, calculus curves, and rigorous mathematical derivations.
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
    """Rigorous JEE Advanced physics animation scene."""

    def construct(self):
        video_id = os.environ.get("CURRENT_VIDEO_ID", "feynman_day2_01")
        title_str = os.environ.get("CURRENT_TITLE", "Advanced Physics Analysis")
        eq_json = os.environ.get("EQUATIONS_JSON", "[]")

        # Create academic header
        title = Tex(title_str, color=PALETTE["ACCENT_BLUE"], font_size=38).to_edge(UP, buff=0.8)
        underline = Line(LEFT * 4.5, RIGHT * 4.5, color=PALETTE["MUTED"], stroke_width=1).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(VGroup(title, underline), shift=DOWN * 0.2), run_time=0.8)

        # Dynamic Visual Dispatch based on Video ID
        if "time_dilation" in video_id or "muon" in video_id:
            self.render_relativistic_time_dilation()
        elif "emc2" in video_id:
            self.render_mass_energy_equivalence()
        elif "space_time" in video_id:
            self.render_light_cone_spacetime()
        elif "gyroscope" in video_id:
            self.render_gyroscopic_precession()
        elif "fermat" in video_id:
            self.render_fermat_principle()
        elif "quantum" in video_id or "two_slit" in video_id:
            self.render_quantum_interference()
        elif "ratchet" in video_id:
            self.render_ratchet_and_pawl()
        elif "moment_of_inertia" in video_id:
            self.render_moment_of_inertia_rod()
        else:
            self.render_generic_physics_visual(eq_json)

    def display_derivation_box(self, latex_str: str):
        eq = MathTex(latex_str, color=PALETTE["ACCENT_GOLD"], font_size=30)
        box = SurroundingRectangle(eq, color=PALETTE["ACCENT_BLUE"], buff=0.25, corner_radius=0.1, stroke_width=1.5)
        box.set_fill(PALETTE["PANEL_BG"], opacity=0.9)
        panel = VGroup(box, eq).to_edge(DOWN, buff=0.8)
        self.play(GrowFromCenter(panel), run_time=0.8)
        return panel

    def render_relativistic_time_dilation(self):
        # Light clock diagram
        mirror_top = Line(LEFT * 1, RIGHT * 1, color=PALETTE["ACCENT_BLUE"], stroke_width=4).shift(UP * 2)
        mirror_bot = Line(LEFT * 1, RIGHT * 1, color=PALETTE["ACCENT_BLUE"], stroke_width=4).shift(DOWN * 1)
        photon = Dot(mirror_bot.get_center(), color=PALETTE["ACCENT_GOLD"], radius=0.12)
        
        clock = VGroup(mirror_top, mirror_bot, photon)
        self.play(Create(clock), run_time=1.0)
        
        self.play(
            photon.animate.shift(UP * 3),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.display_derivation_box(r"\Delta t_{\text{obs}} = \frac{\Delta t_0}{\sqrt{1 - v^2/c^2}} = \gamma \Delta t_0")
        self.wait(2)

    def render_mass_energy_equivalence(self):
        m_box = Square(side_length=1.0, color=PALETTE["ACCENT_CORAL"]).shift(LEFT * 2)
        m_lbl = MathTex("m_0", color=PALETTE["PRIMARY"]).move_to(m_box.get_center())
        arrow = Arrow(LEFT * 1, RIGHT * 1, color=PALETTE["ACCENT_GOLD"])
        e_box = Circle(radius=0.6, color=PALETTE["ACCENT_BLUE"]).shift(RIGHT * 2)
        e_lbl = MathTex("E", color=PALETTE["PRIMARY"]).move_to(e_box.get_center())

        self.play(Create(VGroup(m_box, m_lbl)), Create(arrow), Create(VGroup(e_box, e_lbl)), run_time=1.2)
        self.display_derivation_box(r"E = \sqrt{p^2 c^2 + m_0^2 c^4}, \quad E_{\text{rest}} = m_0 c^2")
        self.wait(2)

    def render_light_cone_spacetime(self):
        line1 = Line(DL * 3, UR * 3, color=PALETTE["ACCENT_GOLD"])
        line2 = Line(UL * 3, DR * 3, color=PALETTE["ACCENT_GOLD"])
        origin = Dot(ORIGIN, color=PALETTE["ACCENT_CORAL"])
        lbl = MathTex("O", color=PALETTE["ACCENT_CORAL"]).next_to(origin, DOWN)

        self.play(Create(line1), Create(line2), FadeIn(origin), FadeIn(lbl), run_time=1.2)
        self.display_derivation_box(r"ds^2 = c^2 dt^2 - dx^2 - dy^2 - dz^2 \geq 0")
        self.wait(2)

    def render_gyroscopic_precession(self):
        wheel = Circle(radius=1.2, color=PALETTE["ACCENT_BLUE"], stroke_width=4).shift(UP * 0.5)
        axis = Line(LEFT * 2, RIGHT * 2, color=PALETTE["ACCENT_GOLD"], stroke_width=3).shift(UP * 0.5)
        l_vec = Arrow(ORIGIN, UP * 2, color=PALETTE["ACCENT_GREEN"], buff=0)

        self.play(Create(wheel), Create(axis), Create(l_vec), run_time=1.2)
        self.play(Rotate(l_vec, angle=0.8, about_point=ORIGIN), run_time=2.0)
        self.display_derivation_box(r"\vec{\tau} = \frac{d\vec{L}}{dt} = \vec{\Omega} \times \vec{L}")
        self.wait(2)

    def render_fermat_principle(self):
        interface = Line(LEFT * 5, RIGHT * 5, color=PALETTE["MUTED"])
        ray1 = Arrow(UP * 2 + LEFT * 2, ORIGIN, color=PALETTE["ACCENT_GOLD"], buff=0)
        ray2 = Arrow(ORIGIN, DOWN * 2 + RIGHT * 2, color=PALETTE["ACCENT_GOLD"], buff=0)

        self.play(Create(interface), Create(ray1), Create(ray2), run_time=1.2)
        self.display_derivation_box(r"\delta \int_{A}^{B} n \, ds = 0 \implies n_1 \sin\theta_1 = n_2 \sin\theta_2")
        self.wait(2)

    def render_quantum_interference(self):
        wall = Line(UP * 2, DOWN * 2, color=PALETTE["ACCENT_BLUE"]).shift(LEFT * 1)
        screen = Line(UP * 2.5, DOWN * 2.5, color=PALETTE["ACCENT_GREEN"]).shift(RIGHT * 3)
        wave = ParametricFunction(lambda t: np.array([t - 3, np.sin(t * 5) * 0.4, 0]), t_range=[0, 3], color=PALETTE["ACCENT_GOLD"])

        self.play(Create(wall), Create(screen), Create(wave), run_time=1.2)
        self.display_derivation_box(r"P_{12} = |\psi_1 + \psi_2|^2 = P_1 + P_2 + 2\sqrt{P_1 P_2}\cos(\delta)")
        self.wait(2)

    def render_ratchet_and_pawl(self):
        gear = Circle(radius=1.5, color=PALETTE["ACCENT_BLUE"], stroke_width=4)
        pawl = Arrow(UP * 2, UP * 0.8, color=PALETTE["ACCENT_CORAL"], buff=0)
        self.play(Create(gear), Create(pawl), run_time=1.2)
        self.display_derivation_box(r"\frac{\epsilon + L\theta}{T_1} = \frac{\epsilon}{T_2} \implies \text{No Perpetual Motion}")
        self.wait(2)

    def render_moment_of_inertia_rod(self):
        rod = Line(LEFT * 2.5, RIGHT * 2.5, color=PALETTE["ACCENT_BLUE"], stroke_width=6)
        axis = Dot(LEFT * 2.5, color=PALETTE["ACCENT_CORAL"], radius=0.2)
        self.play(Create(rod), FadeIn(axis), run_time=1.0)
        self.display_derivation_box(r"I = \int_{-L/2}^{L/2} x^2 dm = \frac{ML^2}{3}")
        self.wait(2)

    def render_generic_physics_visual(self, eq_json_str: str):
        try:
            equations = json.loads(eq_json_str)
            eq_text = equations[0] if equations else r"E = mc^2"
        except Exception:
            eq_text = r"E = mc^2"
        self.display_derivation_box(eq_text)
        self.wait(2)
