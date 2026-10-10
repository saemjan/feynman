#!/usr/init/env python3
"""
Elite JEE Advanced & 3b1b-Grade Physics Rendering Engine.
Features rigorous Free-Body Diagrams, Phasor/Calculus curves, Huygens wavefronts,
and exact mathematical derivations tailored for top-tier competitive engineering aspirants.
"""

import sys
import numpy as np
from manim import *

# 3b1b Signature Luxury Palette
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
config.pixel_height = 1920  # Vertical 9:16 Short Format
config.frame_rate = 30


class UniversalPhysicsScene(MovingCameraScene):
    """Base class for rigorous JEE Advanced physics visualizations."""

    def construct(self):
        video_id = getattr(self, "video_id", "feynman_circuit_rc")
        
        if "rc" in video_id or "capacitor" in video_id:
            self.render_advanced_rc_transient()
        elif "lens" in video_id or "optics" in video_id:
            self.render_huygens_lens_refraction()
        elif "pulley" in video_id or "mechanics" in video_id:
            self.render_rigorous_pulley_fbd()
        elif "dipole" in video_id or "torque" in video_id:
            self.render_rigorous_dipole_torque()
        elif "photoelectric" in video_id or "quantum" in video_id:
            self.render_einstein_photoelectric_graph()
        else:
            self.render_default_advanced_physics(video_id)

    def create_rigorous_header(self, title_str: str, concept_str: str):
        """Creates an academic header suitable for advanced problem-solving."""
        title = Tex(title_str, color=PALETTE["ACCENT_BLUE"], font_size=38).to_edge(UP, buff=0.8)
        subtitle = Tex(concept_str, color=PALETTE["PRIMARY"], font_size=24).next_to(title, DOWN, buff=0.2)
        underline = Line(LEFT * 4.5, RIGHT * 4.5, color=PALETTE["MUTED"], stroke_width=1).next_to(subtitle, DOWN, buff=0.2)
        
        header_group = VGroup(title, subtitle, underline)
        self.play(FadeIn(header_group, shift=DOWN * 0.2), run_time=0.8)
        return header_group

    def display_derivation_box(self, latex_str: str):
        """Displays rigorous mathematical formulations in an architectural panel."""
        eq = MathTex(latex_str, color=PALETTE["ACCENT_GOLD"], font_size=32)
        box = SurroundingRectangle(eq, color=PALETTE["ACCENT_BLUE"], buff=0.25, corner_radius=0.1, stroke_width=1.5)
        box.set_fill(PALETTE["PANEL_BG"], opacity=0.9)
        
        panel = VGroup(box, eq).to_edge(DOWN, buff=0.8)
        self.play(GrowFromCenter(panel), run_time=0.8)
        return panel

    def render_advanced_rc_transient(self):
        """RC Circuit Transient Analysis with differential equation and capacitor energy curves."""
        self.create_rigorous_header("RC Circuit Transient Analysis", "Solving $\\frac{dq}{dt} + \\frac{q}{RC} = \\frac{V_0}{R}$ via Calculus")

        # Schematic
        circuit_group = VGroup(
            Dot(LEFT * 2 + UP * 1, color=PALETTE["ACCENT_GOLD"]),
            Line(LEFT * 2 + UP * 1, LEFT * 1 + UP * 1, color=PALETTE["PRIMARY"], stroke_width=4),
            MathTex("R", color=PALETTE["ACCENT_GOLD"]).shift(LEFT * 1.5 + UP * 1.4),
            Line(LEFT * 1 + UP * 1, RIGHT * 1 + UP * 1, color=PALETTE["PRIMARY"], stroke_width=4),
            Line(RIGHT * 1 + UP * 1.3, RIGHT * 1 + UP * 0.7, color=PALETTE["ACCENT_BLUE"], stroke_width=6),
            Line(RIGHT * 1.3 + UP * 1.3, RIGHT * 1.3 + UP * 0.7, color=PALETTE["ACCENT_BLUE"], stroke_width=6),
            MathTex("C", color=PALETTE["ACCENT_BLUE"]).shift(RIGHT * 1.15 + UP * 1.6)
        ).shift(UP * 1.5)

        self.play(Create(circuit_group), run_time=1.0)

        # Axes for Exponential Charge Growth
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.2, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"color": PALETTE["MUTED"], "include_numbers": False}
        ).shift(DOWN * 1.0)

        labels = axes.get_axis_labels(x_label="t", y_label="q(t)")
        curve = axes.plot(lambda t: 1 - np.exp(-t), color=PALETTE["ACCENT_GREEN"], stroke_width=3)
        curve_label = MathTex("q(t) = C V_0 (1 - e^{-t/\\tau})", color=PALETTE["ACCENT_GREEN"], font_size=24).next_to(curve, UP)

        self.play(Create(axes), Create(labels), run_time=1.0)
        self.play(Create(curve), FadeIn(curve_label), run_time=2.0)

        self.display_derivation_box(r"U_E = \frac{1}{2}\frac{Q^2}{C} = \int_0^t i^2 R \, dt")
        self.wait(2)

    def render_huygens_lens_refraction(self):
        """Optics: Huygens Wavefront Construction & Lens Maker's Rigorous Derivation."""
        self.create_rigorous_header("Wavefront Refraction in Lenses", "Huygens' Principle: Geometrical Path Length Equality $\\int n ds = \\text{const}$")

        # Lens Profile
        lens = ImplicitFunction(
            lambda x, y: (x/0.7)**2 + (y/3.2)**2 - 1,
            color=PALETTE["ACCENT_BLUE"],
            stroke_width=2.5
        ).set_fill(PALETTE["ACCENT_BLUE"], opacity=0.15).shift(DOWN * 0.5)

        axis = DashedLine(LEFT * 4.5, RIGHT * 4.5, color=PALETTE["MUTED"]).shift(DOWN * 0.5)
        self.play(Create(axis), DrawBorderThenFill(lens), run_time=1.2)

        # Incoming parallel wavefronts turning into converging spherical wavefronts
        incoming = VGroup(*[
            Arrow(LEFT * 4 + UP * y, LEFT * 0.5 + UP * y, color=PALETTE["ACCENT_GOLD"], buff=0, stroke_width=2.5)
            for y in np.linspace(-1.8, 0.8, 5)
        ])
        focal_pt = Dot(RIGHT * 3.0 + DOWN * 0.5, color=PALETTE["ACCENT_CORAL"])
        focal_lbl = MathTex("F", color=PALETTE["ACCENT_CORAL"]).next_to(focal_pt, DOWN)

        self.play(Create(incoming), run_time=1.0)
        
        converging = VGroup(*[
            Line(LEFT * 0.5 + UP * y, RIGHT * 3.0 + DOWN * 0.5, color=PALETTE["ACCENT_GOLD"], stroke_width=2.5)
            for y in np.linspace(-1.8, 0.8, 5)
        ])
        self.play(Transform(incoming, converging), FadeIn(focal_pt), FadeIn(focal_lbl), run_time=2.0)

        self.display_derivation_box(r"\frac{1}{f} = (\mu_{rel} - 1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right)")
        self.wait(2)

    def render_rigorous_pulley_fbd(self):
        """Rigorous Mechanics: Atwood Machine Free-Body Diagram with constraint equations."""
        self.create_rigorous_header("Atwood Machine Dynamics", "Constraint: $x_1 + x_2 = l \\implies \\ddot{x}_1 + \\ddot{x}_2 = 0$")

        pulley = Circle(radius=0.4, color=PALETTE["ACCENT_BLUE"], stroke_width=3).shift(UP * 2.5)
        string_l = Line(UP * 2.5 + LEFT * 0.4, DOWN * 0.5 + LEFT * 0.4, color=PALETTE["PRIMARY"], stroke_width=2.5)
        string_r = Line(UP * 2.5 + RIGHT * 0.4, DOWN * 1.5 + RIGHT * 0.4, color=PALETTE["PRIMARY"], stroke_width=2.5)

        m1_box = Square(side_length=0.7, color=PALETTE["ACCENT_CORAL"], stroke_width=2.5).set_fill(PALETTE["ACCENT_CORAL"], opacity=0.2).next_to(string_l, DOWN, buff=0)
        m2_box = Square(side_length=0.8, color=PALETTE["ACCENT_BLUE"], stroke_width=2.5).set_fill(PALETTE["ACCENT_BLUE"], opacity=0.2).next_to(string_r, DOWN, buff=0)

        # FBD Vectors
        t_vec1 = Arrow(m1_box.get_top(), m1_box.get_top() + UP * 0.8, color=PALETTE["ACCENT_GREEN"], buff=0)
        w_vec1 = Arrow(m1_box.get_center(), m1_box.get_center() + DOWN * 0.8, color=PALETTE["ACCENT_CORAL"], buff=0)
        
        fbd_group = VGroup(pulley, string_l, string_r, m1_box, m2_box, t_vec1, w_vec1)
        self.play(Create(fbd_group), run_time=1.2)

        # Acceleration animation
        self.play(
            m1_box.animate.shift(UP * 1.0),
            m2_box.animate.shift(DOWN * 1.0),
            t_vec1.animate.shift(UP * 1.0),
            w_vec1.animate.shift(UP * 1.0),
            run_time=2.0,
            rate_func=rate_functions.ease_in_out_sine
        )

        self.display_derivation_box(r"a = \left(\frac{m_2 - m_1}{m_1 + m_2}\right)g, \quad T = \frac{2m_1 m_2}{m_1 + m_2}g")
        self.wait(2)

    def render_rigorous_dipole_torque(self):
        """Electromagnetism: Electric Dipole in Uniform Field with vector cross product."""
        self.create_rigorous_header("Dipole in Uniform Electric Field", "Net Force $\\vec{F} = 0$, but Torque $\\vec{\\tau} = \\vec{p} \\times \\vec{E}$ Exists")

        # Vector field grid
        field = VGroup(*[
            Arrow(LEFT * 3 + RIGHT * x + UP * y, LEFT * 2 + RIGHT * x + UP * y, color=PALETTE["ACCENT_BLUE"], buff=0, stroke_width=1.5, tip_length=0.08)
            for x in np.linspace(0, 6, 6)
            for y in np.linspace(-2, 2, 5)
        ])
        self.play(FadeIn(field, lag_ratio=0.02), run_time=1.2)

        # Dipole charges
        q_pos = Dot(LEFT * 1 + UP * 0.6, color=PALETTE["ACCENT_CORAL"], radius=0.18)
        q_neg = Dot(RIGHT * 1 + DOWN * 0.6, color=PALETTE["ACCENT_BLUE"], radius=0.18)
        rod = Line(q_pos.get_center(), q_neg.get_center(), color=PALETTE["ACCENT_GOLD"], stroke_width=3)
        
        dipole = VGroup(rod, q_pos, q_neg)
        self.play(GrowFromCenter(dipole), run_time=1.0)

        # Torque rotation
        self.play(Rotate(dipole, angle=-0.6, about_point=ORIGIN), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)

        self.display_derivation_box(r"\vec{\tau} = \vec{p} \times \vec{E} \implies \tau = pE \sin\theta")
        self.wait(2)

    def render_einstein_photoelectric_graph(self):
        """Quantum Physics: Einstein's Photoelectric Equation & Threshold Frequency Graph."""
        self.create_rigorous_header("Einstein's Photoelectric Equation", "Linear Fit: $K_{\max} = h\\nu - \\phi$ where Slope is Universal $h$")

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-1, 4, 1],
            x_length=6,
            y_length=3.5,
            axis_config={"color": PALETTE["MUTED"]}
        ).shift(DOWN * 0.5)

        labels = axes.get_axis_labels(x_label="\\nu", y_label="K_{\max}")
        
        # Photoelectric straight line intercepting at threshold frequency
        line = axes.plot(lambda x: max(0, x - 1.5), color=PALETTE["ACCENT_GREEN"], x_range=[1.5, 5.5], stroke_width=3)
        threshold_dot = Dot(axes.c2p(1.5, 0), color=PALETTE["ACCENT_GOLD"])
        thresh_label = MathTex("\\nu_0", color=PALETTE["ACCENT_GOLD"], font_size=24).next_to(threshold_dot, DOWN)

        self.play(Create(axes), Create(labels), run_time=1.0)
        self.play(Create(line), FadeIn(threshold_dot), FadeIn(thresh_label), run_time=1.5)

        self.display_derivation_box(r"h\nu = \phi + K_{\max}, \quad eV_s = h\nu - \phi")
        self.wait(2)

    def render_default_advanced_physics(self, topic: str):
        self.create_rigorous_header(topic.replace("_", " ").title(), "Advanced JEE Physics Analysis")
        self.display_derivation_box(r"\oint \vec{E} \cdot d\vec{A} = \frac{q_{\text{encl}}}{\varepsilon_0}, \quad \nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}")
        self.wait(2)
