# Geodésicas Tipo Tiempo en el Espacio-Tiempo de Schwarzschild

## Introducción Matemática

Las ecuaciones que describen las geodésicas tipo tiempo en el espacio-tiempo de Schwarzschild se pueden expresar en términos de parámetros orbitales. Para órbitas ligadas, tenemos:

$$ \left\{\begin{matrix}
 Afelio &  u=(1-e) / l , \quad \chi=\pi\\
 Perihelio&  u=(1+e) / l, \quad \chi=0 \\
\end{matrix}\right. $$




Donde:
- $u = M/r$ (coordenada radial adimensional)
- $e$ es la excentricidad orbital
- $l$ es el parámetro angular
- $χ$ es una variable angular auxiliar

La solución exacta involucra la **integral elíptica de primera especie**:



$$F(\psi, k)=\int_0^\psi \frac{\mathrm{d} \gamma}{\sqrt{ }\left(1-k^2 \sin ^2 \gamma\right)}$$


La coordenada azimutal $φ$ se expresa como:

$$\varphi=\frac{2}{(1-6 \mu+2 \mu e)^{1 / 2}} F\left(\frac{1}{2} \pi-\frac{1}{2} \chi, k\right)$$




## Código de Animación con Manim

```python
from manim import *
import numpy as np
from scipy.special import ellipkinc


class SchwarzschildGeodesicsPresentation(Scene):
    """Presentación completa de las tres geodésicas de Schwarzschild"""
    
    def construct(self):
        # Configurar fondo gris oscuro
        self.camera.background_color = "#1a1a1a"
        
        # ===== TÍTULO INICIAL =====
        main_title = Text(
            "Geodésicas Tipo Tiempo\nen Espacio-Tiempo de Schwarzschild",
            font_size=48,
            color=WHITE
        )
        self.play(Write(main_title))
        self.wait(3)
        self.play(FadeOut(main_title))
        self.wait(0.5)
        
        # ===== AGUJERO NEGRO CON SU TÍTULO =====
        M = 3/14
        schwarzschild_radius = 2 * M
        
        # Crear ejes temporales solo para calcular la posición
        temp_axes = Axes(
            x_range=[-30, 30, 5],
            y_range=[-30, 30, 5],
            x_length=6,
            y_length=6,
        )
        
        black_hole_radius = temp_axes.x_axis.point_to_number(
            temp_axes.c2p(schwarzschild_radius, 0)
        ) - temp_axes.x_axis.point_to_number(temp_axes.c2p(0, 0))
        
        # Agujero negro
        black_hole = Circle(
            radius=abs(black_hole_radius),
            color=BLACK,
            fill_opacity=1,
            stroke_width=2,
            stroke_color=WHITE
        )
        
        event_horizon = Circle(
            radius=abs(black_hole_radius) * 1.15,
            color=ORANGE,
            fill_opacity=0.3,
            stroke_width=3,
            stroke_color=YELLOW,
            stroke_opacity=0.6
        )
        
        accretion_disk = Circle(
            radius=abs(black_hole_radius) * 2.5,
            color=GRAY,
            fill_opacity=0.1,
            stroke_width=1,
            stroke_color=GRAY_B,
            stroke_opacity=0.3
        )
        
        bh_title = Text(
            "Agujero Negro de Schwarzschild",
            font_size=36,
            color=WHITE
        ).next_to(black_hole, DOWN, buff=0.8)
        
        # Animar aparición del agujero negro
        self.play(FadeIn(accretion_disk), run_time=0.5)
        self.play(
            GrowFromCenter(event_horizon),
            GrowFromCenter(black_hole),
            run_time=1.5
        )
        self.play(Write(bh_title), run_time=1)
        self.wait(2)
        
        # Quitar el título del agujero negro
        self.play(FadeOut(bh_title), run_time=0.5)
        self.wait(0.5)
        
        # ===== LOOP PARA LAS TRES GEODÉSICAS =====
        geodesics_data = [
            ("A", 0.5, 11, 3/14, BLUE, 30),
            ("B", 0.5, 7.5, 3/14, ORANGE, 20),
            ("C", 0.5, 3, 3/14, GREEN, 8)
        ]
        
        axes = None
        x_label = None
        y_label = None
        
        for i, (case, e, l, M, color, range_val) in enumerate(geodesics_data):
            # ===== AGREGAR EJES Y PARÁMETROS (solo la primera vez) =====
            if i == 0:
                axes = Axes(
                    x_range=[-range_val, range_val, 5],
                    y_range=[-range_val, range_val, 5],
                    x_length=6,
                    y_length=6,
                    axis_config={
                        "color": GRAY_C,
                        "include_numbers": False,
                        "include_ticks": True,
                        "tick_size": 0.05,
                    }
                )
                
                x_label = axes.get_x_axis_label("x/M", direction=DOWN, buff=0.3)
                y_label = axes.get_y_axis_label("y/M", direction=LEFT, buff=0.3)
                x_label.set_color(GRAY_A)
                y_label.set_color(GRAY_A)
                
                self.play(
                    Create(axes),
                    Write(x_label),
                    Write(y_label),
                    run_time=1.5
                )
                self.wait(0.5)
            else:
                # Actualizar ejes si cambia el rango
                if range_val != geodesics_data[i-1][5]:
                    self.play(FadeOut(axes), FadeOut(x_label), FadeOut(y_label))
                    
                    axes = Axes(
                        x_range=[-range_val, range_val, 5],
                        y_range=[-range_val, range_val, 5],
                        x_length=6,
                        y_length=6,
                        axis_config={
                            "color": GRAY_C,
                            "include_numbers": False,
                            "include_ticks": True,
                            "tick_size": 0.05,
                        }
                    )
                    
                    x_label = axes.get_x_axis_label("x/M", direction=DOWN, buff=0.3)
                    y_label = axes.get_y_axis_label("y/M", direction=LEFT, buff=0.3)
                    x_label.set_color(GRAY_A)
                    y_label.set_color(GRAY_A)
                    
                    self.play(
                        Create(axes),
                        Write(x_label),
                        Write(y_label),
                        run_time=1
                    )
            
            # ===== MOSTRAR PARÁMETROS DE LA GEODÉSICA =====
            title = Text(
                f"Caso {case}",
                font_size=40,
                color=color
            ).to_corner(UL)
            
            params = MathTex(
                f"e={e}, \\; l={l}, \\; M={M:.4f}",
                font_size=32,
                color=WHITE
            ).next_to(title, DOWN, aligned_edge=LEFT)
            
            rev_text = Text(
                "Rev: {3f}",
                font_size=24,
                color=GRAY_B
            ).to_corner(UR)
            
            range_text = Text(
                f"Rango: ±{range_val}M",
                font_size=20,
                color=GRAY_A
            ).to_corner(DL)
            
            self.play(
                Write(title),
                Write(params),
                Write(rev_text),
                Write(range_text),
                run_time=1
            )
            self.wait(0.5)
            
            # ===== GENERAR Y ANIMAR LA GEODÉSICA =====
            mu = M / l
            
            # Generar puntos
            chi_values = np.linspace(0, 3 * 2 * np.pi, 3 * 300)
            points = []
            chi_list = []
            
            for chi in chi_values:
                denominator = 1 - 6*mu + 2*mu*e
                if denominator <= 0:
                    continue
                
                k_squared = (3*mu*(1-e)) / denominator
                if k_squared < 0 or k_squared > 1:
                    continue
                    
                k = np.sqrt(k_squared)
                psi = np.pi/2 - chi/2
                F_value = ellipkinc(psi, k_squared)
                phi = 2 * F_value / np.sqrt(denominator)
                r = M / (mu * (1 + e * np.cos(chi)))
                
                x = r * np.cos(phi)
                y = r * np.sin(phi)
                
                points.append([x, y, 0])
                chi_list.append(chi)
            
            scaled_points = [axes.c2p(p[0], p[1]) for p in points]
            
            # Crear trayectoria y partícula
            traced_path = VMobject(color=color, stroke_width=3)
            traced_path.set_points_as_corners([scaled_points[0], scaled_points[0]])
            
            dot = Dot(color=color, radius=0.08)
            dot.move_to(scaled_points[0])
            
            # Encontrar perihelios y afelios
            chi_array = np.array(chi_list)
            perihelion_indices = []
            aphelion_indices = []
            
            for j in range(4):
                target_chi = j * 2 * np.pi
                idx = np.argmin(np.abs(chi_array - target_chi))
                perihelion_indices.append(idx)
            
            for j in range(3):
                target_chi = (2*j + 1) * np.pi
                idx = np.argmin(np.abs(chi_array - target_chi))
                aphelion_indices.append(idx)
            
            perihelion_dots = VGroup()
            aphelion_dots = VGroup()
            perihelion_shown = [False] * len(perihelion_indices)
            aphelion_shown = [False] * len(aphelion_indices)
            first_perihelion = True
            first_aphelion = True
            
            perihelion_label = Text("Perihelio", font_size=20, color=RED)
            aphelion_label = Text("Afelio", font_size=20, color=YELLOW)
            
            self.add(traced_path, dot)
            
            # Animar la órbita con velocidad variable
            # Crear una función de rate personalizada basada en la distancia radial
            def custom_rate_func(t):
                """
                Función de velocidad personalizada:
                - Más rápido cerca del perihelio (punto más cercano)
                - Más lento cerca del afelio (punto más lejano)
                """
                idx = int(t * (len(points) - 1))
                if idx >= len(points):
                    idx = len(points) - 1
                
                # Calcular la distancia radial en cada punto
                x, y, _ = points[idx]
                r = np.sqrt(x**2 + y**2)
                
                # Normalizar: velocidad inversamente proporcional a r
                # Cuando r es pequeño (cerca del perihelio), velocidad es alta
                # Cuando r es grande (cerca del afelio), velocidad es baja
                
                # Calcular r_min y r_max para normalizar
                r_values = [np.sqrt(p[0]**2 + p[1]**2) for p in points]
                r_min = min(r_values)
                r_max = max(r_values)
                
                # Velocidad proporcional a 1/r (conservación del momento angular)
                # Normalizamos para que el promedio sea aproximadamente lineal
                speed_factor = (r_max / r) if r > 0 else 1.0
                
                # Integrar la velocidad para obtener la posición
                # Esto requiere pre-calcular la integral acumulativa
                return t  # Placeholder, se corregirá abajo
            
            # Pre-calcular los tiempos basados en velocidad física
            r_values = [np.sqrt(p[0]**2 + p[1]**2) for p in points]
            r_min = min(r_values)
            r_max = max(r_values)
            
            # Velocidad en cada punto (proporcional a 1/r por conservación de momento angular)
            velocities = [r_max / r if r > 0 else 1.0 for r in r_values]
            
            # Calcular dt basado en velocidad (dt más pequeño donde velocidad es mayor)
            dt_values = [1.0 / v for v in velocities]
            
            # Tiempo acumulado
            cumulative_time = np.cumsum(dt_values)
            total_time = cumulative_time[-1]
            
            # Normalizar para que vaya de 0 a 1
            normalized_times = cumulative_time / total_time
            
            # Crear función de mapeo de alpha a índice
            def alpha_to_index(alpha):
                """Mapea alpha (0 a 1) al índice correcto considerando la velocidad variable"""
                if alpha <= 0:
                    return 0
                if alpha >= 1:
                    return len(scaled_points) - 1
                
                # Buscar el índice correspondiente en normalized_times
                idx = np.searchsorted(normalized_times, alpha)
                return min(idx, len(scaled_points) - 1)
            
            # Funciones de actualización con velocidad variable
            def update_path_variable(mob, alpha):
                idx = alpha_to_index(alpha)
                if idx < len(scaled_points):
                    current_points = scaled_points[:idx+1]
                    if len(current_points) > 1:
                        mob.set_points_as_corners(current_points)
            
            def update_dot_variable(mob, alpha):
                nonlocal first_perihelion, first_aphelion
                idx = alpha_to_index(alpha)
                if idx < len(scaled_points):
                    mob.move_to(scaled_points[idx])
                    
                    for j, p_idx in enumerate(perihelion_indices):
                        if not perihelion_shown[j] and idx >= p_idx:
                            perihelion_shown[j] = True
                            new_dot = Dot(point=scaled_points[p_idx], color=RED, radius=0.1)
                            perihelion_dots.add(new_dot)
                            self.add(new_dot)
                            
                            if first_perihelion:
                                first_perihelion = False
                                perihelion_label.next_to(new_dot, DOWN, buff=0.2)
                                self.add(perihelion_label)
                    
                    for j, a_idx in enumerate(aphelion_indices):
                        if not aphelion_shown[j] and idx >= a_idx:
                            aphelion_shown[j] = True
                            new_dot = Dot(point=scaled_points[a_idx], color=YELLOW, radius=0.1)
                            aphelion_dots.add(new_dot)
                            self.add(new_dot)
                            
                            if first_aphelion:
                                first_aphelion = False
                                aphelion_label.next_to(new_dot, UP, buff=0.2)
                                self.add(aphelion_label)
            
            self.play(
                UpdateFromAlphaFunc(traced_path, update_path_variable),
                UpdateFromAlphaFunc(dot, update_dot_variable),
                run_time=8,
                rate_func=linear
            )
            
            self.wait(1)
            
            # Limpiar para la siguiente geodésica (excepto el agujero negro y ejes)
            if i < len(geodesics_data) - 1:
                self.play(
                    FadeOut(traced_path),
                    FadeOut(dot),
                    FadeOut(perihelion_dots),
                    FadeOut(aphelion_dots),
                    FadeOut(perihelion_label),
                    FadeOut(aphelion_label),
                    FadeOut(title),
                    FadeOut(params),
                    FadeOut(rev_text),
                    FadeOut(range_text),
                    run_time=0.5
                )
                self.wait(0.3)
        
        # Final
        self.wait(2)

```
<video controls autoplay muted loop poster="thumbnail.jpg">
  <source src="vidios_gifs/SchwarzschildGeodesicsPresentation.mp4" type="video/mp4">
</video>

        

