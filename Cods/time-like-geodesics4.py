from manim import *
import numpy as np
from scipy.special import ellipkinc

class SchwarzschildGeodesic(Scene):
    """Clase base para geodésicas de Schwarzschild"""
    
    def __init__(self, e, l, M, color, **kwargs):
        super().__init__(**kwargs)
        self.e = e
        self.l = l
        self.M = M
        self.color = color
        
    def compute_phi(self, chi, mu):
        """
        Calcula φ usando la fórmula:
        φ = 2/sqrt(1-6μ+2μe) * F(π/2 - χ/2, k)
        donde F es la integral elíptica incompleta de primer tipo
        """
        denominator = 1 - 6*mu + 2*mu*self.e
        if denominator <= 0:
            return None
        
        k_squared = self.compute_k_squared(mu)
        if k_squared < 0 or k_squared > 1:
            return None
            
        k = np.sqrt(k_squared)
        psi = np.pi/2 - chi/2
        
        # F(ψ, k) es la integral elíptica incompleta
        F_value = ellipkinc(psi, k_squared)
        
        phi = 2 * F_value / np.sqrt(denominator)
        return phi
    
    def compute_k_squared(self, mu):
        """Calcula k^2 para la integral elíptica"""
        numerator = 3*mu*(1-self.e)
        denominator = 1 - 6*mu + 2*mu*self.e
        if denominator == 0:
            return None
        return numerator / denominator
    
    def compute_r(self, chi, mu):
        """Calcula r en función de χ"""
        M = self.M
        r = M / (mu * (1 + self.e * np.cos(chi)))
        return r
    
    def generate_orbit_points(self, num_revolutions=3, points_per_rev=300):
        """Genera puntos de la órbita"""
        mu = self.M / self.l
        
        chi_values = np.linspace(0, num_revolutions * 2 * np.pi, 
                                 num_revolutions * points_per_rev)
        
        points = []
        chi_list = []
        for chi in chi_values:
            phi = self.compute_phi(chi, mu)
            if phi is None:
                continue
                
            r = self.compute_r(chi, mu)
            
            # Convertir a coordenadas cartesianas
            x = r * np.cos(phi)
            y = r * np.sin(phi)
            
            points.append([x, y, 0])
            chi_list.append(chi)
        
        return points, chi_list
    
    def find_perihelion_aphelion(self, num_revolutions=3):
        """Encuentra los puntos de perihelio (χ=0, 2π, 4π...) y afelio (χ=π, 3π, 5π...)"""
        mu = self.M / self.l
        
        perihelion_points = []
        aphelion_points = []
        
        # Perihelios: χ = 0, 2π, 4π, ...
        for i in range(num_revolutions + 1):
            chi = i * 2 * np.pi
            phi = self.compute_phi(chi, mu)
            if phi is not None:
                r = self.compute_r(chi, mu)
                x = r * np.cos(phi)
                y = r * np.sin(phi)
                perihelion_points.append([x, y, 0])
        
        # Afelios: χ = π, 3π, 5π, ...
        for i in range(num_revolutions):
            chi = (2*i + 1) * np.pi
            phi = self.compute_phi(chi, mu)
            if phi is not None:
                r = self.compute_r(chi, mu)
                x = r * np.cos(phi)
                y = r * np.sin(phi)
                aphelion_points.append([x, y, 0])
        
        return perihelion_points, aphelion_points
    
    def construct(self):
        # Configurar fondo gris oscuro
        self.camera.background_color = "#1a1a1a"
        
        # Calcular μ
        mu = self.M / self.l
        
        # Título
        title = MathTex(
            f"e={self.e}, l={self.l}, M={self.M:.4f}",
            font_size=36,
            color=WHITE
        ).to_corner(UL)
        
        rev_text = Text(
            f"Rev: {{3f}}",
            font_size=24,
            color=GRAY_B
        ).to_corner(UR)
        
        # Crear ejes sin números
        range_val = 30 if self.l > 10 else (20 if self.l > 5 else 8)
        
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
        
        # Crear agujero negro en el centro
        # Radio de Schwarzschild: r_s = 2GM/c² = 2M (en unidades geométricas)
        schwarzschild_radius = 2 * self.M
        
        # Escalar el radio del agujero negro a las coordenadas de la pantalla
        black_hole_radius = axes.x_axis.point_to_number(
            axes.c2p(schwarzschild_radius, 0)
        ) - axes.x_axis.point_to_number(axes.c2p(0, 0))
        
        # Agujero negro (círculo negro con borde brillante)
        black_hole = Circle(
            radius=abs(black_hole_radius),
            color=BLACK,
            fill_opacity=1,
            stroke_width=2,
            stroke_color=WHITE
        ).move_to(axes.c2p(0, 0))
        
        # Horizonte de eventos (aura naranja/amarilla)
        event_horizon = Circle(
            radius=abs(black_hole_radius) * 1.15,
            color=ORANGE,
            fill_opacity=0.3,
            stroke_width=3,
            stroke_color=YELLOW,
            stroke_opacity=0.6
        ).move_to(axes.c2p(0, 0))
        
        # Disco de acreción (anillo gris difuso)
        accretion_disk = Circle(
            radius=abs(black_hole_radius) * 2.5,
            color=GRAY,
            fill_opacity=0.1,
            stroke_width=1,
            stroke_color=GRAY_B,
            stroke_opacity=0.3
        ).move_to(axes.c2p(0, 0))
        
        # Etiqueta del agujero negro
        bh_label = Text(
            "Agujero Negro\nSchwarzschild",
            font_size=16,
            color=GRAY_A
        ).next_to(black_hole, DOWN, buff=0.3)
        
        # Generar puntos de la órbita
        orbit_points, chi_list = self.generate_orbit_points(num_revolutions=3)
        
        if len(orbit_points) < 2:
            error_text = Text("Error: No se pueden calcular geodésicas", 
                            color=RED)
            self.play(Write(error_text))
            self.wait(2)
            return
        
        # Escalar puntos para que se ajusten a los ejes
        scaled_points = [axes.c2p(p[0], p[1]) for p in orbit_points]
        
        # Encontrar perihelios y afelios
        perihelion_points, aphelion_points = self.find_perihelion_aphelion(num_revolutions=3)
        scaled_perihelion = [axes.c2p(p[0], p[1]) for p in perihelion_points]
        scaled_aphelion = [axes.c2p(p[0], p[1]) for p in aphelion_points]
        
        # Crear la curva que se va trazando
        traced_path = VMobject(color=self.color, stroke_width=3)
        traced_path.set_points_as_corners([scaled_points[0], scaled_points[0]])
        
        # Punto que se mueve por la órbita
        dot = Dot(color=self.color, radius=0.08)
        dot.move_to(scaled_points[0])
        
        # Crear grupos para los puntos que irán apareciendo
        perihelion_dots = VGroup()
        aphelion_dots = VGroup()
        
        # Etiquetas que aparecerán la primera vez
        perihelion_label = Text("Perihelio", font_size=20, color=RED)
        aphelion_label = Text("Afelio", font_size=20, color=YELLOW)
        
        range_text = Text(
            f"Rango: ±{range_val}M",
            font_size=20,
            color=GRAY_A
        ).to_corner(DL)
        
        # Animación inicial
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            Write(title),
            Write(rev_text),
            Write(range_text)
        )
        
        # Aparecer el agujero negro con efecto dramático
        self.play(
            FadeIn(accretion_disk),
            run_time=0.5
        )
        self.play(
            GrowFromCenter(event_horizon),
            GrowFromCenter(black_hole),
            run_time=1
        )
        self.play(
            Write(bh_label),
            run_time=0.5
        )
        self.wait(0.5)
        
        self.add(traced_path, dot)
        
        # Calcular índices donde ocurren perihelios y afelios
        chi_array = np.array(chi_list)
        perihelion_indices = []
        aphelion_indices = []
        
        # Encontrar índices cercanos a χ = 0, 2π, 4π... (perihelios)
        for i in range(4):  # 0, 2π, 4π, 6π
            target_chi = i * 2 * np.pi
            idx = np.argmin(np.abs(chi_array - target_chi))
            perihelion_indices.append(idx)
        
        # Encontrar índices cercanos a χ = π, 3π, 5π... (afelios)
        for i in range(3):  # π, 3π, 5π
            target_chi = (2*i + 1) * np.pi
            idx = np.argmin(np.abs(chi_array - target_chi))
            aphelion_indices.append(idx)
        
        # Variables para controlar qué puntos ya se mostraron
        perihelion_shown = [False] * len(perihelion_indices)
        aphelion_shown = [False] * len(aphelion_indices)
        first_perihelion = True
        first_aphelion = True
        
        # Animación del trazo y movimiento con aparición de puntos
        def update_path(mob, alpha):
            idx = int(alpha * (len(scaled_points) - 1))
            if idx < len(scaled_points):
                current_points = scaled_points[:idx+1]
                if len(current_points) > 1:
                    mob.set_points_as_corners(current_points)
        
        def update_dot(mob, alpha):
            nonlocal first_perihelion, first_aphelion
            idx = int(alpha * (len(scaled_points) - 1))
            if idx < len(scaled_points):
                mob.move_to(scaled_points[idx])
                
                # Verificar si pasamos por un perihelio
                for i, p_idx in enumerate(perihelion_indices):
                    if not perihelion_shown[i] and idx >= p_idx:
                        perihelion_shown[i] = True
                        new_dot = Dot(point=scaled_points[p_idx], color=RED, radius=0.1)
                        perihelion_dots.add(new_dot)
                        self.add(new_dot)
                        
                        # Mostrar etiqueta solo la primera vez
                        if first_perihelion:
                            first_perihelion = False
                            perihelion_label.next_to(new_dot, DOWN, buff=0.2)
                            self.add(perihelion_label)
                
                # Verificar si pasamos por un afelio
                for i, a_idx in enumerate(aphelion_indices):
                    if not aphelion_shown[i] and idx >= a_idx:
                        aphelion_shown[i] = True
                        new_dot = Dot(point=scaled_points[a_idx], color=YELLOW, radius=0.1)
                        aphelion_dots.add(new_dot)
                        self.add(new_dot)
                        
                        # Mostrar etiqueta solo la primera vez
                        if first_aphelion:
                            first_aphelion = False
                            aphelion_label.next_to(new_dot, UP, buff=0.2)
                            self.add(aphelion_label)
        
        # Animar el trazo de la órbita
        self.play(
            UpdateFromAlphaFunc(traced_path, update_path),
            UpdateFromAlphaFunc(dot, update_dot),
            run_time=8,
            rate_func=linear
        )
        
        self.wait(2)


