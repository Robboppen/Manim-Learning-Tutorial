from manim import *
import numpy as np

class CampoRotacional(Scene):
    def construct(self):
        
        # -------------------- TÍTULO --------------------
        title = MathTex(r"\text{rot}\,\vec{F}", font_size=80, color=YELLOW).move_to(ORIGIN)
        
        # -------------------- CÍRCULOS CONCÉNTRICOS --------------------
        circles = VGroup()
        radii = [0.8, 1.6, 2.4, 3.2, 4.0, 4.8]
        
        for r in radii:
            circle = Circle(radius=r, color=GREY, stroke_width=1, stroke_opacity=0.3)
            circles.add(circle)
        
        # -------------------- FLECHAS ESTÁTICAS --------------------
        static_arrows = VGroup()
        
        # Crear flechas en cuadrícula
        x_range = np.arange(-6, 6.5, 0.4)
        y_range = np.arange(-3.5, 4, 0.4)
        
        for x in x_range:
            for y in y_range:
                position = np.array([x, y, 0])
                distance = np.linalg.norm(position)
                
                if distance > 0.5:  # Evitar el centro
                    # Campo rotacional: perpendicular al radio
                    direction = np.array([-y, x, 0])
                    direction = direction / np.linalg.norm(direction)
                    
                    # Longitud de la flecha constante
                    arrow_length = 0.25
                    end_point = position + direction * arrow_length
                    
                    arrow = Arrow(
                        start=position,
                        end=end_point,
                        color=RED,
                        buff=0,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.25,
                        max_stroke_width_to_length_ratio=5
                    )
                    
                    static_arrows.add(arrow)
        
        # -------------------- FLECHAS GRANDES ROTATORIAS --------------------
        rotating_arrows = VGroup()
        
        # Crear flechas más largas en posiciones específicas sobre los círculos
        num_arrows_per_circle = [6, 8, 10, 12, 14, 16]
        
        for i, r in enumerate(radii):
            n_arrows = num_arrows_per_circle[i]
            for j in range(n_arrows):
                angle = TAU * j / n_arrows
                position = np.array([r * np.cos(angle), r * np.sin(angle), 0])
                
                # Dirección tangencial (perpendicular al radio)
                direction = np.array([-np.sin(angle), np.cos(angle), 0])
                
                # Flecha más larga
                arrow_length = 0.5
                end_point = position + direction * arrow_length
                
                arrow = Arrow(
                    start=position,
                    end=end_point,
                    color=YELLOW,
                    buff=0,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.2,
                    max_stroke_width_to_length_ratio=6
                )
                
                rotating_arrows.add(arrow)
        
        # -------------------- ANIMACIÓN --------------------
        self.camera.background_color = BLACK
        
        # Mostrar título
        self.play(Write(title))
        self.wait(1)
        
        # Fade out título y mostrar círculos
        self.play(
            FadeOut(title),
            LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.1),
            run_time=2
        )
        
        # Mostrar flechas estáticas
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in static_arrows], lag_ratio=0.003),
            run_time=3
        )
        self.wait(0.5)
        
        # Mostrar título nuevamente en el centro
        title_center = MathTex(r"\text{rot}\,\vec{F}", font_size=80, color=YELLOW).move_to(ORIGIN)
        self.play(Write(title_center))
        
        # Mostrar flechas rotatorias amarillas
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in rotating_arrows], lag_ratio=0.02),
            run_time=2
        )
        self.wait(1)
        
        # Rotar las flechas amarillas
        self.play(
            Rotate(rotating_arrows, angle=TAU, about_point=ORIGIN, rate_func=linear),
            run_time=4
        )
        
        # Continuar rotando
        self.play(
            Rotate(rotating_arrows, angle=TAU, about_point=ORIGIN, rate_func=linear),
            run_time=4
        )
        
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(static_arrows),
            FadeOut(rotating_arrows),
            FadeOut(circles),
            FadeOut(title_center)
        )


