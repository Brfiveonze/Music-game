import sys, random, pygame, button, time, gc
import asyncio

import threading

loop = asyncio.get_event_loop()

WIDTH = 900
HEIGHT = 900

class Game_Page():

    def __init__(self, StartFrame):
        #參數
        pygame.mixer.init()
        self.sounds = pygame.mixer.Sound(StartFrame.MusicPath + "Tetris.mp3")
        self.server = StartFrame.server

        # 音量
        self.sounds.set_volume(0.1)


        self.running = True
        self.MainWin = StartFrame.MainWin
        self.BTclient_Str = [['UP', 'DOWN'], ['LEFT', 'RIGHT']]
        self.Screen_Width, self.Screen_Height = pygame.display.get_window_size()
        self.clock = pygame.time.Clock()
        self.pause_page_IconPath = StartFrame.ImagePath + "pause/"

        #音樂撥放
        self.sounds.play(-1)

        #分數 音符
        self.Score = 0
        self.Hit_List = [0, 0, 0]   #Good Nice Bad
        self.FontSize = 60
        self.speeds = 1
        self.pause = False
        self.notes = 30
        self.GameBlock_UD = pygame.image.load(StartFrame.ImagePath + "g_block_UD.png")
        self.GameBlock_UD = pygame.transform.scale(self.GameBlock_UD, (80, 80))
        self.GameBlock_LR = pygame.image.load(StartFrame.ImagePath + "g_block_LR.png")
        self.GameBlock_LR = pygame.transform.scale(self.GameBlock_LR, (80, 80))

        #暫停頁圖片
        self.pause_page_size = {'x': 150, 'y': 300}
        self.pause_page_location = ((WIDTH - self.pause_page_size['x']) / 2, 300)
        self.pause_img = pygame.image.load(self.pause_page_IconPath + "pause.png")
        self.pause_bt_size = self.pause_img.get_width()
        self.pause_bt = self.Pause_btm(self.pause_bt_size, self.Screen_Width, self.pause_img)

        #暫停介面圖片設定
        self.play_icon = pygame.image.load(self.pause_page_IconPath + "play.png")
        self.play_icon_2 = pygame.image.load(self.pause_page_IconPath + "play_p.png")
        self.restart_icon = pygame.image.load(self.pause_page_IconPath + "restart.png")
        self.restart_icon_2 = pygame.image.load(self.pause_page_IconPath + "restart_p.png")
        self.menu_icon = pygame.image.load(self.pause_page_IconPath + "menu.png")
        self.menu_icon_2 = pygame.image.load(self.pause_page_IconPath + "menu_p.png")
        self.bt_play = button.button(self.pause_page_location[0] + 45, self.pause_page_location[1] + 40, self.play_icon,
                                     self.play_icon_2, 1)
        self.bt_restart = button.button(self.pause_page_location[0] + 45, self.pause_page_location[1] + 120, self.restart_icon,
                                     self.restart_icon_2, 1)
        self.bt_menu = button.button(self.pause_page_location[0] + 45, self.pause_page_location[1] + 200, self.menu_icon,
                                     self.menu_icon_2, 1)

        #得分區spite獲取
        self.JudgmentCircle = self.Score_Circle(StartFrame.ImagePath).ScoreGroup
        #音符獲取
        self.Note_splite = self.GetMusicAndScaleBlock()

        # build thread for receive bluetooth client data
        thread = threading.Thread(target=self.receive_bluetooth_data)
        thread.daemon = True
        thread.start()

        #背景
        self.BG_IG = pygame.image.load(StartFrame.ImagePath + "BG_IG.png")
        #字體
        self.font = pygame.font.SysFont("Arial", self.FontSize)

        while self.running:
            #楨數最大60
            self.clock.tick(60)
            #背景設定
            self.MainWin.blit(self.BG_IG, (0, 0))
            #得分版 總分數配置
            self.JudgmentCircle.draw(self.MainWin)
            self.textSurf = self.font.render(str(self.Score), 0.1, (0, 255, 0))
            self.MainWin.blit(self.textSurf, (self.Screen_Width-self.textSurf.get_width()-(self.pause_bt_size+20), 0))
            #音符繪製
            self.Note_splite.draw(self.MainWin)
            
            #for note in self.Note_splite:
             #   pygame.draw.rect(self.MainWin, (255, 0, 0), note.rect, 1)
            self.pause_bt.draw(self.MainWin)
            #event 獲取
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #暫停判定
            if self.pause:
                #顯示暫停menu
                self.Pause_Page()
                pygame.mixer.pause()
                
                if self.bt_play.click():
                    self.pause = False
                    pygame.mixer.unpause()
                if self.bt_restart.click():
                    pygame.mixer.stop()
                    self.sounds.play(-1)
                    del self.Note_splite
                    self.Note_splite = self.GetMusicAndScaleBlock()
                    self.Score = self.Hit_List[0] = self.Hit_List[1] = self.Hit_List[2] = 0
                    self.pause = False
                    gc.collect()
                if self.bt_menu.click():
                    self.running = False
            else:
                #確認是否點擊暫停鈕
                if self.pause_bt.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    self.pause = True
                else:
                    self.Note_splite.update(self.speeds)

            # list = 0 進入結算
            if not self.Note_splite.sprites():
                time.sleep(1)
                self.Hit_List[2] = self.notes - (self.Hit_List[0] + self.Hit_List[1])
                End_Game_Show_Score(StartFrame, self.Hit_List)
                self.running = False

            #藍芽排程
            #run_one_time(loop)

            pygame.display.update()

        print("close Game_Page")
        loop.close()
        self.sounds.stop()
        gc.collect()

    # receive client's signal
    def receive_bluetooth_data(self):
        client = self.server.get_client_sock()
        while True:
            recv = client.recv(1024)
            if len(recv) == 0:
                break
            print(recv.decode())
            self.hit(recv.decode())
    
    #消除
    def hit(self, hit_type):
        all_note_sprite = pygame.sprite.groupcollide(self.Note_splite, self.JudgmentCircle, False, False)
        for note, areaList in all_note_sprite.items():
            if note.Kill is not True:
                if (hit_type in self.BTclient_Str[0] and note.type == 'LR') or \
                    (hit_type in self.BTclient_Str[1] and note.type == 'UD'):
                    area = areaList[0]
                    note.Kill = True
                    print(area.name)
                    if area.name == "good":
                        self.Score += 10
                        self.Hit_List[0] += 1
                    else:
                        self.Score += 20
                        self.Hit_List[1] += 1

                    break
                else:
                    print(3)
                break
            '''
            elif data == 'OUT':
                print("Bluetooth controller disconnect \n Exit gamepage")
                self.running = False
                #StartFrame.BTclient = None
            else:
                print("Bluetooth get data {} is not {}".format(self.client_data, self.BTclient_Str))'''

    async def get_input(self, StartFrame):
        try:
            data = await self.BTclient.recv(1024)
            print(f"get data is {data}")
            self.client_data = data
        except OSError as e:
            print(str(e))
            '''self.running = False
            StartFrame.BTclient = None'''
            print("Tty reconnect Bluetooth controller")

    

    class Score_Circle():
        class Area(pygame.sprite.Sprite):
            def __init__(self, name):
                pygame.sprite.Sprite.__init__(self)
                self.name = name
        def __init__(self, ImagePath):
            pygame.sprite.Sprite.__init__(self)

            #每個得分格長與寬
            #得分格設定
            self.Score10 = self.Area("nice")
            self.Score5_Top = self.Area("good")
            self.Score5_Bot = self.Area("good")
            self.Score10.image = pygame.image.load(ImagePath + "/baseline.png")

            self.block_x = self.Score10.image.get_width()
            self.block_y = self.Score10.image.get_height()

            self.Score5_Top.image = pygame.Surface((self.block_x, self.block_y))
            self.Score5_Bot.image = pygame.Surface((self.block_x, self.block_y))
            #得分塊位置
            self.locationx = (WIDTH - self.block_x) / 2
            self.locationy = 700

            #背景透明化
            self.Score5_Top.image.set_alpha(1)
            self.Score5_Bot.image.set_alpha(1)

            self.Score10.rect = self.Score10.image.get_rect()
            self.Score5_Top.rect = self.Score5_Top.image.get_rect()
            self.Score5_Bot.rect = self.Score5_Bot.image.get_rect()
            self.Score10.rect.topleft = (self.locationx, self.locationy)
            self.Score5_Top.rect.topleft = (self.locationx, self.locationy - self.block_y)
            self.Score5_Bot.rect.topleft = (self.locationx, self.locationy + self.block_y)
            self.ScoreGroup = pygame.sprite.Group()
            self.ScoreGroup.add(self.Score10)
            self.ScoreGroup.add(self.Score5_Top)
            self.ScoreGroup.add(self.Score5_Bot)
            #self.AddFont()

        def AddFont(self):
            font_size = 20
            self.font = pygame.font.SysFont("Arial", font_size)
            self.textSurf = self.font.render('+5', 1, (0, 0, 0))
            self.textSurf1 = self.font.render('+10', 1, (0, 0, 0))
            self.Score5_Top.image.blit(self.textSurf, (0, 0))
            self.Score10.image.blit(self.textSurf1, (0, 0))
            self.Score5_Bot.image.blit(self.textSurf, (0, 0))

    class Pause_btm(pygame.sprite.Sprite):
        def __init__(self, bt_size, width, img):
            pygame.sprite.Sprite.__init__(self)
            self.bt_size = bt_size
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.topleft = (width - self.bt_size, 10)

        def draw(self, s):
            s.blit(self.image, self.rect.topleft)

    def GetMusicAndScaleBlock(self):
        g = pygame.sprite.Group()
        y_set = -10
        for i in range(self.notes):
            a = random.randrange(2)
            if a == 0:
                g.add(UD_Note(y_set, self.GameBlock_UD))
            else:
                g.add(LR_Note(y_set, self.GameBlock_LR))
            y_set -= random.randint(81, 201)
        return g

    def Pause_Page(self):
        self.pause_page = pygame.sprite.Sprite()
        self.pause_page.image = pygame.Surface(list(self.pause_page_size.values()))
        self.pause_page.image.fill((152, 152, 152))
        self.MainWin.blit(self.pause_page.image, tuple(self.pause_page_location))
        self.bt_play.draw(self.MainWin)
        self.bt_restart.draw(self.MainWin)
        self.bt_menu.draw(self.MainWin)


