from manim import *
import numpy as np

class Plot1(Scene):
    def construct(self):
        ejes=Axes(x_range=[-7, 7, 0.5],
                  y_range=[-50, 50, 5],
                  axis_config={
                      "color": BLUE,
                  },

                  x_axis_config={
                      "numbers_to_include": np.arange(2, 7.5, 1.5),
                  },
                  y_axis_config={"numbers_to_include": np.arange(0, 60, 15),},
                  )
        labels=ejes.get_axis_labels(MathTex("x", color= RED), MathTex("y", color=RED))
        

        
        graph = ejes.plot( lambda x: 2*np.e**x, x_range=[-7, 7], color=GREEN )


        self.play(Create(ejes))
        self.play(Create(graph), run_time=2)
        self.play(Write(labels))
        self.wait(2)

class Plot2(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-2*np.pi, 2*np.pi, np.pi/2],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={
                "color": BLUE,
                "include_numbers": False,  
            },
            tips=False,
        )

        # Etiquetas en π (solo estas aparecen)
        axes.get_x_axis().add_labels({
            -2*np.pi: MathTex(r"-2\pi"),
            -np.pi: MathTex(r"-\pi"),
            0: MathTex("0"),
            np.pi: MathTex(r"\pi"),
            2*np.pi: MathTex(r"2\pi"),
        })

        labels = axes.get_axis_labels(
            MathTex("x", color=RED),
            MathTex(r"\sin x", color=RED)
        )

        seno = axes.plot(lambda x: np.sin(x), color=GREEN)

        self.play(Create(axes))
        self.play(Create(seno), run_time=2)
        self.play(Write(labels))
        self.wait()



class SenoConFase(Scene):
    def construct(self):
        # Ejes
        axes = Axes(
            x_range=[-2*np.pi, 2*np.pi, np.pi/2],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={
                "color": BLUE,
                "include_numbers": False,
            },
            tips=False,
        )

        # Etiquetas en π
        axes.get_x_axis().add_labels({
            -2*np.pi: MathTex(r"-2\pi"),
            -np.pi: MathTex(r"-\pi"),
            0: MathTex("0"),
            np.pi: MathTex(r"\pi"),
            2*np.pi: MathTex(r"2\pi"),
        })

        labels = axes.get_axis_labels(
            MathTex(r"x", color=RED),
            MathTex(r"\sin(x+\phi)", color=RED)
        )

        # Parámetro de fase
        phi = ValueTracker(0)

        # Seno animado
        seno = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x + phi.get_value()),
                color=GREEN
            )
        )

        self.play(Create(axes), Write(labels))
        self.add(seno)

        # Animación de la fase
        self.play(
            phi.animate.set_value(2 * np.pi),
            run_time=6,
            rate_func=linear
        )

        self.wait()





class OndaViajera(Scene):
    def construct(self):
        # Parámetros físicos
        A = 1          # amplitud
        k = 1          # número de onda
        omega = 1      # frecuencia angular

        # Ejes
        axes = Axes(
            x_range=[-2*np.pi, 2*np.pi, np.pi/2],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={
                "color": BLUE,
                "include_numbers": False,
            },
            tips=False,
        )

        # Etiquetas en π
        axes.get_x_axis().add_labels({
            -2*np.pi: MathTex(r"-2\pi"),
            -np.pi: MathTex(r"-\pi"),
            0: MathTex("0"),
            np.pi: MathTex(r"\pi"),
            2*np.pi: MathTex(r"2\pi"),
        })

        labels = axes.get_axis_labels(
            MathTex("x", color=RED),
            MathTex("y", color=RED)
        )

        # Tiempo
        t = ValueTracker(0)

        # Onda viajera
        onda = always_redraw(
            lambda: axes.plot(
                lambda x: A * np.sin(k * x - omega * t.get_value()),
                color=GREEN
            )
        )

        self.play(Create(axes), Write(labels))
        self.add(onda)

        # Animación temporal
        self.play(
            t.animate.set_value(4 * np.pi),
            run_time=8,
            rate_func=linear
        )

        self.wait()


class SuperposicionOndas(Scene):
    def construct(self):
        # Parámetros físicos
        A = 1
        k = 1
        omega = 1

        # Ejes
        axes = Axes(
            x_range=[-2*np.pi, 2*np.pi, np.pi/2],
            y_range=[-2.5, 2.5, 0.5],
            axis_config={
                "color": BLUE,
                "include_numbers": False,
            },
            tips=False,
        )

        # Etiquetas en π
        axes.get_x_axis().add_labels({
            -2*np.pi: MathTex(r"-2\pi"),
            -np.pi: MathTex(r"-\pi"),
            0: MathTex("0"),
            np.pi: MathTex(r"\pi"),
            2*np.pi: MathTex(r"2\pi"),
        })

        labels = axes.get_axis_labels(
            MathTex("x", color=RED),
            MathTex("y", color=RED)
        )

        # Tiempo
        t = ValueTracker(0)

        # Ondas viajeras
        onda_derecha = always_redraw(
            lambda: axes.plot(
                lambda x: A * np.sin(k*x - omega*t.get_value()),
                color=GREEN
            )
        )

        onda_izquierda = always_redraw(
            lambda: axes.plot(
                lambda x: A * np.sin(k*x + omega*t.get_value()),
                color=ORANGE
            )
        )

        # Superposición
        superposicion = always_redraw(
            lambda: axes.plot(
                lambda x: 2*A * np.sin(k*x) * np.cos(omega*t.get_value()),
                color=YELLOW
            )
        )

        self.play(Create(axes), Write(labels))
        self.add(onda_derecha, onda_izquierda, superposicion)

        self.play(
            t.animate.set_value(4*np.pi),
            run_time=8,
            rate_func=linear
        )

        self.wait()




class OndaConNodos(Scene):
    def construct(self):
        # Parámetros físicos
        A = 1
        k = 1
        omega = 1

        # Ejes
        axes = Axes(
            x_range=[-2*np.pi, 2*np.pi, np.pi/2],
            y_range=[-2.5, 2.5, 0.5],
            axis_config={
                "color": BLUE,
                "include_numbers": False,
            },
            tips=False,
        )

        axes.get_x_axis().add_labels({
            -2*np.pi: MathTex(r"-2\pi"),
            -np.pi: MathTex(r"-\pi"),
            0: MathTex("0"),
            np.pi: MathTex(r"\pi"),
            2*np.pi: MathTex(r"2\pi"),
        })

        labels = axes.get_axis_labels(
            MathTex("x", color=RED),
            MathTex("y", color=RED)
        )

        # Tiempo
        t = ValueTracker(0)

        # Onda estacionaria
        onda = always_redraw(
            lambda: axes.plot(
                lambda x: 2*A*np.sin(k*x)*np.cos(omega*t.get_value()),
                color=YELLOW
            )
        )

        # ===== NODOS AUTOMÁTICOS =====
        # x_n = n*pi/k dentro del rango
        n_vals = np.arange(-2, 3)   # ajusta si cambias el rango
        nodos = VGroup(*[
            Dot(
                axes.coords_to_point(n*np.pi/k, 0),
                color=RED,
                radius=0.06
            )
            for n in n_vals
        ])

        # Etiqueta opcional
        texto_nodos = MathTex(r"\text{Nodos}", color=RED).to_corner(UR)

        self.play(Create(axes), Write(labels))
        self.add(onda)
        self.play(FadeIn(nodos), Write(texto_nodos))

        self.play(
            t.animate.set_value(4*np.pi),
            run_time=8,
            rate_func=linear
        )

        self.wait()