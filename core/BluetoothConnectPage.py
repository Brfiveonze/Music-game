import sys,button, gc
import pygame

#
import server
#
class BlueTooth_Page():
    def __init__(self, StartFrame):
        # create server
        if StartFrame.server == None:
            print("none")
            self.server = server.Server()
        else:
            print("oe")
            self.server = StartFrame.server

        StartFrame.MainWin.fill((255, 255, 255))
        #get image
        #self.bt_reset = pygame.image.load(StartFrame.BT_Image + "Reset.png")
        self.bt_back = pygame.image.load(StartFrame.BT_Image + "Back.png")
        #Button
        #self.ReConnect = button.button(600, 0, self.bt_reset, self.bt_reset)
        self.BK_bt = button.button(600, 100, self.bt_back, self.bt_back)
        #font set
        self.font = pygame.font.SysFont("msjh", 48)

        print('Server host and channel:', self.server.get_server_sock().getsockname())

        running = True
        while running:
            client_sock = self.server.get_client_sock()
            if client_sock == None:

                self.text = self.font.render("Waiting for device to connect...", True, (0, 0, 255), (255, 255, 255))
                   
                StartFrame.MainWin.blit(self.text, ((StartFrame.MainWin.get_rect().w - self.text.get_rect().w) / 2,
                                                (StartFrame.MainWin.get_rect().h - self.text.get_rect().h) / 2))
                #pygame.display.update()
            else:
                #文字顯示
                self.text = self.font.render("Connect device name: {}".format(client_sock.getsockname()), True,
                                             (0, 127, 127), (255, 255, 255))
                StartFrame.MainWin.blit(self.text, ((StartFrame.MainWin.get_rect().w - self.text.get_rect().w) / 2,
                                                    (StartFrame.MainWin.get_rect().h - self.text.get_rect().h) / 2))

                StartFrame.connected = True
                StartFrame.server = self.server

                #顯示"重新連線"按鈕
                #self.ReConnect.draw(StartFrame.MainWin)

            #顯示"返回上一頁"按鈕
            self.BK_bt.draw(StartFrame.MainWin)

            #按鈕點擊
            if self.BK_bt.click():
                running = False
                if self.server.get_client_sock() == None:
                    self.server.close()
            """
            if self.ReConnect.click():
                StartFrame.MainWin.fill((255, 255, 255))
                self.server.close()
                StartFrame.server.close()
                """

            # 獲取所有event
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            gc.collect()
            pygame.display.update()