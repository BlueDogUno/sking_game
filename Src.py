# coding: utf-8
import sys
import pygame
import random
import math
import time
from pygame.locals import *


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

class Node:
	def __init__(self, data):
		self.data = data
		self.next = None

class LinkedList:
	def __init__(self):
		self.head = None

	def add(self, data):
		new_node = Node(data)
		new_node.next = self.head
		self.head = new_node

	def get(self, index):
		current = self.head
		for i in range(index):
			if current is None:
				return None
			current = current.next
		return current.data

# 滑雪者类
class SkierClass(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
# 滑雪者的朝向(-2到2)
		self.direction = 0
		self.imgs = LinkedList()
		self.imgs.add("./images/small_skier_right2.png")
		self.imgs.add("./images/small_skier_right1.png")
		self.imgs.add("./images/small_skier_forward.png")
		self.imgs.add("./images/small_skier_left1.png")
		self.imgs.add("./images/small_skier_left2.png")
		self.person = pygame.image.load(self.imgs.get(self.direction+2))
		self.rect = self.person.get_rect()
		self.rect.center = [320, 350]
		self.speed = [self.direction, 6-abs(self.direction)*2]

# 改变滑雪者的朝向
# 负数为向左，正数为向右，0为向前
	def turn(self, num):
		self.direction += num
		self.direction = max(-2, self.direction)
		self.direction = min(2, self.direction)
		center = self.rect.center
		self.person = pygame.image.load(self.imgs.get(self.direction+2))
		self.rect = self.person.get_rect()
		self.rect.center = center
		self.speed = [self.direction, 6-abs(self.direction)*2]
		return self.speed

# 移动滑雪者
	def move(self):
		self.rect.centerx += self.speed[0]
		self.rect.centerx = max(20, self.rect.centerx)
		self.rect.centerx = min(620, self.rect.centerx)

# 障碍物类
# Input:
# 	-img_path: 障碍物图片路径
# 	-location: 障碍物位置
# 	-attribute: 障碍物类别属性
class ObstacleClass(pygame.sprite.Sprite):
	def __init__(self, img_path, location, attribute):
		pygame.sprite.Sprite.__init__(self)
		self.img_path = img_path
		self.image = pygame.image.load(self.img_path)
		self.location = location
		self.rect = self.image.get_rect()
		self.rect.center = self.location
		self.attribute = attribute
		self.passed = False
	# 移动
	def move(self, num):
		self.rect.centery = self.location[1] - num


# 创建障碍物
def create_obstacles(s, e, num=10):
	obstacles = pygame.sprite.Group()
	locations = []
	for i in range(num):
		row = random.randint(s, e)
		col = random.randint(0, 9)
		location  = [col*64+20, row*64+20]
		if location not in locations:
			locations.append(location)
			attribute = random.choice(["tree", "flag"])
			img_path = './images/small_tree.png' if attribute=="tree" else './images/flag.png'
			obstacle = ObstacleClass(img_path, location, attribute)
			obstacles.add(obstacle)
	return obstacles

#创建道具收集物
class ToolClass(pygame.sprite.Sprite):
	def __init__(self, img_path, location, attribute):
		pygame.sprite.Sprite.__init__(self)
		self.img_path = img_path
		self.image = pygame.image.load(self.img_path)
		self.location = location
		self.rect = self.image.get_rect()
		self.rect.center = self.location
		self.attribute = attribute
		self.passed = False
	# 移动
	def move(self, num):
		self.rect.centery = self.location[1] - num

# 合并障碍物
def AddObstacles(obstacles0, obstacles1):
	obstacles = pygame.sprite.Group()
	for obstacle in obstacles0:
		obstacles.add(obstacle)
	for obstacle in obstacles1:
		obstacles.add(obstacle)
	return obstacles


# 显示游戏开始界面
def Show_Start_Interface(Demo, width, height):
	Demo.fill((255, 255, 255))
	tfont = pygame.font.Font('./font/simkai.ttf', width//4)
	cfont = pygame.font.Font('./font/simkai.ttf', width//20)
	# infont = pygame.font.Font('./font/simkai.ttf', width//40)
	title = tfont.render(u'极速滑雪', True, (255, 0, 0))
	content = cfont.render(u'按任意键开始游戏', True, (0, 0, 255))
	#玩法介绍
	# introduce = infont.reader(u'躲避树和敌人，拿旗加分')
	trect = title.get_rect()
	trect.midtop = (width/2, height/10)
	crect = content.get_rect()
	crect.midtop = (width/2, height/2.2)
	Demo.blit(title, trect)
	Demo.blit(content, crect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				return

#真人玩家链表

def hit_check(x1,x2,y1,y2): #敌我之间的碰撞检测
	if abs(x1-x2)<=5 and (abs(y1-y2)-32) <= 5 :#todo有神必的偏移量
		return True
	else :
		return False


#电脑玩家链表数据
class EnemyClass(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# 电脑玩家的朝向(-2到2)
		self.direction = 0
		self.imgs = ["./images/enemy_forward.png", "./images/enemy_right1.png", "./images/enemy_right2.png", "./images/enemy_left2.png", "./images/enemy_left1.png"]
		self.person = pygame.image.load(self.imgs[self.direction])
		self.rect = self.person.get_rect()
		self.rect.center = [320, 50]				#初始化人物位置
		self.livejug = 0
		self.time = 0
		#todo优化初始化数值
		self.speed = 1
		self.distance = 0
		self.angle = 0
		self.step_x = 0
		self.step_y = 0


	#方向判断
	def offset_jug (self,x1,x2,y1,y2):
		self.LRoffset = abs(x1-x2)-abs(y1-y2)+100 #判断图像和
		self.direction = 0
		if x1 < x2 and abs(x1-x2) > 20 :
			if  self.LRoffset < 0:
				self.direction = 4
			else :
				self.direction = -2

		elif x1 > x2 and abs(x1-x2) > 20:
			if self.LRoffset < 0 :
				self.direction = 1
			else :
				self.direction = 2

		else:
			self.direction = 0

		self.person = pygame.image.load(self.imgs[self.direction])
		# self.rect = self.person.get_rect()	#mystery加上敌人就会固定在左上角

	#todo追踪真人玩家--添加树结构和算法
	def chase(self,x1,x2,y1,y2) :
		# self.speed = 1
		 # 计算目标点与起始点之间的距离和角度
		self.distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
		self.angle = math.atan2(y1 - y2, x1 - x2)
    
    	# 根据速度计算每一步的移动距离
		self.step_x = self.speed * math.cos(self.angle)
		self.step_y = self.speed * math.sin(self.angle)
    
    	# 循环移动直到达到目标点附近
		self.distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

		self.rect.centery += self.step_y
		if self.rect.centery == y1 :
			self.step_x = x1-x2
		self.rect.centery = min(y1, self.rect.centery)

		self.rect.centerx += self.step_x
		self.rect.centerx = max(20, self.rect.centerx)
		self.rect.centerx = min(620, self.rect.centerx)

	def rebirth(self): #初始敌人位置
		self.rect.centerx = 320
		self.rect.centery = 50

	#通过贪心算法实现追击功能
	def calculate_distance(self,ddirection,x1,x2,y1,y2):
		# self.speed = 2
		if ddirection == "right":
			x2 = x2 + self.speed
		elif ddirection == "left":
			x2 = x2 - self.speed
		elif ddirection == "down":
			y2 = y2 + self.speed
		elif ddirection == "up":
			y2 = y2 -self.speed

		new_distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
		return new_distance
	def move(self,direction):
		if direction =="right":
			self.rect.centerx += self.speed
			self.rect.centerx = max(20, self.rect.centerx)
			self.rect.centerx = min(620, self.rect.centerx)
		elif direction =="left":
			self.rect.centerx -= self.speed
			self.rect.centerx = max(20, self.rect.centerx)
			self.rect.centerx = min(620, self.rect.centerx)
		elif direction =="down":
			self.rect.centery += self.speed
		elif direction =="up":
			self.rect.centery += self.speed
	def greedychase(self,x1,x2,y1,y2):
		# 计算当前位置到目标位置的距离
		self.distance = self.calculate_distance("raw",x1,x2,y1,y2)
		# distance = calculate_distance(tracking_position, target_position)
		# 获取所有可行的移动方向
		self.possible_directions = []

		if x2 < x1:
			self.possible_directions.append("right")
		elif x2 > x1:
			self.possible_directions.append("left")
		if y2 < y1:
			self.possible_directions.append("up")
		elif y2 > y1:
			self.possible_directions.append("down")
		# 创建一个根节点
		root = TreeNode('Root')
		current_node = root

		# 添加子节点，表示每个可能的方向
		possible_directions = ['up', 'down', 'left', 'right']
		for direction in possible_directions:
			new_node = TreeNode(direction)
			current_node.children.append(new_node)

		# 将最优方向作为子节点
		best_direction = None
		min_distance = float('inf')
		for child in current_node.children:
			new_distance = self.calculate_distance(child.value, x1, x2, y1, y2)
			if new_distance < min_distance:
				best_direction = child
				min_distance = new_distance

		# 更新最佳方向属性
		current_node.best_direction = best_direction.value
		# 更新追踪Sprite的位置
		self.move(current_node.best_direction)
		
#todo创建收藏物品序列--栈
class Collections():
	def __init__(self):
		self.num = 0

		

# 主程序
def main():
	'''
	初始化
	'''
	pygame.init()
	# 声音
	pygame.mixer.init()
	pygame.mixer.music.load("./music/bg_music.mp3")
	pygame.mixer.music.set_volume(0.4)
	pygame.mixer.music.play(-1)
	# 屏幕
	screen = pygame.display.set_mode([640, 640])
	pygame.display.set_caption('数据结构作业--滑雪')
	# 主频
	clock = pygame.time.Clock()
	# 滑雪者
	skier = SkierClass()

	#电脑玩家
	enemy = EnemyClass()
	#enemy.livejug = 0应该包含了

	# 记录滑雪的距离
	distance = 0
	# 创建障碍物
	obstacles0 = create_obstacles(20, 29)
	obstacles1 = create_obstacles(10, 19)
	obstaclesflag = 0
	obstacles = AddObstacles(obstacles0, obstacles1)

	#创建道具和收藏物
	# tools0 = create_tools(20, 29)
	# tools1 = create_tools(10, 19)
	# toolsflag = 0
	# tools = Addtools(tools0, tools1)



	# 分数
	font = pygame.font.Font(None, 50)
	score = 0
	score_text = font.render("Score: "+str(score), 1, (0, 0, 0))

	#敌我相关信息显示
	pfont = pygame.font.Font(None, 25)

	# 速度
	speed = [0, 6]
	Show_Start_Interface(screen, 640, 640)
	'''
	主循环
	'''
	# 更新屏幕
	def update():
		screen.fill([255, 255, 255])
		pygame.display.update(obstacles.draw(screen))
		pygame.display.update(obstacles.draw(screen))
		#人物的创建
		screen.blit(enemy.person, enemy.rect)	
		screen.blit(skier.person, skier.rect)
		#文字创建
		screen.blit(score_text, [10, 10])
		screen.blit(poeple_text, [10, 50])

		pygame.display.flip()
	while True:
		# 左右键控制人物方向
		# print(enemy.best_direction)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					speed = skier.turn(-1)
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					speed = skier.turn(1)		
		skier.move()
		#敌人行动
		enemy.offset_jug (skier.rect.x,enemy.rect.x,skier.rect.y,enemy.rect.y)

		#调试输出 
		# print(abs(skier.rect.x-enemy.rect.x),abs(skier.rect.y-enemy.rect.y))
		# print(skier.rect.x,enemy.rect.x,skier.rect.y,enemy.rect.y)


		distance += speed[1]
		if distance >= 640 and obstaclesflag == 0:
			obstaclesflag = 1
			obstacles0 = create_obstacles(20, 29)
			obstacles = AddObstacles(obstacles0, obstacles1)
		if distance >= 1280 and obstaclesflag == 1:
			obstaclesflag = 0
			distance -= 1280
			for obstacle in obstacles0:
				obstacle.location[1] = obstacle.location[1] - 1280
			obstacles1 = create_obstacles(10, 19)
			obstacles = AddObstacles(obstacles0, obstacles1)
		# 用于碰撞检测
		for obstacle in obstacles:
			obstacle.move(distance)
		#敌我碰撞检测
		pis_hit = hit_check(skier.rect.x,enemy.rect.x,skier.rect.y,enemy.rect.y)
		e_hit = pygame.sprite.spritecollide(enemy, obstacles, True)

		if e_hit or pis_hit or enemy.livejug == 1:
			# enemy.chase (skier.rect.x,enemy.rect.x,skier.rect.y,enemy.rect.y)
			enemy.greedychase (skier.rect.x,enemy.rect.x,skier.rect.y,enemy.rect.y)
			if e_hit:
				if e_hit[0].attribute == "tree" and not e_hit[0].passed:
					eis_hit = "enemy is dead +50"
					enemy.rebirth()
					score = score + 50
			elif pis_hit:
				eis_hit = "enemy got you -50"
				enemy.rebirth()
				# score = score - 50
				score = 0 
				skier.person = pygame.image.load("./images/small_skier_fall.png")
				update()
				# 摔倒后暂停一会再站起来
				pygame.time.delay(600)
				skier.person = pygame.image.load("./images/small_skier_forward.png")
				skier.direction = 0
				speed = [0, 6]
				# is_hit[0].passed = True
			enemy.livejug = 1
			# enemy.rebirth()
			enemy.livejug = 0

		else :
			eis_hit = "is chasing you"
			# enemy.chase (skier.rect.x,enemy.rect.x,skier.rect.y,enemy.rect.y)
			enemy.greedychase (skier.rect.x,enemy.rect.x,skier.rect.y,enemy.rect.y)
		#敌树碰撞反馈
		poeple_text = pfont.render("enemy:"+str(eis_hit),1,(0,0,0))
		# print(enemy.livejug)
		
		# 碰撞检测
		is_hit = pygame.sprite.spritecollide(skier, obstacles, False)
		if is_hit:
			if is_hit[0].attribute == "tree" and not is_hit[0].passed:
				score -= 50
				score = max(0,score)
				skier.person = pygame.image.load("./images/small_skier_fall.png")
				update()
				# 摔倒后暂停一会再站起来
				pygame.time.delay(600)
				skier.person = pygame.image.load("./images/small_skier_forward.png")
				skier.direction = 0
				speed = [0, 6]
				is_hit[0].passed = True
			elif is_hit[0].attribute == "flag" and not is_hit[0].passed:
				score += 10
				obstacles.remove(is_hit[0])
		score_text = font.render("Score: "+str(score), 1, (0, 0, 0))

			#敌我碰撞检测
		# if hit_check(skier.rect.x,enemy.rect.x,skier.rect.y,enemy.rect.y):
		# 	pis_hit = "hit!"
		# else :
		# 	pis_hit = "chasing"

		

		update()
		clock.tick(40)


if __name__ == '__main__':
	main()