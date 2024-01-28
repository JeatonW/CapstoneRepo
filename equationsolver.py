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

#returns a fixed float without the weird python stuff where print(0.1+0.2) = 0.30000000000000004
def fixFloat(f:float) -> float:

	#convert to a string so we can evaluate every character
	f = str(f)

	#start at the beginning and evaluate every character
	fix = False
	zeroesInARow = 0
	index = 0

	#if 10 zeroes are found in a row, throw away the zeroes and everything after
	for i in f:
		if(i == '0'):
			zeroesInARow = zeroesInARow + 1
			if(zeroesInARow >= 10):
				fix = True
				break
		else:
			zeroesInARow = 0
		index = 0
	if(fix):
		f = f[:index-zeroesInARow]

	#return the fixed float
	return float(f)

#returns true only if a singular character is a mathematical operator
def isOperator(character:str) -> bool:

	#if string size is greater than 1, its not an operator
	if(len(character) > 1):
		return False

	#return true if operator, false otherwise
	match(character):
		case "^":
			return True
		case "*":
			return True
		case "/":
			return True
		case "%":
			return True
		case "+":
			return True
		case "-":
			return True
		case _:
			return False

#returns true if an entire string is made up of numbers
def isStrNum(string:str) -> bool:

	#blank strings are not numbers
	if(len(string) == 0):
		return False

	#allow one decimal value
	decimal = False

	#for every character, check if its a number. if its not return false
	index = 0
	for s in string:
		asciiVal = ord(s)

		#allow a subtraction sign only at the beginning
		if(index == 0 and asciiVal == 45):
			continue

		#allow one and only one decimal point (skip num check once)
		if(asciiVal == 46):
			if(not decimal):
				decimal = True
				continue
			else:
				raise Exception("Invalid syntax; numerical value has two decimal points.")

		#if character is not a num, return false
		if(asciiVal < 48 or asciiVal > 57):
			return False

	#if all charcters were numbers return true
	return True

#multiplication occurs when numbers are outside and next to parenthesis. add a multiplication operator there
def formatParentheses(equation:str) -> str:

	#remove spaces from the string
	equation = equation.replace(" ", "")

	#start at the beginning and assess every character
	index = 0
	while(index < len(equation) - 1):

		#number preceeding open parenthesis, insert * in between
		if(isStrNum(equation[index]) and equation[index+1] == "("):
			equation = equation[:index+1] + "*" + equation[index+1:]

		#closed parenthesis preceeding number, insert * in between
		if(equation[index] == ")" and isStrNum(equation[index+1])):
			equation = equation[:index+1] + "*" + equation[index+1:]

		index = index + 1

	return equation

#if parentheses are present, perform the equation inside them recursively
def assessParentheses(equation:str) -> str:

	#remember the original equation
	originalEquation = equation

	#remember if and when an open parenthesis is found
	openFound = False
	openIndex = 0
	closedFound = False
	closedIndex = 0

	#start at the beginning and assess every character
	index = 0
	while(index < len(equation)):

		#if a closed parenthesis is found before an open parenthesis, something is wrong
		if(not openFound and equation[index] == ")"):
			raise Exception("Closed parenthesis found before open parenthesis.")

		#keep updating the open parenthesis until closed parenthesis is found
		if(equation[index] == "("):
			openFound = True
			openIndex = index

		#if we found an open and closed parenthesis, then a sub equation has been found
		if(openFound and equation[index] == ")"):
			closedFound = True
			closedIndex = index
			break

		#go to next character
		index = index + 1

	#if there are no parentheses, end the method with no changes
	if(not openFound and not closedFound):
		return originalEquation

	#remember original equation before the parentheses
	originalStart = equation[:openIndex]

	#sub equation will start after the open parenthesis
	subEquation = equation[openIndex+1:]

	#sub equation will end before the close parenthesis
	subEnd = closedIndex - (openIndex + 1)
	subEquation = subEquation[:subEnd]

	#remember original equation after the parentheses
	originalEnd = equation[closedIndex+1:]

	#this is what the equation now looks like after the sub equation inside the parentheses has been solved
	originalSubSolved = originalStart + str(solveEquation(subEquation)) + originalEnd

	#we still need to assess the rest of the equation (we exited the loop upon finding the first pair) for parentheses
	return assessParentheses(originalSubSolved)

#split the string numerical values, variables, and operators into "items"
def splitToItems(equation:str) -> LinkedList:

	#create the linked list for the items
	items = LinkedList()

	#check the equation string character by character to find numbers/operators
	curItem = ""
	for i in equation:

		#finding an operator means the previous number has ended;
		#add the number and the operator to the list of items
		if(isOperator(i)):
			if(curItem != ""):

				#convert ints to floats
				if(isStrNum(curItem)):
					curItem = float(curItem)

				items.append(curItem)
			curItem = ""
			items.append(i)

		#if we havent found an operator yet, the number hasnt ended
		else:
			curItem = curItem + i

	#reached the length of the string, so add the last item if there is one
	if(isStrNum(curItem)):
		curItem = float(curItem)
	if(curItem != ""):
		items.append(curItem)

	#empty equations are an issue
	if(items.size == 0):
		raise Exception("Empty equation.")

	#return the finished list of items
	return items

