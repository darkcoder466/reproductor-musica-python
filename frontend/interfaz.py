import tkinter as tk
from tkinter import filedialog
from .Tooltip import Tooltip
from backend.gestor_reproductor import GestorReproductor
import pygame
class Reproductor():
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Reproductor de Música")
        self.ventana.geometry("600x600")
        self.ventana.resizable(0, 0)
        self.ventana.configure(bg="#2a2a2a") 


        # Inicializar el gestor
        self.gestor = GestorReproductor()
        self.actualizando_ui = False

        # Configuración de colores
        self.color_fondo = "#2a2a2a"
        self.color_principal = "#1db954"
        self.color_secundario = "#191414"
        self.color_texto = "#ffffff"
        self.color_botones = "#1db954"
        self.color_botones_hover = "#1ed760"
        self.color_barra_progreso = "#1db954"
        self.color_fondo_lista = "#191414"

        self._crear_interfaz()
        self._actualizar_ui_periodicamente()

    def _crear_interfaz(self):
        """Crea todos los componentes de la interfaz"""
        self._crear_boton_cargar()
        self._crear_marco_principal()
        self._crear_frame_controles()

    def _crear_boton_cargar(self):
        """Crea el botón para cargar carpetas"""
        self.boton_cargar = tk.Button(
            self.ventana, 
            text="📁 Cargar carpeta",
            bg=self.color_botones,
            fg=self.color_texto,
            activebackground=self.color_botones_hover,
            activeforeground=self.color_texto,
            relief=tk.FLAT,
            font=("Arial", 10, "bold"),
            padx=10
        )
        self.boton_cargar.place(x=10, y=10)
        self.boton_cargar.bind("<Button-1>", self.cargar_carpeta)
        Tooltip(self.boton_cargar, "Selecciona una carpeta con canciones")

    def _crear_marco_principal(self):
        """Crea el marco principal con lista de canciones y controles"""
        self.frame_lista = tk.Frame(self.ventana, bg=self.color_secundario, width=560, height=500)
        self.frame_lista.place(relx=0.5, rely=0.5, anchor="center")

        # marco para la lista de canciones
        self.frame_canciones = tk.Frame(self.frame_lista, bg=self.color_fondo_lista, width=280, height=540)
        self.frame_canciones.place(x=0, y=0)

        # Listbox para mostrar las canciones
        self.lista_canciones = tk.Listbox(
            self.frame_canciones,
            bg="#2d2d2d",
            fg="white",
            selectbackground="#4a4a4a",
            selectforeground="white",
            font=('Helvetica', 10),
            activestyle='none',
            width=35,
            height=20
        )
        self.lista_canciones.pack(fill="both", expand=True, padx=5, pady=5)
        self.lista_canciones.bind("<<ListboxSelect>>", self.seleccionar_cancion)

        # marco para información de reproducción
        self.frame_tiempo = tk.Frame(self.frame_lista, bg=self.color_secundario, width=280, height=540)
        self.frame_tiempo.place(x=280, y=0)

        # Barra de progreso
        self.progreso = tk.Scale(
            self.frame_tiempo, 
            from_=0, 
            to=100, 
            orient="horizontal",
            length=240, 
            bg=self.color_secundario, 
            fg=self.color_texto, 
            troughcolor="#535353",
            highlightthickness=0,
            showvalue=False,
            activebackground=self.color_barra_progreso,
            sliderrelief=tk.FLAT
        )
        self.progreso.set(0)
        self.progreso.place(relx=0.5, rely=0.1, anchor="n")
        self.progreso.bind("<ButtonRelease-1>", self.saltar_a_posicion)
        Tooltip(self.progreso, "Haz clic para avanzar a un punto específico")

        # Etiqueta de tiempo
        self.etiqueta_tiempo = tk.Label(
            self.frame_tiempo, 
            text="00:00 / 00:00", 
            bg=self.color_secundario, 
            fg=self.color_texto, 
            font=("Arial", 12)
        )
        self.etiqueta_tiempo.place(relx=0.5, rely=0.2, anchor="n")

        # Información de la canción actual
        self.info_cancion = tk.Label(
            self.frame_tiempo,
            text="No hay canción seleccionada",
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 12),
            wraplength=250
        )
        self.info_cancion.place(relx=0.5, rely=0.3, anchor="n")

    def _crear_frame_controles(self):
        """Crea el frame inferior con los controles de reproducción"""
        self.frame_controles = tk.Frame(
            self.ventana, 
            bg=self.color_secundario, 
            width=600, 
            height=100
        )
        self.frame_controles.place(x=0, y=500)

        x_inicial = 50
        espacio = 60

        # Botones de control
        self.boton_atras = self._crear_boton_control(
            self.frame_controles, "⏮", self.retroceder, x_inicial + 0 * espacio
        )
        Tooltip(self.boton_atras, "Canción anterior")

        self.boton_reproducir = self._crear_boton_control(
            self.frame_controles, "▶", self.reproducir, x_inicial + 1 * espacio
        )
        Tooltip(self.boton_reproducir, "Reproducir canción")

        self.boton_pausar = self._crear_boton_control(
            self.frame_controles, "⏸", self.pausar, x_inicial + 2 * espacio
        )
        Tooltip(self.boton_pausar, "Pausar canción")

        self.boton_detener = self._crear_boton_control(
            self.frame_controles, "⏹", self.detener, x_inicial + 3 * espacio
        )
        Tooltip(self.boton_detener, "Detener canción")

        self.boton_adelantar = self._crear_boton_control(
            self.frame_controles, "⏭", self.adelantar, x_inicial + 4 * espacio
        )
        Tooltip(self.boton_adelantar, "Siguiente canción")

        # Control de volumen
        self.label_volumen = tk.Label(
            self.frame_controles,
            text="Volumen",
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 12, "bold")
        )
        self.label_volumen.place(x=x_inicial + 6 * espacio + 20, rely=0.4, anchor="s")

        self.slider_volumen = tk.Scale(
            self.frame_controles, 
            from_=0, 
            to=100, 
            orient="horizontal", 
            length=100,
            bg=self.color_secundario,
            fg=self.color_texto,
            troughcolor="#535353",
            highlightthickness=0,
            activebackground=self.color_barra_progreso,
            command=self.ajustar_volumen
        )
        self.slider_volumen.set(50)
        self.slider_volumen.place(x=x_inicial + 8 * espacio, rely=0.46, anchor="s")
        Tooltip(self.slider_volumen, "Ajustar volumen")

    def _crear_boton_control(self, frame, texto, comando, x_pos):
        """Crea un botón de control con estilo consistente"""
        boton = tk.Button(
            frame,
            text=texto,
            bg=self.color_botones,
            fg=self.color_texto,
            activebackground=self.color_botones_hover,
            activeforeground=self.color_texto,
            relief=tk.FLAT,
            width=5,
            font=("Arial", 12)
        )
        boton.place(x=x_pos, rely=0.4, anchor="s")
        boton.bind("<Button-1>", comando)
        return boton

    def _actualizar_ui_periodicamente(self):
        """Actualiza la UI periódicamente para mostrar el progreso"""
        if not self.actualizando_ui:
            self.actualizar_ui()
            self.ventana.after(1000, self._actualizar_ui_periodicamente)

    def actualizar_ui(self):
        """Actualiza todos los elementos de la UI según el estado del gestor"""
        cancion_actual = self.gestor.obtener_cancion_actual()
        
        # Actualizar barra de progreso y tiempo
        if cancion_actual:
            tiempo_actual = self.gestor.obtener_tiempo_actual()
            self.progreso.config(to=cancion_actual.duracion)
            self.progreso.set(tiempo_actual)
            
            # Formatear tiempo
            def formato_tiempo(segundos):
                minutos, segundos = divmod(int(segundos), 60)
                return f"{minutos:02d}:{segundos:02d}"
                
            self.etiqueta_tiempo.config(
                text=f"{formato_tiempo(tiempo_actual)} / {formato_tiempo(cancion_actual.duracion)}"
            )
            self.info_cancion.config(text=cancion_actual.nombre)
        else:
            self.progreso.set(0)
            self.etiqueta_tiempo.config(text="00:00 / 00:00")
            self.info_cancion.config(text="No hay canción seleccionada")

    # === Métodos de control ===
    def cargar_carpeta(self, event=None):
        """Carga una carpeta con canciones"""
        carpeta = filedialog.askdirectory()
        if carpeta:
            canciones = self.gestor.cargar_carpeta(carpeta)
            self.lista_canciones.delete(0, tk.END)
            for cancion in canciones:
                self.lista_canciones.insert(tk.END, str(cancion))

    def seleccionar_cancion(self, event=None):
        """Selecciona una canción de la lista"""
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            self.gestor.reproducir(seleccion[0])

    def reproducir(self, event=None):
        """Reproduce la canción actual o seleccionada"""
        self.gestor.reproducir()
        self.actualizar_ui()

    def pausar(self, event=None):
        """Pausa o reanuda la reproducción"""
        self.gestor.pausar()
        self.actualizar_ui()

    def detener(self, event=None):
        """Detiene la reproducción"""
        self.gestor.detener()
        self.actualizar_ui()

    def adelantar(self, event=None):
        """Avanza a la siguiente canción"""
        self.gestor.siguiente()
        self.actualizar_ui()

    def retroceder(self, event=None):
        """Retrocede a la canción anterior"""
        self.gestor.anterior()
        self.actualizar_ui()

    def saltar_a_posicion(self, event=None):
        """Salta a una posición específica en la canción"""
        if self.gestor.obtener_cancion_actual():
            nueva_posicion = self.progreso.get()
            pygame.mixer.music.set_pos(nueva_posicion) 
            # no actuliza bien el tiempo de reproducción actual, ni e slider, espere nuva actulizaciones.
            
           
        

            

    def ajustar_volumen(self, valor):
        """Ajusta el volumen del reproductor"""
        self.gestor.establecer_volumen(float(valor))
