#a node in a link list has contains data, prevnode, and next node
class LinkedListNode:

	def __init__(self, data:str, prevNode, nextNode):
		self.data = data
		self.prevNode = prevNode
		self.nextNode = nextNode

#a linked list of nodes
class LinkedList:

	#create an empty head and tail
	def __init__(self):
		self.head = None
		self.tail = None
		self.size = 0

	#get a data value at a given position
	def get(self, position:int):
		curNode = head

		while(position > 0):
			curNode = curNode.nextNode
			position = position - 1

		return curNode

	#create a new node at the end of the list
	def append(self, data:str):
		self.size = self.size + 1

		#ensure every data inserted becomes a string
		data = str(data)

		#if the list is empty, create head and tail
		if(self.head == None and self.tail == None):
			self.head = self.tail = LinkedListNode(data, None, None)
			return

		#add another node and set it to be the tail
		oldTail = self.tail
		oldTail.nextNode = LinkedListNode(data, oldTail, None)
		self.tail = oldTail.nextNode

	#create a new node at the beginning of the list
	def prepend(self, data:str):
		self.size = self.size + 1

		#ensure every data inserted becomes a string
		data = str(data)

		#if the list is empty, create head and tail
		if(self.head == None and self.tail == None):
			self.head = self.tail = LinkedListNode(data, None, None)
			return

		#add another node and set it to be the head
		oldHead = self.head
		oldHead.prevNode = LinkedList(data, None, oldHead)
		self.head = oldHead.prevNode

	#create a new node at a specific position in the list
	def insert(self, data:str, position:int):

		#ensure every data inserted becomes a string
		data = str(data)

		#if inserting at 0 or lower, just prepend
		if(position <= 0):
			self.prepend(data)
			return

		#if inserting at the end or higher, just append
		if(position >= self.size):
			self.append(data)
			return

		#go to the position we will be inserting at
		curNode = self.head
		while(position > 0):
			curNode = curNode.nextNode
			position = position - 1

		#create the node
		newNode = LinkedListNode(data, curNode.prevNode, curNode)

		#update the old nodes to include the new one
		curNode.prevNode.nextNode = newNode
		curNode.prevNode = newNode

		self.size = self.size + 1

	#remove a node at a certain position
	def remove(self, position:int):

		#if we delete the head, move the head up
		if(position == 0):
			secondNode = self.head.nextNode
			secondNode.prevNode = None
			self.head = secondNode
			self.size = self.size - 1
			return

		#if we delete the tail, move the tail down
		if(position == self.size - 1):
			secondToLastNode = self.tail.prevNode
			secondToLastNode.nextNode = None
			self.tail = secondToLastNode
			self.size = self.size - 1
			return

		#find the node to be deleted
		curNode = self.head
		while(position > 0):
			curNode = curNode.nextNode
			position = position - 1

		#determine its prev/next nodes
		p = curNode.prevNode
		n = curNode.nextNode

		#link the prev/next nodes, thus skipping current node
		if(p != None):
			p.nextNode = n
		if(n != None):
			n.prevNode = p

		self.size = self.size - 1

	#print the linked list
	def print(self):

		#empty list
		if(self.head == None and self.tail == None):
			print("Empty List")
			return

		#list with only 1 node
		if(self.head == self.tail):
			print("<" + self.head.data + ">")
			return

		#print all node data one by one
		curNode = self.head
		print("<", end="")
		while(curNode != self.tail):
			if(type(curNode.data) == 'float'):
				curNode.data = fixFloat(curNode.data)
			print(curNode.data + ", ", end="")
			curNode = curNode.nextNode
		print(curNode.data + ">")