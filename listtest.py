import keyboard

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def get(self, index):
        if index < 0:
            return None
        current = self.head
        for i in range(index):
            if current is None:
                return None
            current = current.next
        if current is None:
            return None
        return current.data

class PlayerClass:
    def __init__(self):
        self.listt = LinkedList()
        self.listt.add(1)
        self.listt.add(2)
        self.listt.add(3)
        self.listt.add(4)
        self.listt.add(5)

def main():
    player = PlayerClass()
    point = 0

    # for event in pygame.event.get():
	# 	if event.type == pygame.QUIT:
	# 		sys.exit()
	# 	if event.type == pygame.KEYDOWN:
	# 		if event.key == pygame.K_LEFT or event.key == pygame.K_a:
	# 			speed = skier.turn(-1)
	# 		elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
	# 			speed = skier.turn(1)	

    # while True:
    #     flag = 0
    #     if keyboard.is_pressed('a'):
    #         flag = 1
    #         if flag:
    #             point -= 1
    #             point = min(0,point)
    #             flag = 0
    #     elif keyboard.is_pressed('d'):
    #         flag = 1
    #         if flag:
    #             point += 1
    #             point = max(5,point)
    #             flag = 0
        # else:
        #     pass

        # print("当前 point 值为:", point)
if __name__ == '__main__':
    main()