class CampoRotacionalContinuo(Scene):
    def construct(self):
        
        # -------------------- TÍTULO --------------------
        title = MathTex(r"\text{rot}\,\vec{F}", font_size=80, color=YELLOW).move_to(ORIGIN)
        
        # -------------------- CÍRCULOS CONCÉNTRICOS --------------------
        circles = VGroup()
        radii = [0.8, 1.6, 2.4, 3.2, 4.0, 4.8]
        
        for r in radii:
            circle = Circle(radius=r, color=GREY, stroke_width=1, stroke_opacity=0.3)
            circles.add(circle)
        
        # -------------------- FLECHAS ESTÁTICAS --------------------
        static_arrows = VGroup()
        
        x_range = np.arange(-6, 6.5, 0.4)
        y_range = np.arange(-3.5, 4, 0.4)
        
        for x in x_range:
            for y in y_range:
                position = np.array([x, y, 0])
                distance = np.linalg.norm(position)
                
                if distance > 0.5:
                    direction = np.array([-y, x, 0])
                    direction = direction / np.linalg.norm(direction)
                    
                    arrow_length = 0.25
                    end_point = position + direction * arrow_length
                    
                    arrow = Arrow(
                        start=position,
                        end=end_point,
                        color=RED,
                        buff=0,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.25,
                        max_stroke_width_to_length_ratio=5
                    )
                    
                    static_arrows.add(arrow)
        
        # -------------------- FLECHAS GRANDES ROTATORIAS --------------------
        rotating_arrows = VGroup()
        
        num_arrows_per_circle = [6, 8, 10, 12, 14, 16]
        
        for i, r in enumerate(radii):
            n_arrows = num_arrows_per_circle[i]
            for j in range(n_arrows):
                angle = TAU * j / n_arrows
                position = np.array([r * np.cos(angle), r * np.sin(angle), 0])
                direction = np.array([-np.sin(angle), np.cos(angle), 0])
                
                arrow_length = 0.5
                end_point = position + direction * arrow_length
                
                arrow = Arrow(
                    start=position,
                    end=end_point,
                    color=YELLOW,
                    buff=0,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.2,
                    max_stroke_width_to_length_ratio=6
                )
                
                rotating_arrows.add(arrow)
        
        # -------------------- ANIMACIÓN --------------------
        self.camera.background_color = BLACK
        
        self.play(Write(title))
        self.wait(1)
        
        self.play(
            FadeOut(title),
            LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.1),
            run_time=2
        )
        
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in static_arrows], lag_ratio=0.003),
            run_time=3
        )
        self.wait(0.5)
        
        title_center = MathTex(r"\text{rot}\,\vec{F}", font_size=80, color=YELLOW).move_to(ORIGIN)
        self.play(Write(title_center))
        
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in rotating_arrows], lag_ratio=0.02),
            run_time=2
        )
        self.wait(1)
        
        # Rotación continua con updater
        def rotate_arrows(mob, dt):
            mob.rotate(dt * 0.5, about_point=ORIGIN)
        
        rotating_arrows.add_updater(rotate_arrows)
        self.wait(10)  # Rota continuamente por 10 segundos
        rotating_arrows.remove_updater(rotate_arrows)
        
        self.wait(1)
        
        self.play(
            FadeOut(static_arrows),
            FadeOut(rotating_arrows),
            FadeOut(circles),
            FadeOut(title_center)
        )


