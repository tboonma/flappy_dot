import tkinter as tk
from tkinter import messagebox 

from gamelib import Sprite, GameApp, Text

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5
STARTING_VELOCITY = -30
JUMP_VELOCITY = -20
PILLAR_SPEED = 10

class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False
    
    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY
    
    def start(self):
        self.is_started = True

    def jump(self):
        self.vy = JUMP_VELOCITY

    def is_out_of_screen(self):
        if self.x <= CANVAS_WIDTH and self.y <= CANVAS_HEIGHT:
            return False
        return True
    
    def is_hit(self, pillar_pair):
        if self.x >= pillar_pair.x-40 and self.x <= pillar_pair.x+40:
            if self.y <= pillar_pair.y-100 or self.y >= pillar_pair.y+100:
                return True
        return False

class FlappyGame(GameApp):
    def create_sprites(self):
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)

        self.elements.append(self.dot)

        self.pillar_pair = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.elements.append(self.pillar_pair)

    def init_game(self):
        self.create_sprites()
        self.is_started = False
        
    def pre_update(self):
        pass

    def post_update(self):
        if self.dot.is_out_of_screen() and self.is_started:
            messagebox.showinfo("Alert", "Game Over!")
            self.elements.clear()
            self.init_game()
        if self.dot.is_hit(self.pillar_pair):
            messagebox.showinfo("Alert", "Game Over!")
            self.elements.clear()
            self.init_game()

    def on_key_pressed(self, event):
        if event.char == ' ':
            if not self.is_started:
                self.is_started = True
                self.dot.start()
                self.pillar_pair.start()
            else:
                self.dot.jump()


class PillarPair(Sprite):
    def init_element(self):
        self.is_started = False
    
    def start(self):
        self.is_started = True
    
    def is_out_of_screen(self):
        if self.x <= CANVAS_WIDTH+40 and self.x >= -20:
            return False
        return True

    def update(self):
        if self.is_started:
            self.vx = PILLAR_SPEED
            self.x -= self.vx
            if self.is_out_of_screen():
                self.reset_position()

    def reset_position(self):
        self.x = CANVAS_WIDTH+40
        self.y = self.random_height()

    def random_height(self):
        import random
        return random.randint(120, CANVAS_HEIGHT-120)
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")
    
    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
