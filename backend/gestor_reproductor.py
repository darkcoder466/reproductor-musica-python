import os
import pygame
from .cancion import Cancion

class GestorReproductor:
    def __init__(self):
        pygame.mixer.init()
        self.canciones = []
        self.indice_actual = -1
        self.volumen = 0.5
        self.pausado = False
        self.en_reproduccion = False
        
    def cargar_carpeta(self, ruta_carpeta):
        """Carga todas las canciones MP3 de una carpeta"""
        self.canciones = []
        for archivo in os.listdir(ruta_carpeta):
            if archivo.lower().endswith((".mp3", ".wav", ".ogg", ".flac")):
                ruta_completa = os.path.join(ruta_carpeta, archivo)
                self.canciones.append(Cancion(ruta_completa))
        return self.canciones
        
    def reproducir(self, indice=None):
        """Reproduce una canción por su índice"""
        if not self.canciones:
            return False
            
        if indice is not None and 0 <= indice < len(self.canciones):
            self.indice_actual = indice
            
        if self.indice_actual == -1:
            self.indice_actual = 0
            
        pygame.mixer.music.load(self.canciones[self.indice_actual].ruta)
        pygame.mixer.music.set_volume(self.volumen)
        pygame.mixer.music.play()
        self.en_reproduccion = True
        self.pausado = False
        return True
        
    def pausar(self):
        """Pausa o reanuda la reproducción"""
        if self.pausado:
            pygame.mixer.music.unpause()
            self.pausado = False
        else:
            pygame.mixer.music.pause()
            self.pausado = True
            
    def detener(self):
        """Detiene la reproducción"""
        pygame.mixer.music.stop()
        self.en_reproduccion = False
        self.pausado = False
        
    def siguiente(self):
        """Pasa a la siguiente canción"""
        if not self.canciones:
            return False
            
        nuevo_indice = (self.indice_actual + 1) % len(self.canciones)
        return self.reproducir(nuevo_indice)
        
    def anterior(self):
        """Retrocede a la canción anterior"""
        if not self.canciones:
            return False
            
        nuevo_indice = (self.indice_actual - 1) % len(self.canciones)
        return self.reproducir(nuevo_indice)
        
    def establecer_volumen(self, volumen):
        """Establece el volumen (0-100)"""
        self.volumen = max(0, min(1, volumen / 100))
        pygame.mixer.music.set_volume(self.volumen)
        
    def obtener_cancion_actual(self):
        """Devuelve la canción actualmente en reproducción"""
        if 0 <= self.indice_actual < len(self.canciones):
            return self.canciones[self.indice_actual]
        return None
        
    def obtener_tiempo_actual(self):
        """Devuelve el tiempo actual de reproducción en segundos"""
        if self.en_reproduccion:
            return pygame.mixer.music.get_pos() / 1000
        return 0