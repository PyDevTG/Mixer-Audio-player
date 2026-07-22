import pygame
import time

class AudioPlayer:
    def __init__(self):
        self.available = False
        # Tenta inicializar com WASAPI (padrão Windows)
        try:
            pygame.mixer.init(devicename=None)
            self.available = True
            print("✅ Áudio inicializado.")
        except pygame.error as e:
            print(f"⚠️ Falha ao inicializar WASAPI: {e}")
            try:
                # Fallback para DirectSound
                pygame.mixer.init(driver='directsound')
                self.available = True
                print("✅ Áudio inicializado com DirectSound.")
            except Exception as e2:
                print(f"❌ Falha definitiva no áudio: {e2}")
                print("   O sistema funcionará sem som (modo mudo).")
                self.available = False

    def play(self, file_path, wait=True):
        """
        Toca o arquivo de áudio.
        Se wait=True (padrão), a função bloqueia até o áudio terminar.
        Se wait=False, toca e retorna imediatamente (interrompe o anterior).
        """
        if not self.available:
            return
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            if wait:
                while pygame.mixer.music.get_busy():
                    time.sleep(0.05)
        except Exception as e:
            print(f"Erro ao reproduzir {file_path}: {e}")

    def stop(self):
        """Para a reprodução atual."""
        if self.available:
            pygame.mixer.music.stop()