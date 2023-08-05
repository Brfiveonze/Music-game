import sys
import pygame, GamePlayPage, BluetoothConnectPage
from button import button
from pygame.locals import QUIT

#參數設定
FPS = 60
WIDTH = 900
HEIGHT = 900

pygame.init()
MainWin = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('音樂遊戲(暫定)')
clock = pygame.time.Clock()

class Game_Win():
    def __init__(self):
        self.ImagePath = "pic/"
        self.BT_Image = self.ImagePath + "bt/"
        self.MusicPath = "music/"
        self.font_path = "C:\\Users\\brfiveonze\\Desktop\\mine\\SCH\\Music game\\font\\"
        self.MainWin = MainWin
        self.width = WIDTH
        self.height = HEIGHT

        font = pygame.font.Font(self.font_path + "Round.otf", 90)
        textSurf = font.render('節奏遊戲', 0.1, (0, 255, 0))
        
        self.server = None
        self.connected = False

        bt_start = pygame.image.load(self.BT_Image + "Start.png").convert_alpha()
        BG_S = pygame.image.load(self.ImagePath + "GB_MM.png")
        bt = button(WIDTH/2-75, HEIGHT/2-20, bt_start, bt_start, 1)

        while True:
            clock.tick(60)
            self.MainWin.blit(BG_S, (0, 0))
            self.MainWin.blit(textSurf, ((WIDTH - textSurf.get_width())/2, 200))
            bt.draw(self.MainWin)
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if bt.click():
                Game_Menu_Win(self)
            pygame.display.update()

class Game_Menu_Win():
    def __init__(self, StartFrame):
        self.StartFrame = StartFrame

        fontTitle = pygame.font.Font(self.StartFrame.font_path + "Round.otf", 90)
        textSurf = fontTitle.render('節奏遊戲', 0.1, (0, 255, 0))

        fontContext = pygame.font.Font(self.StartFrame.font_path + "NotoSansTC.otf", 40)
        textWarning = fontContext.render('請先連接設備', 1, (230, 0, 0))
        warn = False

        bt_play = pygame.image.load(self.StartFrame.BT_Image + "Play.png").convert_alpha()
        bt_bluetooth = pygame.image.load(self.StartFrame.BT_Image + "BlueTooth.png").convert_alpha()
        bt_back = pygame.image.load(self.StartFrame.BT_Image + "Back.png").convert_alpha()
        SelectSong = button(375, 350, bt_play, bt_play, 1)
        BlueToothSet = button(375, 430, bt_bluetooth, bt_bluetooth, 1)
        Back = button(375, 510, bt_back, bt_back, 1)


        BG = pygame.image.load(self.StartFrame.ImagePath + "GB_MM.png")
        Running = True

        while Running:
            MainWin.blit(BG, (0, 0))
            MainWin.blit(textSurf, ((WIDTH - textSurf.get_width())/2, 200))
            if self.StartFrame.connected:
                warn = False
            if warn:
                MainWin.blit(textWarning, ((WIDTH - textWarning.get_width())/2, 600))
            for bt in [SelectSong, BlueToothSet, Back]:
                bt.draw(StartFrame.MainWin)
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()

            #button event
            if SelectSong.click():
                if self.StartFrame.connected:
                    GamePlayPage.Game_Page(StartFrame)
                else:
                    MainWin.blit(textWarning, ((WIDTH - textWarning.get_width())/2, 600))
                    warn = True
                    print("No any bluetooth control device!")
            if BlueToothSet.click():
                BluetoothConnectPage.BlueTooth_Page(StartFrame)
            if Back.click():
                Running = False
            pygame.display.update()
    def __del__(self):
        print("Game_Menu_Win close!")

if __name__ == '__main__':
    Game_Win()