#evaluate a node and return what type of data it is
def getNodeDataType(node) -> str:
	if(node == None):
		return "None"
	elif(isOperator(node.data)):
		return "Operator"
	elif(isStrNum(node.data)):
		return "Number"
	else:
		return None

#convert subtraction to addition with negative numbers
#combine multiple addition operators in a row into one addition operator
def formatSubAdd(items:LinkedList) -> LinkedList:

	#start at the second to last item
	#the very last item SHOULD be a number
	#check every item one by one
	i = items.size - 2
	curNode = items.tail.prevNode
	while(i >= 0):

		#if there is an operator or nothing followed by an addition operator, remove addition operator
		if(curNode.data == "+"):
			if(curNode.prevNode == None):
				items.remove(i)
			else:
				if(isOperator(curNode.prevNode.data)):
					items.remove(i)

		#convert subtraction into addition with negative numbers
		if(curNode.data == "-" and isStrNum(curNode.nextNode.data)):
			curNode.data = "+"
			curNode.nextNode.data = str(0 - float(curNode.nextNode.data))
			continue

		i = i - 1
		curNode = curNode.prevNode

	return items

#solves the equation using a linked list of items, returns final value
def solveItemList(items:LinkedList) -> float:

	#start at the head of the list
	curNode = items.head
	index = 0

	#do exponents
	while(curNode != None):
		if(curNode.data == "^"):

			#handle incorrect syntax
			prevType = getNodeDataType(curNode.prevNode)
			nextType = getNodeDataType(curNode.nextNode)
			if(prevType == "None" or prevType == "Operator" or nextType == "None" or nextType == "Operator"):
				raise Exception(prevType + " type cannot be exponentiated with " + nextType + " type.")

			#number before ^ is the base, and after is the exponent
			base = int(float(curNode.prevNode.data))
			exponent = int(float(curNode.nextNode.data))

			#negative and zero exponents are handled differently
			negative = False
			zero = False
			if(exponent < 0):
				negative = True
				exponent = 0 - exponent
			elif(exponent == 0):
				zero = True

			if(not zero):

				#perform multiplication
				product = base
				for x in range(0, exponent-1):
					product = product * base

				#positive exponent
				if(not negative):
					curNode.data = str(product)

				#negative exponent
				else:
					curNode.data = str(1 / product)

			#zero exponent
			else:
				curNode.data = 1

			#combine the two numbers and its operator into final answer
			items.remove(index - 1)
			items.remove(index)

			#we deleted a previous node, so correct the index
			index = index - 1

		#go to next node
		curNode = curNode.nextNode
		index = index + 1

	#return to the head of the list
	curNode = items.head
	index = 0

	#do division/multiplication/modulus
	while(curNode != None):
		if(curNode.data == "*" or curNode.data == "/" or curNode.data == "%"):

			#handle incorrect syntax
			prevType = getNodeDataType(curNode.prevNode)
			nextType = getNodeDataType(curNode.nextNode)
			if(prevType == "None" or prevType == "Operator" or nextType == "None" or nextType == "Operator"):
				raise Exception(prevType + " type cannot be multplied with " + nextType + " type.")

			#perform the operator
			if(curNode.data == "*"):
				curNode.data = str(float(curNode.prevNode.data) * float(curNode.nextNode.data))
			if(curNode.data == "/"):
				curNode.data = str(float(curNode.prevNode.data) / float(curNode.nextNode.data))
			if(curNode.data == "%"):
				curNode.data = str(float(curNode.prevNode.data) % float(curNode.nextNode.data))

			#combine the two numbers and its operator into final answer
			items.remove(index - 1)
			items.remove(index)

			#we deleted a previous node, so correct the index
			index = index - 1

		#go to next node
		curNode = curNode.nextNode
		index = index + 1

	#return to head of the list
	curNode = items.head
	index = 0

	#do addition/subtraction
	while(curNode != None):

		if(curNode.data == "+"):

			#handle incorrect syntax
			prevType = getNodeDataType(curNode.prevNode)
			nextType = getNodeDataType(curNode.nextNode)
			if(nextType == "None" or nextType == "Operator"):
				raise Exception(nextType + " type cannot be added to " + prevType + " type.")

			#perform the operator
			if(curNode.data == "+"):
				curNode.data = str(float(curNode.prevNode.data) + float(curNode.nextNode.data))
			if(curNode.data == "-"):
				curNode.data = str(float(curNode.prevNode.data) - float(curNode.nextNode.data))

			#combine the two numbers and its operator into final answer
			items.remove(index - 1)
			items.remove(index)

			#we deleted a previous node, so correct the index
			index = index - 1

		#go to next node
		curNode = curNode.nextNode
		index = index + 1

	#return the final answer (also ensure it displays properly)
	return fixFloat(items.head.data)

#perform all needed methods to solve an equation
def solveEquation(eq:str) -> float:

	formattedEquation = formatParentheses(eq)
	subEquationsSolved = assessParentheses(formattedEquation)
	originalItems = splitToItems(subEquationsSolved)
	formattedItems = formatSubAdd(originalItems)
	finalValue = solveItemList(formattedItems)

	return finalValue

print("Final value: " + str(solveEquation(input("\nInsert equation as String: "))))