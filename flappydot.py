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
        if self.y <= -20:
            return True
        if self.x <= CANVAS_WIDTH and self.y <= CANVAS_HEIGHT:
            return False
        return True
    
    def is_hit(self, pillar_pair):
        if self.x >= pillar_pair.x-40 and self.x <= pillar_pair.x+40:
            if self.y <= pillar_pair.y-100 or self.y >= pillar_pair.y+100:
                return True
        return False
    
    def counting_score(self, pillar_pair):
        if self.x >= pillar_pair.x-40 and self.x <= pillar_pair.x+40:
            if self.y >= pillar_pair.y-100 or self.y <= pillar_pair.y+100:
                return True
        return False


class FlappyGame(GameApp):
    def create_sprites(self):
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)

        self.elements.append(self.dot)

        self.pillar_pair = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.elements.append(self.pillar_pair)

    def init_game(self):
        self.bg_file = tk.PhotoImage(file='images/bg.png')
        self.background = self.canvas.create_image(
            CANVAS_WIDTH // 2, 
            CANVAS_HEIGHT // 2,
            image=self.bg_file)
        self.create_sprites()
        self.is_started = False
        self.score = 0
        self.passing_pillar = False
        self.all_score_letter = []
        self.all_score_pic = []
        
    def pre_update(self):
        self.logo_image = "images/logo.png"
        self.logo = tk.PhotoImage(file=self.logo_image)
        self.canvas_object_id = self.canvas.create_image(
            self.canvas_width//2, 
            60,
            image=self.logo)

    def post_update(self):
        if self.is_started:
            self.logo.blank()
            self.score_pic_locate = "images/score.png"
            self.score_pic = tk.PhotoImage(file=self.score_pic_locate)
            self.canvas_object_id = self.canvas.create_image(
            100, 
            50,
            image=self.score_pic)
            self.update_score()
            self.show_score()
        if self.dot.is_out_of_screen() and self.is_started:
            self.game_over()
        if self.dot.is_hit(self.pillar_pair):
            self.game_over()

    def on_key_pressed(self, event):
        if event.char == ' ':
            if not self.is_started:
                self.is_started = True
                self.dot.start()
                self.pillar_pair.start()
            else:
                self.dot.jump()
    
    def game_over(self):
        messagebox.showinfo("Alert", "Game Over!")
        self.elements.clear()
        self.init_game()
        self.score_pic.blank()
    
    def update_score(self):
        if self.dot.counting_score(self.pillar_pair):
            self.passing_pillar = True
        else:
            if self.passing_pillar:
                self.score += 1
                self.passing_pillar = False
    
    def show_score(self):
        if len(self.all_score_pic) > 0:
            for i in self.all_score_pic:
                i.blank()
        self.all_score_letter = list(str(self.score))
        self.all_score_pic = []
        for i in self.all_score_letter:
            locate = "images/number" + i + ".png"
            self.all_score_pic.append(tk.PhotoImage(file=locate))
        for i in range(len(self.all_score_pic)):
            self.canvas.create_image(
            200+(i*26), 
            50,
            image=self.all_score_pic[i])



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
    root.title("Flappy Dot Game")
    
    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()