class NoteBlock(pygame.sprite.Sprite):
    def __init__(self, y_set, img, width, height, Ntype):
        pygame.sprite.Sprite.__init__(self)
        self.type = Ntype
        self.w = width
        self.h = height
        self.image = img.subsurface(((img.get_width() - width) / 2, (img.get_height() - height) / 2, width, height))
        
        x = (WIDTH - width) / 2 
        self.rect = pygame.Rect(x, y_set, width, height)
        self.rect.x = x
        self.rect.y = y_set
        self.Kill = False
        self.color = (255, 255, 255)
        self.killTime = 0
    def color_set(self, colorS):
        self.color = pygame.color.Color(colorS)
        self.image.fill(self.color)
    def update(self, speed):
        if self.Kill:
            if self.killTime < 20:
                ct = self.rect.center
                self.image = pygame.Surface((self.image.get_width() * 1.02, self.image.get_height() * 1.02))
                self.image.fill(self.color)
                self.image.set_alpha(200 - (10 * self.killTime))
                self.rect = self.image.get_rect()
                self.rect.center = ct
                self.killTime += 1
            else:
                self.kill()
        else:
            self.rect.y += speed
            if self.rect.y > 850:
                self.kill()

class UD_Note(NoteBlock):
    def __init__(self, y, img):
        self.type = 'UD'
        NoteBlock.__init__(self, y, img, 30, 80, self.type)
