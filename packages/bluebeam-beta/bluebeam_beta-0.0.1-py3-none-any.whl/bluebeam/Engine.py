# Hides "Hello from the pygame community"
from os import environ
import os

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pytmx

from bluebeam.GlobalVars import GlobalVars
#import GlobalVars
from bluebeam.Level import Level
from pytmx.util_pygame import load_pygame
from pygame import mixer

class Game_Engine:
    def __init__(self):
        # System init
        pygame.init()
        pygame.font.init()
        self._get_settings()
        self.clock = pygame.time.Clock()
        self.globals = GlobalVars()
        self.game_running = False

        # Screen init
        screen_size = ((self.screen_width, self.screen_height))
        self.globals.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Blue Beam")

        # getting directory for images
        self.sourceFileDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #print("os.getcwd(): ",os.getcwd())
        #print(self.sourceFileDir)
        self.imageDir = os.path.join(self.sourceFileDir, "bluebeam/images")
        self.soundDir = os.path.join(self.sourceFileDir, "bluebeam/Sounds")
        #print(self.soundDir)
        #self.heart = pygame.image.load(self.imageDir, "heart.png")

        # Load HUD information

        HUDfont = pygame.font.SysFont('Arial', 30)
        self.lives_text = HUDfont.render("Life: ", False, (0, 0, 0))
       # self.heart = pygame.transform.scale(pygame.image.load("images/heart.png").convert_alpha(), (50, 50))
        self.heart = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "heart.png")).convert_alpha(), (50, 50))
       # self.testHUD = pygame.transform.scale(pygame.image.load("images/testHUD2.png").convert_alpha(), (1920, 1080))
        self.testHUD = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "testHUD2.png")).convert_alpha(), (1920, 1080))
        self.HUDrect = self.testHUD.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
       # self.options = pygame.transform.scale(pygame.image.load("images/pause.png").convert_alpha(), (370, 85))
        self.options = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "pause.png")).convert_alpha(), (370, 85))
        self.optionsRect = self.options.get_rect(center = (1710, 1027))
        self.menuOn = True
        self.gameOn = True

        self.level = None
        self.image = None

        self.pause = False
        self.dead = False
        self.restart = False
        #Load mixer/sounds
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()

        self.images = []
        self.index = 0
        self.animation_counter = 0



    def reset(self):
        # Get Level
        self.level = Level(self.globals, self.screen, self.camera_offset)
            
    def yel_update(self):
        self.images = []
        for frame in range(1,6):
            img = pygame.image.load(os.path.join(self.imageDir, f'Yellow/frame{frame}.png'))

            #img = pygame.image.load(f'images/Yellow/frame{frame}.png')
            img = pygame.transform.scale(img, (80, 80))
            self.images.append(img)
        self.image = self.images[self.index]
        
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.image = self.images[self.index]
            self.index += 1
            self.animation_counter = 0
            if self.index >= 5:
                self.index = 0

    def blue_update(self):
        self.images = []
        for frame in range(1,6):
            img = pygame.image.load(os.path.join(self.imageDir, f'Blue/frame {frame}.png'))

            #img = pygame.image.load(f'images/Blue/frame {frame}.png')
            img = pygame.transform.scale(img, (80, 80))
            self.images.append(img)
        self.image = self.images[self.index]
        
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.image = self.images[self.index]
            self.index += 1
            self.animation_counter = 0
            if self.index >= 5:
                self.index = 0

    def red_update(self):
        self.images = []
        for frame in range(1,6):
            img = pygame.image.load(os.path.join(self.imageDir, f'Red/frame {frame}.png'))


            #img = pygame.image.load(f'images/Red/frame {frame}.png')
            img = pygame.transform.scale(img, (80, 80))
            self.images.append(img)
        self.image = self.images[self.index]
        
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.image = self.images[self.index]
            self.index += 1
            self.animation_counter = 0
            if self.index >= 5:
                self.index = 0

    
    def powerup_render(self):
        self.screen.blit(self.image, (920, 975))
    # CURRENTLY HARDCODED!!! 
    # We can modify this later - to read from another file
    def _get_settings(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.fps = 60
        self.camera_offset = pygame.math.Vector2(self.screen_width / 2 - 25, self.screen_height / 2 - 25)

    def _check_events(self):
        mouse = pygame.mouse.get_pos()
        if self.game_running:
            if self.level.player.hp <= 0:
                self.dead = True
                self.death_screen()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_running and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
                    self.pause = True
                    self.paused()
            elif event.type == pygame.MOUSEBUTTONUP:
                    if mouse[0] in range(self.optionsRect.left, self.optionsRect.right) and mouse[1] in range(self.optionsRect.top, self.optionsRect.bottom):
                        self.pause = True
                        self.paused()

    def _object_updates(self):
        self.level.update()
        '''
        if self.level.player.current_power == "yellow":
            self.yel_update()
        elif self.level.player.current_power == "blue":
            self.blue_update()
        elif self.level.player.current_power == "red":
            self.red_update()
        '''

    def _show_hud(self):
        lives = int(self.level.player.hp / 10)

        self.screen.blit(self.testHUD, self.HUDrect)
        self.screen.blit(self.options, (1525, 985))

        for i in range(lives):
            self.screen.blit(self.heart, ((285 + i * 55), 1010))


        # Ranges from 0 to 2, and can go higher
        # At 1 and higher, we want an icon to show up representing "fire speed"
        # At 2 and higher, the player unlocks the charged shot mechanic - with the corresponding charge bar
        powerup_level  = self.level.player.get_powerup_level()
        
        # Ranges from 0.0 to 1.0, representing 0% to 100% charge
        charge_percent = self.level.player.get_charge_level()

        if self.level.player.charge_unlocked:
            pygame.draw.rect(self.screen, (255, 0, 0, 100), pygame.rect.Rect(1120, 1020, 350, 20))
            pygame.draw.rect(self.screen, (0, 255, 0, 100), pygame.rect.Rect(1120, 1020, 350 * charge_percent, 20))
        

    def _update_screen(self):
        self.level.render()
        self._show_hud()
        #if self.image:
        #    self.powerup_render()
        # Does same thing as .flip(), but is more intuitive
        pygame.display.update()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def _update_dt(self):
        if self.clock.get_fps() == 0:
            dt = 0
        else:
            dt = 1. / self.clock.get_fps()
        self.globals.delta_time = dt

    def _cam_pos(self):
        return self.level.player.pos - self.camera_offset

    def main_menu(self):
        self.menu_running = True
        #mixer.music.load("sounds/Dangerous Dungeon.wav")
        mixer.music.load(os.path.join(self.soundDir, "Dangerous Dungeon.wav"))
        mixer.music.set_volume(0.25)
        mixer.music.play(-1)
        
        while self.menu_running:
            self._check_events()

            self.screen.fill((0, 0, 0))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            largeText = pygame.font.SysFont("arial", 115)
            btnText = pygame.font.SysFont("arial", 40)
            TextSurf, TextRect = self.text_objects("BlueBeam", largeText)
            TextRect.center = ((self.screen_width / 2), (self.screen_height / 2) - 200)
            self.screen.blit(TextSurf, TextRect)

                

            #startBtn = pygame.transform.scale(pygame.image.load("images/StartButton.png").convert_alpha(), (300, 125))
            startBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "StartButton.png")).convert_alpha(), (300, 125))
            #quitBtn = pygame.transform.scale(pygame.image.load("images/QuitButton.png").convert_alpha(), (300, 125))
            quitBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "QuitButton.png")).convert_alpha(), (300, 125))

            startRect = startBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
            quitRect = quitBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 125))
            
            self.screen.blit(startBtn, startRect)
            self.screen.blit(quitBtn, quitRect)

            

            if mouse[0] in range(startRect.left, startRect.right) and mouse[1] in range(startRect.top, startRect.bottom):
                # self.screen.blit(pygame.transform.scale(pygame.image.load("images/StartButtonRed.png"), (300, 125)),
                #                  startRect)
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "StartButtonRed.png")), (300, 125)),
                                                        startRect)
                if click[0] == 1:
                    mixer.music.stop()
                    mixer.music.unload()
                    self.menu_running = False
                    self.menuOn = False
                    self.reset()
                    return
            if mouse[0] in range(quitRect.left, quitRect.right) and mouse[1] in range(quitRect.top, quitRect.bottom):
                # self.screen.blit(pygame.transform.scale(pygame.image.load("images/QuitButtonRed.png"), (300, 125)),
                #                  quitRect)
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "QuitButtonRed.png")), (300, 125)),
                                 quitRect)
                if click[0] == 1:
                    self.exit()
            
            pygame.display.update()
            self.clock.tick(self.fps)

    def game_loop(self):
        while self.gameOn:
            if self.menuOn:
                self.main_menu()
            elif self.restart:
                self.restart = False
                self.reset()
                self.run_game()
            else:
                self.run_game()
    def run_game(self):
        #print(self.sourceFileDir)
        self.game_running = True
        # Get Level
        while self.game_running:   
            if self.pause == False and self.dead == False and self.restart == False:
                self._update_dt()
                self._check_events()
                self._object_updates()
            self._update_screen()
            self.clock.tick(self.fps) # Performs a time.sleep, at an interval ensuring the game runs at (fps)
        self.level.delete()

    
    def paused(self):
        
        pauseFont = pygame.font.SysFont('verdana', 55)

        resume, resumeRect = self.text_objects("Resume", pauseFont)
        resumeRect.center = (960, 400)
        menu, menuRect = self.text_objects("Main Menu", pauseFont)
        menuRect.center = (960, 475)
        end, endRect = self.text_objects("Quit", pauseFont)
        endRect.center = (960, 550)
        

        
        while self.pause == True:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            self.screen.blit(pygame.image.load(os.path.join(self.imageDir, "PauseMenu.png")).convert_alpha(), (0, 0))
            self.screen.blit(resume, resumeRect)
            self.screen.blit(menu, menuRect)
            self.screen.blit(end, endRect)


            if resumeRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Resume", True, (255, 0, 0)), resumeRect)
            if menuRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Main Menu", True, (255, 0, 0)), menuRect)
            if endRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Quit", True, (255, 0, 0)), endRect)
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = False
                            
                elif event.type == pygame.MOUSEBUTTONUP:
                    if resumeRect.collidepoint(mouse):
                        self.pause = False
                    if menuRect.collidepoint(mouse):
                        self.game_running = False
                        self.pause = False
                        self.menuOn = True
                    if endRect.collidepoint(mouse):
                        self.exit()
                    
            
            


            pygame.display.update()
            self.clock.tick(60)
            

    def death_screen(self):
        
        restart = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "RestartButton.png")), (300, 125))
        restartRect = restart.get_rect(center = (self.screen_width / 2, self.screen_height / 2 - 25))

        menuBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "MenuButton.png")), (300, 125))
        menuRect = menuBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 100))

        quitBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "QuitButton.png")), (300, 125))
        quitRect = quitBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 225))

        pygame.mixer.music.stop()
        # pygame.mixer.music.load(f'Sounds/cherish.xm')
        cherish_sound_dir = os.path.join(self.soundDir, f'cherish.xm')
        #print(cherish_sound_dir)
        pygame.mixer.music.load(cherish_sound_dir)
        pygame.mixer.music.play(-1,0,0)
        
        while self.dead:
            mouse = pygame.mouse.get_pos()

            self.screen.blit(pygame.image.load(os.path.join(self.imageDir, "DeathScreen.png")).convert_alpha(), (0, 0))
            self.screen.blit(restart, restartRect)
            self.screen.blit(menuBtn, menuRect)
            self.screen.blit(quitBtn, quitRect)

            if restartRect.collidepoint(mouse):
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "RestartButtonRed.png")), (300, 125)),
                                 restartRect)
            if menuRect.collidepoint(mouse):
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "MenuButtonRed.png")), (300, 125)),
                                 menuRect)
            if quitRect.collidepoint(mouse):
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "QuitButtonRed.png")), (300, 125)),
                                 quitRect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if mouse[0] in range(restartRect.left, restartRect.right) and mouse[1] in range(restartRect.top, restartRect.bottom):
                        self.game_running = False
                        self.dead = False
                        self.restart = True
                    if mouse[0] in range(menuRect.left, menuRect.right) and mouse[1] in range(menuRect.top, menuRect.bottom):
                        self.game_running = False
                        self.dead = False
                        self.menuOn = True
                    if mouse[0] in range(quitRect.left, quitRect.right) and mouse[1] in range(quitRect.top, quitRect.bottom):
                        self.exit()

            pygame.display.update()
            self.clock.tick(60)

    def exit(self):
        self.gameOn = False
        self.pause = False
        self.dead = False
        self.menu_running = False
        self.game_running = False

def main():
    engine = Game_Engine()
    engine.game_loop()


if __name__ == '__main__':
    main()

    # engine = Game_Engine()
    # engine.game_loop()
    #engine.run_game()
