from manim import *
import numpy as np

class SpacetimeDeformation(ThreeDScene):
    def construct(self):
        # Configurar la cámara en perspectiva inclinada
        self.set_camera_orientation(phi=75 * DEGREES, theta=-55 * DEGREES, distance=9)
        
        # Parámetros
        r_V = 2.5  # Radio de Schwarzschild (rojo)
        r_T = 4.5  # Radio exterior (amarillo)
        grid_size = 15  # Aumentado para efecto infinito
        
        # MEJORA 1: Crear grilla que se pierde en el horizonte con gradiente de opacidad
        def create_flat_grid():
            lines = VGroup()
            for i in np.linspace(-grid_size, grid_size, 40):  # Más líneas
                # Calcular opacidad basada en distancia del centro
                dist_from_center = abs(i) / grid_size
                opacity = 1.0 - (dist_from_center ** 1.5) * 0.7  # Gradiente suave
                
                line1 = Line3D(
                    start=[i, -grid_size, 0],
                    end=[i, grid_size, 0],
                    color=BLUE_D,
                    stroke_width=1.5,
                    stroke_opacity=opacity
                )
                line2 = Line3D(
                    start=[-grid_size, i, 0],
                    end=[grid_size, i, 0],
                    color=BLUE_D,
                    stroke_width=1.5,
                    stroke_opacity=opacity
                )
                lines.add(line1, line2)
            return lines
        
        grid = create_flat_grid()
        
        # MEJORA 2: Círculos más gruesos y brillantes
        def create_circle_in_plane(radius, color):
            points = []
            num_points = 120
            for i in range(num_points + 1):
                angle = i * TAU / num_points
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                z = 0
                points.append([x, y, z])
            circle = VMobject(color=color, stroke_width=6)  # Más grueso
            circle.set_points_as_corners(points)
            circle.set_stroke(opacity=1.0)
            return circle
        
        circle_rV = create_circle_in_plane(r_V, RED)
        circle_rT = create_circle_in_plane(r_T, YELLOW)
        
        # MEJORA 3: Labels más grandes y visibles
        label_rV = MathTex("r_V", color=RED, font_size=48).move_to([r_V + 0.7, 0.5, 0])
        label_rT = MathTex("r_T", color=YELLOW, font_size=48).move_to([r_T + 0.7, 0.8, 0])
        
        # MEJORA 4: Puntos más grandes y brillantes
        center_dot = Dot3D(point=[0, 0, 0], color=GREEN, radius=0.25)
        center_dot.set_glow_factor(1.5)
        
        # FASE 1: Mostrar estado inicial
        self.play(Create(grid), run_time=2.5)
        self.play(
            Create(circle_rT),
            Create(circle_rV),
            Write(label_rT),
            Write(label_rV),
            run_time=2
        )
        self.play(FadeIn(center_dot, scale=0.3), run_time=0.5)
        self.wait(1)
        
        # FASE 2: Mostrar puntos en las circunferencias y línea conectora
        angle_ref = 180 * DEGREES
        
        # MEJORA 5: Puntos más grandes en las circunferencias
        dot_rV = Dot3D(
            point=[r_V * np.cos(angle_ref), r_V * np.sin(angle_ref), 0],
            color=RED,
            radius=0.18
        )
        dot_rV.set_glow_factor(1.2)
        
        dot_rT = Dot3D(
            point=[r_T * np.cos(angle_ref), r_T * np.sin(angle_ref), 0],
            color=YELLOW,
            radius=0.18
        )
        dot_rT.set_glow_factor(1.2)
        
        # MEJORA 6: Línea conectora más gruesa
        connector_line = Line3D(
            start=dot_rV.get_center(),
            end=dot_rT.get_center(),
            color=WHITE,
            stroke_width=5
        )
        
        # Label de distancia más grande
        distance_label = MathTex("d", color=WHITE, font_size=50).move_to([-4.0, 0.3, 0])
        
        # Mostrar puntos y línea conectora con énfasis
        self.play(
            FadeIn(dot_rV, scale=0.3),
            FadeIn(dot_rT, scale=0.3),
            Create(connector_line),
            Write(distance_label),
            run_time=1.5
        )
        self.wait(1)
        
        # FASE 3: Rotación suave
        self.move_camera(theta=-410 * DEGREES, run_time=3, rate_func=smooth)
        self.wait(0.5)
        
        # Quitar las marcas de distancia
        self.play(
            FadeOut(connector_line),
            FadeOut(distance_label),
            run_time=0.5
        )
        self.wait(0.3)
        
        # MEJORA 7: Función de deformación suave y gradual
        def deformation_function(r, depth_factor):
            """
            Función que crea una deformación tipo agujero negro
            que crece gradualmente desde 0
            """
            if r >= r_V:
                return 0
            elif r < 0.15:
                # Limitar la divergencia en el centro
                return -depth_factor * 7.0
            else:
                # Función suave que diverge gradualmente
                normalized = r / r_V
                # Usar función que comienza en 0 y crece suavemente
                z = -depth_factor * 6.0 * (1 - normalized**2)**1.5 / (normalized**0.7 + 0.15)
                return z
        
        # FASE 4: Deformación gradual en MÚLTIPLES ETAPAS suaves
        def create_deformed_grid(depth_factor=0.0):
            """Crea grilla con deformación y gradiente de opacidad"""
            lines = VGroup()
            for i in np.linspace(-grid_size, grid_size, 40):
                points1 = []
                points2 = []
                
                # Calcular opacidad para el horizonte
                dist_from_center_i = abs(i) / grid_size
                opacity_i = 1.0 - (dist_from_center_i ** 1.5) * 0.7
                
                for j in np.linspace(-grid_size, grid_size, 80):
                    # Líneas en dirección x
                    r = np.sqrt(i**2 + j**2)
                    z = deformation_function(r, depth_factor)
                    points1.append([i, j, z])
                    
                    # Líneas en dirección y
                    r = np.sqrt(j**2 + i**2)
                    z = deformation_function(r, depth_factor)
                    points2.append([j, i, z])
                
                line1 = VMobject(color=BLUE_D, stroke_width=1.5)
                line1.set_points_as_corners(points1)
                line1.set_stroke(opacity=opacity_i)
                
                line2 = VMobject(color=BLUE_D, stroke_width=1.5)
                line2.set_points_as_corners(points2)
                line2.set_stroke(opacity=opacity_i)
                
                lines.add(line1, line2)
            return lines
        
        def create_deformed_circle(radius, color, depth_factor=0.0):
            """Crea un círculo que se deforma junto con el espacio-tiempo"""
            points = []
            num_points = 120
            for i in range(num_points + 1):
                angle = i * TAU / num_points
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                r = radius
                
                z = deformation_function(r, depth_factor)
                points.append([x, y, z])
            
            circle = VMobject(color=color, stroke_width=6)
            circle.set_points_as_corners(points)
            circle.set_stroke(opacity=1.0)
            return circle
        
        # MEJORA 8: Deformación en 6 etapas muy suaves para que se vea el crecimiento
        stages = [0.15, 0.3, 0.45, 0.6, 0.8, 1.0]
        
        for stage_num, depth in enumerate(stages):
            deformed_grid = create_deformed_grid(depth_factor=depth)
            deformed_circle_rV = create_deformed_circle(r_V, RED, depth_factor=depth)
            deformed_circle_rT = create_deformed_circle(r_T, YELLOW, depth_factor=depth)
            
            z_green = deformation_function(0.0, depth)
            z_dot_rV = deformation_function(r_V, depth)
            
            # Primera etapa más lenta, últimas más rápidas
            duration = 2.5 if stage_num < 2 else 2.0 if stage_num < 4 else 1.8
            
            self.play(
                Transform(grid, deformed_grid),
                Transform(circle_rV, deformed_circle_rV),
                Transform(circle_rT, deformed_circle_rT),
                center_dot.animate.move_to([0, 0, z_green]),
                dot_rV.animate.move_to([
                    r_V * np.cos(angle_ref),
                    r_V * np.sin(angle_ref),
                    z_dot_rV
                ]),
                run_time=duration,
                rate_func=smooth
            )
            
            # Pausa más corta entre etapas
            if stage_num < len(stages) - 1:
                self.wait(0.3)
        
        self.wait(1)
        
        # Fade out de los puntos
        self.play(
            FadeOut(dot_rV),
            FadeOut(dot_rT),
            run_time=0.5
        )
        
        # Rotación final para apreciar la geometría
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(7)
        self.stop_ambient_camera_rotation()
        self.wait(2)