class GeodesicA(SchwarzschildGeodesic):
    """Geodésica con e=1/2, l=11, M=3/14"""
    def __init__(self, **kwargs):
        super().__init__(e=0.5, l=11, M=3/14, color=BLUE, **kwargs)


class GeodesicB(SchwarzschildGeodesic):
    """Geodésica con e=1/2, l=7.5, M=3/14"""
    def __init__(self, **kwargs):
        super().__init__(e=0.5, l=7.5, M=3/14, color=ORANGE, **kwargs)


class GeodesicC(SchwarzschildGeodesic):
    """Geodésica con e=1/2, l=3, M=3/14"""
    def __init__(self, **kwargs):
        super().__init__(e=0.5, l=3, M=3/14, color=GREEN, **kwargs)


class AllGeodesics(Scene):
    """Muestra las tres geodésicas en secuencia de forma continua"""
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
            
            # Funciones de actualización
            def update_path(mob, alpha):
                idx = int(alpha * (len(scaled_points) - 1))
                if idx < len(scaled_points):
                    current_points = scaled_points[:idx+1]
                    if len(current_points) > 1:
                        mob.set_points_as_corners(current_points)
            
            def update_dot(mob, alpha):
                nonlocal first_perihelion, first_aphelion
                idx = int(alpha * (len(scaled_points) - 1))
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
            
            # Animar la órbita
            self.play(
                UpdateFromAlphaFunc(traced_path, update_path),
                UpdateFromAlphaFunc(dot, update_dot),
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