#!/usr/init/env python3
"""
Elite Mobile-Optimized 1-Minute Physics Rendering Engine (3b1b & Feynman Style).
Fully mapped for the new Feynman Batch 1 topics, vertical mobile layout (1080x1920).
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
        video_id = os.environ.get("CURRENT_VIDEO_ID", "feynman_batch1_01")
        title_str = os.environ.get("CURRENT_TITLE", "Advanced Physics Analysis")
        eq_json = os.environ.get("EQUATIONS_JSON", "[]")

        # 1. TOP HEADER ZONE
        title = Tex(title_str, color=PALETTE["ACCENT_BLUE"], font_size=38).to_edge(UP, buff=1.2)
        underline = Line(LEFT * 4.5, RIGHT * 4.5, color=PALETTE["MUTED"], stroke_width=2).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=DOWN * 0.3), Create(underline), run_time=1.0)

        # 2. CENTER SIMULATION & BOTTOM PANEL (Dispatched per topic)
        if "conservation_energy" in video_id:
            self.render_conservation_energy_layout()
        elif "gravitational_force" in video_id:
            self.render_gravitational_force_layout()
        elif "kinetic_theory" in video_id:
            self.render_kinetic_theory_layout()
        elif "harmonic_oscillator" in video_id:
            self.render_harmonic_oscillator_layout()
        elif "gravitational_potential" in video_id:
            self.render_gravitational_potential_layout()
        elif "escape_velocity" in video_id:
            self.render_escape_velocity_layout()
        elif "simple_pendulum" in video_id:
            self.render_simple_pendulum_layout()
        elif "rms_speed" in video_id:
            self.render_rms_speed_layout()
        elif "relativistic_momentum" in video_id:
            self.render_relativistic_momentum_layout()
        elif "moment_inertia_disk" in video_id:
            self.render_moment_inertia_disk_layout()
        else:
            self.render_generic_layout(eq_json)

    def show_bottom_derivation_panel(self, latex_str: str):
        """Anchors the main JEE formula in the bottom safe-zone panel."""
        eq = MathTex(latex_str, color=PALETTE["ACCENT_GOLD"], font_size=34)
        box = SurroundingRectangle(eq, color=PALETTE["ACCENT_BLUE"], buff=0.4, corner_radius=0.2, stroke_width=2.5)
        box.set_fill(PALETTE["PANEL_BG"], opacity=0.95)
        panel = VGroup(box, eq).to_edge(DOWN, buff=1.5)
        self.play(GrowFromCenter(panel), run_time=1.2)
        return panel

    def render_conservation_energy_layout(self):
        u_box = Square(side_length=1.4, color=PALETTE["ACCENT_BLUE"]).shift(UP * 1.5 + LEFT * 2)
        u_lbl = MathTex("U", color=PALETTE["PRIMARY"], font_size=40).move_to(u_box.get_center())
        k_box = Square(side_length=1.4, color=PALETTE["ACCENT_CORAL"]).shift(UP * 1.5 + RIGHT * 2)
        k_lbl = MathTex("K", color=PALETTE["PRIMARY"], font_size=40).move_to(k_box.get_center())
        plus = MathTex("+", color=PALETTE["PRIMARY"], font_size=44).shift(UP * 1.5)

        self.play(Create(u_box), Write(u_lbl), Create(k_box), Write(k_lbl), Write(plus), run_time=1.2)
        for _ in range(3):
            self.play(u_box.animate.scale(1.2), k_box.animate.scale(0.8), run_time=1.0)
            self.play(u_box.animate.scale(1.0), k_box.animate.scale(1.0), run_time=1.0)

        self.show_bottom_derivation_panel(r"E = U + K = \text{constant}")
        self.wait(15)

    def render_gravitational_force_layout(self):
        m1 = Circle(radius=0.8, color=PALETTE["ACCENT_GOLD"]).shift(UP * 1.0 + LEFT * 2.5)
        m2 = Circle(radius=0.8, color=PALETTE["ACCENT_GOLD"]).shift(UP * 1.0 + RIGHT * 2.5)
        f_vec = Arrow(LEFT * 1.5, RIGHT * 1.5, color=PALETTE["ACCENT_GREEN"], stroke_width=5).shift(UP * 1.0)

        self.play(Create(m1), Create(m2), GrowArrow(f_vec), run_time=1.2)
        self.show_bottom_derivation_panel(r"F = G\frac{m_1 m_2}{r^2}")
        self.wait(15)

    def render_kinetic_theory_layout(self):
        container = RoundedRectangle(corner_radius=0.3, width=5, height=4, color=PALETTE["ACCENT_BLUE"]).shift(UP * 1.0)
        particle = Dot(UP * 1.0, color=PALETTE["ACCENT_CORAL"], radius=0.2)
        
        self.play(Create(container), FadeIn(particle), run_time=1.0)
        for _ in range(4):
            self.play(particle.animate.shift(UP * 1.5 + RIGHT * 1.5), run_time=0.8)
            self.play(particle.animate.shift(DOWN * 1.5 + LEFT * 2.0), run_time=0.8)

        self.show_bottom_derivation_panel(r"PV = \frac{1}{3} N m \overline{v^2}, \quad K.E. = \frac{3}{2} kT")
        self.wait(15)

    def render_harmonic_oscillator_layout(self):
        spring = ParametricFunction(lambda t: np.array([t, np.sin(t * 8) * 0.5 + 1.0, 0]), t_range=[-3, 3], color=PALETTE["ACCENT_GREEN"], stroke_width=4)
        mass = Square(side_length=1.2, color=PALETTE["ACCENT_CORAL"]).shift(UP * 1.0 + RIGHT * 3)

        self.play(Create(spring), Create(mass), run_time=1.2)
        for _ in range(3):
            self.play(mass.animate.shift(LEFT * 1.5), run_time=0.8)
            self.play(mass.animate.shift(RIGHT * 1.5), run_time=0.8)

        self.show_bottom_derivation_panel(r"m \frac{d^2 x}{dt^2} + kx = 0, \quad \omega = \sqrt{\frac{k}{m}}")
        self.wait(15)

    def render_gravitational_potential_layout(self):
        earth = Circle(radius=1.5, color=PALETTE["ACCENT_BLUE"]).shift(UP * 0.5)
        orbit = Circle(radius=2.8, color=PALETTE["MUTED"], stroke_width=2, stroke_opacity=0.5).shift(UP * 0.5)
        sat = Dot(UP * 3.3, color=PALETTE["ACCENT_GOLD"], radius=0.15)

        self.play(Create(earth), Create(orbit), Fade
