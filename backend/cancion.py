import os
from mutagen.mp3 import MP3

class Cancion:
    def __init__(self, ruta):
        self.ruta = ruta
        self.nombre = os.path.basename(ruta)
        self.duracion = self._obtener_duracion()
        
    def _obtener_duracion(self):
        try:
            audio = MP3(self.ruta)
            return int(audio.info.length)
        except:
            return 0  # Si no se puede obtener la duración
    
    def __str__(self):
        minutos, segundos = divmod(self.duracion, 60)
        return f"{self.nombre} ({minutos:02d}:{segundos:02d})"