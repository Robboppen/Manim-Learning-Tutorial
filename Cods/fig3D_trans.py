from manim import *
import numpy as np

class SurfacesAnimation(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes()

        # -------------------- CYLINDER --------------------
        cylinder = Surface(
            lambda u, v: np.array([
                np.cos(TAU * v),
                np.sin(TAU * v),
                2 * (1 - u)
            ]),
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(6, 32),
            fill_opacity=0.5,
            fill_color=GRAY
        )

        # -------------------- PARABOLOID --------------------
        paraboloid = Surface(
            lambda u, v: np.array([
                u * np.cos(v),
                u * np.sin(v),
                u**2
            ]),
            u_range=[0, 2],
            v_range=[0, TAU],
            resolution=(10, 32),
            checkerboard_colors=[PURPLE_D, PURPLE_E]
        ).scale(2)

        # -------------------- HYPERBOLIC PARABOLOID --------------------
        para_hyp = Surface(
            lambda u, v: np.array([
                u,
                v,
                u**2 - v**2
            ]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(15, 32),
            checkerboard_colors=[BLUE_D, BLUE_E]
        )

        # -------------------- CONE --------------------
        cone = Surface(
            lambda u, v: np.array([
                u * np.cos(v),
                u * np.sin(v),
                u
            ]),
            u_range=[0, 2],
            v_range=[0, TAU],
            resolution=(15, 32),
            checkerboard_colors=[GREEN_D, GREEN_E]
        )

        # -------------------- ONE-SHEET HYPERBOLOID --------------------
        hip_one_side = Surface(
            lambda u, v: np.array([
                np.cosh(u) * np.cos(v),
                np.cosh(u) * np.sin(v),
                np.sinh(u)
            ]),
            u_range=[-1.5, 1.5],
            v_range=[0, TAU],
            resolution=(15, 32),
            checkerboard_colors=[YELLOW_D, YELLOW_E]
        )

        # -------------------- ELLIPSOID --------------------
        ellipsoid = Surface(
            lambda u, v: np.array([
                np.cos(u) * np.cos(v),
                2 * np.cos(u) * np.sin(v),
                0.5 * np.sin(u)
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(15, 32),
            checkerboard_colors=[TEAL_D, TEAL_E]
        ).scale(2)

        # -------------------- SPHERE --------------------
        sphere = Surface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(15, 32),
            checkerboard_colors=[RED_D, RED_E]
        ).scale(2)

        # -------------------- TITLES --------------------
        title_sphere = Text("Sphere", font_size=48).to_corner(UL)
        title_ellipsoid = Text("Ellipsoid", font_size=48).to_corner(UL)
        title_cone = Text("Cone", font_size=48).to_corner(UL)
        title_hyperboloid = Text("Hyperboloid (One Sheet)", font_size=36).to_corner(UL)
        title_para_hyp = Text("Hyperbolic Paraboloid", font_size=40).to_corner(UL)
        title_paraboloid = Text("Paraboloid", font_size=48).to_corner(UL)
        title_cylinder = Text("Cylinder", font_size=48).to_corner(UL)

        # -------------------- CAMERA --------------------
        self.set_camera_orientation(phi=75 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)

        # -------------------- ANIMATION SEQUENCE --------------------
        self.add(axes)

        # Agregar título fijo en el frame
        self.add_fixed_in_frame_mobjects(title_sphere)
        self.play(Create(sphere), Write(title_sphere))
        self.wait()

        self.remove(title_sphere)
        self.add_fixed_in_frame_mobjects(title_ellipsoid)
        self.play(
            ReplacementTransform(sphere, ellipsoid),
            Write(title_ellipsoid)
        )
        self.wait()

        self.remove(title_ellipsoid)
        self.add_fixed_in_frame_mobjects(title_cone)
        self.play(
            ReplacementTransform(ellipsoid, cone),
            Write(title_cone)
        )
        self.wait()

        self.remove(title_cone)
        self.add_fixed_in_frame_mobjects(title_hyperboloid)
        self.play(
            ReplacementTransform(cone, hip_one_side),
            Write(title_hyperboloid)
        )
        self.wait()

        self.remove(title_hyperboloid)
        self.add_fixed_in_frame_mobjects(title_para_hyp)
        self.play(
            ReplacementTransform(hip_one_side, para_hyp),
            Write(title_para_hyp)
        )
        self.wait()

        self.remove(title_para_hyp)
        self.add_fixed_in_frame_mobjects(title_paraboloid)
        self.play(
            ReplacementTransform(para_hyp, paraboloid),
            Write(title_paraboloid)
        )
        self.wait()

        self.remove(title_paraboloid)
        self.add_fixed_in_frame_mobjects(title_cylinder)
        self.play(
            ReplacementTransform(paraboloid, cylinder),
            Write(title_cylinder)
        )
        self.wait()

        self.play(FadeOut(cylinder), FadeOut(title_cylinder))