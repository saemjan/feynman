#!/usr/bin/env python3
"""
Universal 3b1b & Feynman-Grade Physics Rendering Engine.
Features dynamic camera zooming, glowing vector fields, fluid particle simulations,
and precise LaTeX typesetting tailored for JEE, NEET, and CBSE mastery.
"""

import sys
from manim import *

# 3b1b Signature Color Palette
PALETTE = {
    "BG": "#111111",
    "PRIMARY": "#ECE6E2",
    "ACCENT_BLUE": "#58C4DD",
    "ACCENT_GOLD": "#FFD700",
    "ACCENT_CORAL": "#FF6B6B",
    "ACCENT_GREEN": "#83C167",
    "MUTED": "#888888"
}

config.background_color = PALETTE["BG"]
config.pixel_width = 1080
config.pixel_height = 1920  # Vertical 9:16 Short format
config.frame_rate = 30


class UniversalPhysicsScene(MovingCameraScene):
    """Base class providing 3b1b-style typography, camera framing, and glowing visual primitives."""

    def construct(self):
        # Read topic from arguments or environment
        video_id = getattr(self, "video_id", "feynman_circuit_rc")
        
        # Dispatch to specific high-elegance visual primitive
        if "rc" in video_id or "capacitor" in video_id:
            self.render_capacitor_elegance()
        elif "lens" in video_id or "optics" in video_id:
            self.render_lens_wavefront_elegance()
        elif "pulley" in video_id or "mechanics" in video_id:
            self.render_pulley_elegance()
        elif "dipole" in video_id or "torque" in video_id:
            self.render_dipole_elegance()
        elif "photoelectric" in video_id or "quantum" in video_id:
            self.render_photoelectric_elegance()
        else:
            self.render_default_physics_elegance(video_id)

    def create_header(self, title_text: str, subtitle_text: str):
        """Creates a minimalist, elegant 3b1b title header anchored at the top."""
        title = Tex(title_text, color=PALETTE["ACCENT_BLUE"], font_size=42).to_edge(UP, buff=1.2)
        subtitle = Tex(subtitle_text, color=PALETTE["PRIMARY"], font_size=26).next_to(title, DOWN, buff=0.3)
        
        header_group = VGroup(title, subtitle)
        self.play(FadeIn(header_group, shift=DOWN * 0.3), run_time=0.8)
        return header_group

    def display_equation_box(self, latex_str: str):
        """Displays key equations in a frosted glass aesthetic box at the bottom."""
        eq = MathTex(latex_str, color=PALETTE["ACCENT_GOLD"], font_size=36)
        box = SurroundingRectangle(eq, color=PALETTE["ACCENT_BLUE"], buff=0.3, corner_radius=0.15, stroke_width=2)
        box.set_fill(PALETTE["BG"], opacity=0.85)
        
        eq_group = VGroup(box, eq).to_edge(DOWN, buff=1.0)
        self.play(GrowFromCenter(eq_group), run_time=0.8)
        return eq_group

    def render_capacitor_elegance(self):
        """Feynman hydraulic-RC analogy with glowing charge buildup and exponential curves."""
        self.create_header("How Capacitors Store Energy", "Voltage builds up as charges crowd together")

        # Draw Circuit: Resistor (pipe) and Capacitor (rubber tank)
        resistor = VGroup(
            Line(LEFT * 3, LEFT * 1.5, color=PALETTE["ACCENT_GOLD"], stroke_width=4),
            ZigZagInductionLine(LEFT * 1.5, LEFT * 0.5, color=PALETTE["ACCENT_GOLD"], stroke_width=4),
            Line(LEFT * 0.5, LEFT * 0, color=PALETTE["ACCENT_GOLD"], stroke_width=4)
        )
        
        plate_top = Line(UP * 1, DOWN * 1, color=PALETTE["ACCENT_BLUE"], stroke_width=6).shift(RIGHT * 1.5)
        plate_bot = Line(UP * 1, DOWN * 1, color=PALETTE["ACCENT_BLUE"], stroke_width=6).shift(RIGHT * 2.2)
        capacitor_label = MathTex("C", color=PALETTE["ACCENT_BLUE"]).next_to(plate_top, UP)
        resistor_label = MathTex("R", color=PALETTE["ACCENT_GOLD"]).next_to(resistor, UP)

        circuit = VGroup(resistor, plate_top, plate_bot, capacitor_label, resistor_label).shift(UP * 0.5)
        self.play(Create(circuit), run_time=1.5)

        # Dynamic Particle Flow (Charges crowding)
        dots = VGroup(*[Dot(point=LEFT * 3 + RIGHT * i * 0.2, color=PALETTE["ACCENT_CORAL"], radius=0.08) for i in range(10)])
        self.play(FadeIn(dots), run_time=0.5)

        # Animate flow slowing down exponentially
        self.play(
            dots.animate.shift(RIGHT * 3.2),
            rate_func=rate_functions.exponential_decay,
            run_time=3.0
        )

        # Equation Reveal
        self.display_equation_box(r"V(t) = V_0(1 - e^{-t/RC}), \quad \tau = RC")
        self.wait(2)

    def render_lens_wavefront_elegance(self):
        """Feynman optical time-delay wavefront bending through a convex lens."""
        self.create_header("Why Lenses Bend Light", "Curvature creates a time delay across wavefronts")

        # Lens shape
        lens = ImplicitFunction(
            lambda x, y: (x/0.8)**2 + (y/3)**2 - 1,
            color=PALETTE["ACCENT_BLUE"],
            stroke_width=3
        ).set_fill(PALETTE["ACCENT_BLUE"], opacity=0.2)

        optical_axis = DashedLine(LEFT * 4, RIGHT * 4, color=PALETTE["MUTED"])
        self.play(Create(optical_axis), DrawBorderThenFill(lens), run_time=1.2)

        # Wavefront rays bending to focal point
        incoming_rays = VGroup(*[
            Arrow(LEFT * 4 + UP * y_offset, LEFT * 0.8 + UP * y_offset, color=PALETTE["ACCENT_GOLD"], buff=0, stroke_width=3)
            for y_offset in [-1.5, -0.75, 0, 0.75, 1.5]
        ])
        
        focal_point = Dot(RIGHT * 3.5, color=PALETTE["ACCENT_CORAL"])
        focal_label = MathTex("F", color=PALETTE["ACCENT_CORAL"]).next_to(focal_point, DOWN)

        converging_rays = VGroup(*[
            Arrow(LEFT * 0.8 + UP * y_offset, RIGHT * 3.5, color=PALETTE["ACCENT_GOLD"], buff=0, stroke_width=3)
            for y_offset in [-1.5, -0.75, 0, 0.75, 1.5]
        ])

        self.play(Create(incoming_rays), run_time=1.0)
        self.play(Transform(incoming_rays, converging_rays), FadeIn(focal_point), FadeIn(focal_label), run_time=2.0)

        self.display_equation_box(r"\frac{1}{f} = (n-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right), \quad v = \frac{c}{n}")
        self.wait(2)

    def render_pulley_elegance(self):
        """Frictionless pulley with dynamic mass imbalance acceleration."""
        self.create_header("Discovering Acceleration in Pulley", "Symmetry breaks when mass ratios differ")

        pulley_circle = Circle(radius=0.5, color=PALETTE["ACCENT_BLUE"], stroke_width=4).shift(UP * 2)
        string_left = Line(UP * 2 + LEFT * 0.5, DOWN * 0.5 + LEFT * 0.5, color=PALETTE["PRIMARY"], stroke_width=3)
        string_right = Line(UP * 2 + RIGHT * 0.5, DOWN * 1.5 + RIGHT * 0.5, color=PALETTE["PRIMARY"], stroke_width=3)

        m1_box = Square(side_length=0.8, color=PALETTE["ACCENT_CORAL"], stroke_width=3).set_fill(PALETTE["ACCENT_CORAL"], opacity=0.3).next_to(string_left, DOWN, buff=0)
        m2_box = Square(side_length=0.9, color=PALETTE["ACCENT_BLUE"], stroke_width=3).set_fill(PALETTE["ACCENT_BLUE"], opacity=0.3).next_to(string_right, DOWN, buff=0)
        
        m1_label = MathTex("m_1", color=PALETTE["PRIMARY"]).move_to(m1_box.get_center())
        m2_label = MathTex("m_2", color=PALETTE["PRIMARY"]).move_to(m2_box.get_center())

        pulley_system = VGroup(pulley_circle, string_left, string_right, m1_box, m2_box, m1_label, m2_label)
        self.play(Create(pulley_system), run_time=1.2)

        # Dynamic motion simulation (m2 accelerates down, m1 up)
        self.play(
            m1_box.animate.shift(UP * 1.2),
            m2_box.animate.shift(DOWN * 1.2),
            string_left.animate.stretch_about_point(0.7, UP * 2, DOWN),
            string_right.animate.stretch_about_point(1.4, UP * 2, DOWN),
            run_time=2.0,
            rate_func=rate_functions.ease_in_out_sine
        )

        self.display_equation_box(r"a = \frac{m_2 - m_1}{m_1 + m_2}g, \quad T = \frac{2m_1 m_2}{m_1 + m_2}g")
        self.wait(2)

    def render_dipole_elegance(self):
        """Glowing vector field demonstrating torque rotation on a dipole."""
        self.create_header("Why a Dipole Starts Turning", "Electric fields create a twist - not a push")

        # Create background vector field grid
        field_arrows = VGroup(*[
            Arrow(start=LEFT * 3 + RIGHT * x + UP * y, end=LEFT * 2.2 + RIGHT * x + UP * y, color=PALETTE["ACCENT_BLUE"], buff=0, stroke_width=2, tip_length=0.1)
            for x in np.linspace(0, 6, 5)
            for y in np.linspace(-2, 2, 5)
        ])
        self.play(FadeIn(field_arrows, lag_ratio=0.05), run_time=1.5)

        # Dipole charges (+q and -q) connected by a rigid rod
        pos_charge = Dot(LEFT * 1 + UP * 0.5, color=PALETTE["ACCENT_CORAL"], radius=0.2)
        neg_charge = Dot(RIGHT * 1 + DOWN * 0.5, color=PALETTE["ACCENT_BLUE"], radius=0.2)
        rod = Line(pos_charge.get_center(), neg_charge.get_center(), color=PALETTE["ACCENT_GOLD"], stroke_width=4)
        
        plus_lbl = MathTex("+q", color=PALETTE["BG"], font_size=20).move_to(pos_charge.get_center())
        minus_lbl = MathTex("-q", color=PALETTE["BG"], font_size=20).move_to(neg_charge.get_center())

        dipole = VGroup(rod, pos_charge, neg_charge, plus_lbl, minus_lbl)
        self.play(GrowFromCenter(dipole), run_time=1.0)

        # Rotate dipole to align with field
        self.play(Rotate(dipole, angle=-0.5, about_point=ORIGIN), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)

        self.display_equation_box(r"\vec{F}_{\text{net}} = \vec{0}, \quad \vec{\tau} = \vec{p} \times \vec{E}")
        self.wait(2)

    def render_photoelectric_elegance(self):
        """Photon packet impacts knocking out electrons instantly."""
        self.create_header("Light Beats Metals in Whacks", "Photons deliver energy in single packets")

        metal_plate = Rectangle(width=4, height=0.4, color=PALETTE["ACCENT_BLUE"]).to_edge(DOWN, buff=2.0)
        plate_label = MathTex(r"\text{Metal Plate ($\Phi$)}", color=PALETTE["PRIMARY"]).next_to(metal_plate, DOWN)
        self.play(Create(metal_plate), FadeIn(plate_label), run_time=1.0)

        # Incoming photon wave packet
        photon = ParametricFunction(
            lambda t: np.array([t, np.sin(t * 4) * 0.3 + 1, 0]),
            t_range=[-3, 0],
            color=PALETTE["ACCENT_GOLD"],
            stroke_width=4
        )
        photon_label = MathTex(r"h\nu", color=PALETTE["ACCENT_GOLD"]).next_to(photon, UP)
        
        self.play(Create(photon), FadeIn(photon_label), run_time=1.0)

        # Electron ejection
        electron = Dot(metal_plate.get_center(), color=PALETTE["ACCENT_GREEN"], radius=0.15)
        e_label = MathTex("e^{-}", color=PALETTE["ACCENT_GREEN"], font_size=24).next_to(electron, UP)
        
        self.play(FadeIn(electron), FadeIn(e_label), run_time=0.3)
        self.play(
            electron.animate.shift(UP * 2 + RIGHT * 1.5),
            e_label.animate.shift(UP * 2 + RIGHT * 1.5),
            FadeOut(photon),
            FadeOut(photon_label),
            run_time=1.2
        )

        self.display_equation_box(r"K_{\max} = h\nu - \Phi, \quad E = h\nu")
        self.wait(2)

    def render_default_physics_elegance(self, topic: str):
        self.create_header(topic.replace("_", " ").title(), "Visualizing Fundamental Physics Principles")
        self.display_equation_box(r"E = mc^2, \quad \vec{\nabla} \cdot \vec{E} = \frac{\rho}{\varepsilon_0}")
        self.wait(2)


class ZigZagInductionLine(VMobject):
    """Helper utility for rendering clean resistor zig-zags in Manim."""
    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        path = VMobject()
        points = [start]
        num_peaks = 5
        vector = end - start
        unit_vec = vector / num_peaks
        perp = np.array([-unit_vec[1], unit_vec[0], 0]) * 0.4
        
        for i in range(1, num_peaks):
            p = start + unit_vec * i + (perp if i % 2 == 1 else -perp)
            points.append(p)
        points.append(end)
        path.set_points_as_corners(points)
        self.add(path)
