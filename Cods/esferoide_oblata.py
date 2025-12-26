from manim import *

class EsferaAEsferoideOblata(ThreeDScene):
    def construct(self):

        # Cámara
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=45 * DEGREES,
            zoom=0.9
        )

        # Ejes cartesianos 3D
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-3, 3],
            axis_config={"color": WHITE}
        )

        labels = axes.get_axis_labels(
            Text("x"), Text("y"), Text("z")
        )

        # Esfera
        sphere = Sphere(
            radius=1.5,
            resolution=(32, 32),
            fill_color=BLUE,
            fill_opacity=0.6,
            stroke_color=BLUE_E
        )

        # Animaciones iniciales
        self.play(Create(axes), Write(labels))
        self.play(FadeIn(sphere))
        self.wait(1)

        # Transformación a esferoide oblata
        oblate = sphere.copy().scale([1, 1, 0.5])

        self.play(
            Transform(sphere, oblate),
            run_time=3
        )

        self.wait(2)


class SphereToOblate(ThreeDScene):
    def construct(self):
        
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # -------------------- SPHERE --------------------
        sphere = Surface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(30, 30),
            checkerboard_colors=[RED_D, RED_E]
        )
        
        # -------------------- OBLATE SPHEROID --------------------
        # Parámetros para el esferoide oblato
        a = 1.5  # parámetro de escala
        
        oblate_spheroid = Surface(
            lambda u, v: np.array([
                a * np.cosh(u) * np.cos(v) * np.cos(0),  # empezamos con phi=0 para simplificar
                a * np.cosh(u) * np.cos(v) * np.sin(TAU * 0.5),  # variamos phi para dar volumen
                a * np.sinh(u) * np.sin(v)
            ]),
            u_range=[0, 1.2],  # rango para mu
            v_range=[-PI/2, PI/2],  # rango para nu
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        # Versión completa del esferoide oblato (revolucionando alrededor del eje z)
        oblate_full = Surface(
            lambda u, v: np.array([
                a * np.cosh(0.8) * np.cos(u) * np.cos(v),  # mu fijo, variamos nu y phi
                a * np.cosh(0.8) * np.cos(u) * np.sin(v),
                a * np.sinh(0.8) * np.sin(u)
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        # -------------------- TITLES AND EQUATIONS --------------------
        title_sphere = Text("Sphere", font_size=44).to_corner(UL)
        title_oblate = Text("Oblate Spheroid", font_size=44).to_corner(UL)
        
        # Ecuaciones de la esfera
        eq_sphere = MathTex(
            r"x &= R\cos\theta\cos\varphi\\",
            r"y &= R\cos\theta\sin\varphi\\",
            r"z &= R\sin\theta",
            font_size=32
        ).to_corner(UR)
        
        # Ecuaciones del esferoide oblato
        eq_oblate = MathTex(
            r"x &= a\cosh\mu\cos\nu\cos\varphi\\",
            r"y &= a\cosh\mu\cos\nu\sin\varphi\\",
            r"z &= a\sinh\mu\sin\nu",
            font_size=32
        ).to_corner(UR)
        
        # -------------------- CAMERA SETUP --------------------
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)
        
        # -------------------- ANIMATION SEQUENCE --------------------
        self.add(axes)
        
        # Mostrar esfera con su título y ecuaciones
        self.add_fixed_in_frame_mobjects(title_sphere, eq_sphere)
        self.play(
            Create(sphere),
            Write(title_sphere),
            Write(eq_sphere)
        )
        self.wait(2)
        
        # Transformar a esferoide oblato
        self.remove(title_sphere, eq_sphere)
        self.add_fixed_in_frame_mobjects(title_oblate, eq_oblate)
        self.play(
            ReplacementTransform(sphere, oblate_full),
            Write(title_oblate),
            Write(eq_oblate),
            run_time=2
        )
        self.wait(3)
        
        # Fade out
        self.play(
            FadeOut(oblate_full),
            FadeOut(title_oblate),
            FadeOut(eq_oblate),
            FadeOut(axes)
        )
        self.wait()