class LR_Note(NoteBlock):
    def __init__(self, y, img):
        self.type = 'LR'
        NoteBlock.__init__(self, y, img, 80, 20, self.type)

class End_Game_Show_Score():
    def __init__(self, SF, SList):
        self.Running = True

        self.GameOver_font = pygame.font.SysFont("Arial", 60)
        self.OverFontShow = self.GameOver_font.render("Game Over!", 0.1, (0, 255, 0))
        self.GoodFont = self.GameOver_font.render("Good X" + str(SList[0]), 0.1, (127, 85, 34))
        self.NiceFont = self.GameOver_font.render("Nice X" + str(SList[1]), 0.1, (135, 35, 124))
        self.BadFont = self.GameOver_font.render("Bad   X" + str(SList[2]), 0.1, (65, 86, 74))
        img = pygame.image.load(SF.ImagePath + "bt/Back.png")
        self.BackButtom = button.button(600, 800, img, img, 1)
        while self.Running:
            SF.MainWin.fill((127, 127, 127))
            SF.MainWin.blit(self.OverFontShow, (0, 0))
            SF.MainWin.blit(self.GoodFont, (0, 200))
            SF.MainWin.blit(self.NiceFont, (0, 300))
            SF.MainWin.blit(self.BadFont, (0, 400))
            self.BackButtom.draw(SF.MainWin)
            if self.BackButtom.click():
                self.Running = False


            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

#asyncio set
def run_one_time(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()
