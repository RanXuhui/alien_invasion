import pygame.font


class Button():

    def __init__(self, ai_settings, screen, msg):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self. button_color = (255, 255, 0)
        self.text_color = (25, 255, 255)
        self.font = pygame.font.SysFont(None, 48)   # 第一个参数是字体名，第二个参数是字号.none代表让python使用默认字体

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # pygame.Rect(left,top,width,height)或者是pygame.Rect((left,top),(width,height))   left,top其实就是矩形左上点的横纵坐标，用来控制生成rect对象的位置，而后面的宽度和高度则是用来控制生成矩形的大小尺寸
        self.rect.center = self.screen_rect.center

        # 按钮的标签只创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中（Pygame通过将你要显示的字符串渲染为图像来处理文本）"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)    # font.render(转换对象，是否开启反锯齿，文本颜色，背景颜色)将存储在msg中的文本转换为图像。True or False参数指定开启还是关闭反锯齿功能（反锯齿让文本的边缘更平滑）
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)   # Surface.blit(source, dest(位置), area=None, special_flags = 0):