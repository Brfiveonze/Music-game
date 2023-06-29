import pygame

class button(pygame.sprite.Sprite):
    def __init__(self, x, y, image1, image2, scale=1):
        self.FirstImage = image1
        self.SecendImage = image2
        self.scale = scale
        width = 148
        height = 40
        self.image = pygame.transform.scale(image1, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click_on = False
        self.clicked = False
        self.focus = False

    #畫圖
    def draw(self, surface):

        #滑鼠位置
        pos = pygame.mouse.get_pos()

        #按鈕狀態
        MouseMoment = pygame.mouse.get_pressed()

        #根據滑鼠按鈕 位置改變按鈕圖示
        if self.rect.collidepoint(pos):                                 #滑鼠位於按鈕範圍內
            if MouseMoment[0] == 0:                                     #滑鼠放開左鍵
                if self.clicked:                                        #觸發點擊效果
                    self.clicked = False
                    self.focus = True
                    self.click_on = True
                    surface.blit(self.FirstImage, (self.rect.x, self.rect.y))
                else:                                                   #確認滑鼠已在按鈕上但未觸發指令
                    self.focus = True
                    self.click_on = False
                    surface.blit(self.FirstImage, (self.rect.x, self.rect.y))
            elif MouseMoment[0] == 1 and (self.focus or self.clicked):  #滑鼠左鍵按壓
                self.clicked = True
                self.focus = False
                surface.blit(self.SecendImage, (self.rect.x, self.rect.y))
            else: surface.blit(self.FirstImage, (self.rect.x, self.rect.y))     #滑鼠於範圍外按壓移進到此按鈕
        #按鈕位於範圍外
        else:
            self.focus = False
            if MouseMoment[0] == 0:
                self.clicked = self.focus = False
                surface.blit(self.FirstImage, (self.rect.x, self.rect.y))
            else:
                surface.blit(self.FirstImage, (self.rect.x, self.rect.y))
        return

    def click(self):
        if self.click_on:
            self.click_on = False
            return True
        return False