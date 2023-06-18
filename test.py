# 导入相应的库
import pygame

# 初始化 Pygame
pygame.init()

# 创建屏幕和精灵
screen = pygame.display.set_mode((800, 600))
sprite1 = pygame.Rect(160, 160, 50, 50)  # 精灵1的矩形框
sprite2 = pygame.Rect(200, 200, 50, 50)  # 精灵2的矩形框

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # 绘制屏幕和精灵
    screen.fill((255, 255, 255))  # 填充屏幕为白色
    pygame.draw.rect(screen, (0, 0, 0), sprite1)  # 在屏幕上绘制精灵1的矩形框
    pygame.draw.rect(screen, (255, 0, 0), sprite2)  # 在屏幕上绘制精灵2的矩形框
    
    # 判断碰撞
    if sprite1.colliderect(sprite2):
        print("精灵1和精灵2发生了碰撞！")
    else:
        print("精灵1和精灵2没有碰撞。")
    
    # 刷新屏幕
    pygame.display.flip()

# 退出游戏
pygame.quit()