class CurlField(Scene):
    def construct(self):
        
        # -------------------- TÍTULO --------------------
        title = Text("Curl", font_size=100, color=WHITE, weight=BOLD).move_to(ORIGIN)
        
        # -------------------- CÍRCULOS CONCÉNTRICOS (LÍNEAS ROTATORIAS) --------------------
        circles = VGroup()
        num_circles = 40
        max_radius = 6
        
        for i in range(num_circles):
            r = max_radius * (i + 1) / num_circles
            circle = Circle(radius=r, color=GREY, stroke_width=1.5, stroke_opacity=0.6)
            circles.add(circle)
        
        # -------------------- FLECHAS CON GRADIENTE DE COLOR --------------------
        arrows = VGroup()
        
        # Parámetros para la distribución de flechas
        num_radii = 25
        arrows_per_radius = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56]
        
        for i in range(num_radii):
            r = max_radius * (i + 1) / num_radii
            n_arrows = arrows_per_radius[min(i, len(arrows_per_radius) - 1)]
            
            for j in range(n_arrows):
                angle = TAU * j / n_arrows
                position = np.array([r * np.cos(angle), r * np.sin(angle), 0])
                
                # Dirección tangencial
                direction = np.array([-np.sin(angle), np.cos(angle), 0])
                
                # Longitud de flecha
                arrow_length = 0.15
                end_point = position + direction * arrow_length
                
                # Gradiente de color basado en el radio
                color_value = i / num_radii
                if color_value < 0.25:
                    color = interpolate_color(RED, ORANGE, color_value * 4)
                elif color_value < 0.5:
                    color = interpolate_color(ORANGE, YELLOW, (color_value - 0.25) * 4)
                elif color_value < 0.75:
                    color = interpolate_color(YELLOW, GREEN, (color_value - 0.5) * 4)
                else:
                    color = interpolate_color(GREEN, TEAL, (color_value - 0.75) * 4)
                
                arrow = Arrow(
                    start=position,
                    end=end_point,
                    color=color,
                    buff=0,
                    stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.3,
                    max_stroke_width_to_length_ratio=5
                )
                
                arrows.add(arrow)
        
        # -------------------- ANIMACIÓN --------------------
        self.camera.background_color = BLACK
        
        # Mostrar título
        self.play(Write(title))
        self.wait(1)
        
        # Fade out título
        self.play(FadeOut(title))
        self.wait(0.3)
        
        # Mostrar círculos y flechas simultáneamente
        self.play(
            LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.03),
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.002),
            run_time=3
        )
        self.wait(0.5)
        
        # Mostrar título en el centro
        title_center = Text("Curl", font_size=100, color=WHITE, weight=BOLD).move_to(ORIGIN)
        self.play(Write(title_center))
        self.wait(1)
        
        # -------------------- ROTACIÓN CON IMPULSOS --------------------
        # Impulso 1: Rotación rápida
        self.play(
            Rotate(circles, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            run_time=0.8
        )
        # Reposo
        self.wait(0.4)
        
        # Impulso 2
        self.play(
            Rotate(circles, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            run_time=0.8
        )
        self.wait(0.4)
        
        # Impulso 3
        self.play(
            Rotate(circles, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            run_time=0.8
        )
        self.wait(0.4)
        
        # Impulso 4
        self.play(
            Rotate(circles, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            run_time=0.8
        )
        self.wait(0.5)
        
        # Impulso 5 - más largo
        self.play(
            Rotate(circles, angle=PI, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI, about_point=ORIGIN, rate_func=rush_into),
            run_time=1.2
        )
        self.wait(0.6)
        
        # Impulso 6
        self.play(
            Rotate(circles, angle=PI, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI, about_point=ORIGIN, rate_func=rush_into),
            run_time=1.2
        )
        self.wait(0.6)
        
        # Rotación continua final
        self.play(
            Rotate(circles, angle=TAU * 2, about_point=ORIGIN, rate_func=linear),
            Rotate(arrows, angle=TAU * 2, about_point=ORIGIN, rate_func=linear),
            run_time=6
        )
        
        self.wait(1)
        
        # Fade out
        self.play(
            FadeOut(circles),
            FadeOut(arrows),
            FadeOut(title_center)
        )


class CurlFieldPulse(Scene):
    def construct(self):
        
        # -------------------- TÍTULO --------------------
        title = Text("Curl", font_size=100, color=WHITE, weight=BOLD).move_to(ORIGIN)
        
        # -------------------- CÍRCULOS CONCÉNTRICOS --------------------
        circles = VGroup()
        num_circles = 40
        max_radius = 6
        
        for i in range(num_circles):
            r = max_radius * (i + 1) / num_circles
            circle = Circle(radius=r, color=GREY, stroke_width=1.5, stroke_opacity=0.6)
            circles.add(circle)
        
        # -------------------- FLECHAS CON GRADIENTE --------------------
        arrows = VGroup()
        num_radii = 25
        arrows_per_radius = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56]
        
        for i in range(num_radii):
            r = max_radius * (i + 1) / num_radii
            n_arrows = arrows_per_radius[min(i, len(arrows_per_radius) - 1)]
            
            for j in range(n_arrows):
                angle = TAU * j / n_arrows
                position = np.array([r * np.cos(angle), r * np.sin(angle), 0])
                direction = np.array([-np.sin(angle), np.cos(angle), 0])
                
                arrow_length = 0.15
                end_point = position + direction * arrow_length
                
                color_value = i / num_radii
                if color_value < 0.25:
                    color = interpolate_color(RED, ORANGE, color_value * 4)
                elif color_value < 0.5:
                    color = interpolate_color(ORANGE, YELLOW, (color_value - 0.25) * 4)
                elif color_value < 0.75:
                    color = interpolate_color(YELLOW, GREEN, (color_value - 0.5) * 4)
                else:
                    color = interpolate_color(GREEN, TEAL, (color_value - 0.75) * 4)
                
                arrow = Arrow(
                    start=position,
                    end=end_point,
                    color=color,
                    buff=0,
                    stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.3,
                    max_stroke_width_to_length_ratio=5
                )
                
                arrows.add(arrow)
        
        # -------------------- ANIMACIÓN --------------------
        self.camera.background_color = BLACK
        
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        self.wait(0.3)
        
        self.play(
            LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.03),
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.002),
            run_time=3
        )
        self.wait(0.5)
        
        title_center = Text("Curl", font_size=100, color=WHITE, weight=BOLD).move_to(ORIGIN)
        self.play(Write(title_center))
        self.wait(1)
        
        # -------------------- IMPULSOS CON EFECTO DE ACELERACIÓN/DESACELERACIÓN --------------------
        angles = [PI/3, PI/2, 2*PI/3, PI, PI, 3*PI/2, TAU]
        times = [0.6, 0.7, 0.8, 1.0, 1.0, 1.2, 1.5]
        rests = [0.5, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2]
        
        for angle, time, rest in zip(angles, times, rests):
            # Impulso con aceleración y desaceleración
            self.play(
                Rotate(circles, angle=angle, about_point=ORIGIN, rate_func=there_and_back_with_pause),
                Rotate(arrows, angle=angle, about_point=ORIGIN, rate_func=there_and_back_with_pause),
                run_time=time
            )
            # Reposo
            self.wait(rest)
        
        self.wait(1)
        
        self.play(
            FadeOut(circles),
            FadeOut(arrows),
            FadeOut(title_center)
        )