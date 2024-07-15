import pygame

class Sound:

    def __init__(self, path):
        pygame.init()
        pygame.mixer.init()
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.Sound.play(self.sound)