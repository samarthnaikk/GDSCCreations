import pygame
import numpy as np

class Chip8:
    def __init__(self):
        self.memory = np.zeros(4096, dtype=np.uint8)
        self.V = np.zeros(16, dtype=np.uint8)
        self.display = np.zeros((32, 64), dtype=np.uint8)
        self.pc = 0x200
        self.running = True
        self.memory[0x300:0x305] = [0xF0,  # ####
                                    0x90,  # #  #
                                    0x90,  # #  #
                                    0x90,  # #  #
                                    0xF0]  # ####

        self.V[0] = 10
        self.V[1] = 10
        pygame.init()
        self.scale = 10
        self.screen = pygame.display.set_mode((64 * self.scale, 32 * self.scale))
        pygame.display.set_caption("CHIP-8 Emulator")
        self.clock = pygame.time.Clock()
        self.execute_opcode(0xD015)

    def execute_opcode(self, opcode):
        if opcode == 0x00E0:  # CLS (Clear Screen)
            self.display.fill(0)
        elif opcode & 0xF000 == 0xD000:
            x = self.V[(opcode & 0x0F00) >> 8] % 64
            y = self.V[(opcode & 0x00F0) >> 4] % 32
            height = opcode & 0x000F
            self.V[0xF] = 0  

            for row in range(height):
                sprite_byte = self.memory[0x300 + row]  
                for col in range(8):
                    pixel = (sprite_byte >> (7 - col)) & 1
                    if pixel == 1:
                        if self.display[(y + row) % 32, (x + col) % 64] == 1:
                            self.V[0xF] = 1 
                        self.display[(y + row) % 32, (x + col) % 64] ^= 1
        
    def draw_screen(self):
        self.screen.fill((0, 0, 0))  
        for y in range(32):
            for x in range(64):
                if self.display[y, x] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (x * self.scale, y * self.scale, self.scale, self.scale))
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw_screen()
            self.clock.tick(60) 
        pygame.quit()

chip8 = Chip8()
chip8.run()
