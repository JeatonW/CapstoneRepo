import CommandFormatter as CF

class TreeNode:

	#every node contains data (command), the line that the original command in the text file was on, a list of children, and a parent
	def __init__(self, data, line:int):
		self.data = data
		self.children = []
		self.parent = None
		self.line = line

	#returns true only if the node is the head of the tree
	def isHead(self) -> bool:
		if(self.parent == None):
			return True
		return False

	#set the parent of this node. head node does not have a parent
	def setParent(self, parent):
		self.parent = parent

	#insert a child node into this node. this node will be the parent of child node
	def insertChild(self, child):
		self.children.append(child)
		child.setParent(self)

	def printTuples(self):
		self.printTuplesHelper(0)
	def printTuplesHelper(self, tabs):
		for i in range(0, tabs):
			print("   ", end="")
		print(self.data)
		for i in self.children:
			i.printTuplesHelper(tabs + 1)

	#print tree in preorder traversal
	def printTree(self):
		self.printTreeHelper(0)
	def printTreeHelper(self, tabs):
		for i in range(0, tabs):
			print("   ", end="")
		self.data.print()
		for i in self.children:
			i.printTreeHelper(tabs + 1)

	def solveAndPrint(self):
		self.solveAndPrintHelper(0)
	def solveAndPrintHelper(self, tabs):
		for i in range(0, tabs):
			print("   ", end="")

		try:
			self.data.solve()
		except Exception as e:
			print("\nLine " + str(self.line) + ": " + str(self.data.originalCodeLine))
			print(e)
			exit()
		self.data.print()


		if(self.data.comType == "If"):
			if(self.data.comparisonAnswer == "1"):
				for i in self.children:
					i.solveAndPrintHelper(tabs + 1)
		elif(self.data.comType == "While"):
			while(self.data.comparisonAnswer == "1"):

				for i in self.children:

					i.solveAndPrintHelper(tabs + 1)
					for i in range(0, tabs):
						print("   ", end="")
					self.data.solve()
					self.data.print()
		else:
			for i in self.children:
				i.solveAndPrintHelper(tabs + 1)

	def solve(self):
		self.data.solve()

		if(self.data.comType == "If"):
			if(self.data.comparisonAnswer == "1"):
				for i in self.children:
					i.solve()
		elif(self.data.comType == "While"):
			while(self.data.comparisonAnswer == "1"):
				for i in self.children:
					i.solve()
					self.data.solve()
		else:
			for i in self.children:
				i.solve()

	#get a node using its index in preorder traversal
	def getNode(self, num:int):
		if(num == 0):
			return self
		for i in self.children:
			num = num - 1
			if(num == 0):
				return i
		for i in self.children:
			i.getNode(num)

	#get the list of children for this node
	def getChildren(self) -> list:
		return self.children

#returns true if a string of characters are all numbers
def isStrNum(string:str) -> bool:

	for s in string:
		asciiVal = ord(s)
		if(asciiVal < 48 or asciiVal > 57):
			return False
	return True

#returns true if character is an operator
def isOperator(char:str) -> bool:
	if(len(char) > 1):
		print("Invalid length of string: " + char + ". Must be length of 1 for isOperator().")
		exit()
	if(char == '/' or char == '*' or char == '+' or char == '-' or char == '%' or char == '^'):
		return True
	return False

#returns true if character is a number or letter
def isNumOrLet(char:str) -> bool:
	if(len(char) > 1):
		print("Invalid length of string: " + char + ". Must be length of 1 for isOperator().")
		exit()
	asciiVal = ord(char)
	if(asciiVal >= 65 and asciiVal <= 90):
		return True
	if(asciiVal >= 97 and asciiVal <= 122):
		return True
	if(asciiVal >= 48 and asciiVal <= 57):
		return True
	return False

#prints a syntrax error using the incorrect code, the line its on, the position/length of the error, and the error message
def printSyntaxError(command:str, line:int, errorStartLength:int, errorEndLength:int, errorMessage:str):

	#print syntax message and faulty text line
	print("\nLine " + str(line) + ": Invalid syntax. " + errorMessage + "\n")
	print("   " + command)
	print("   ", end ="")

	#display ~ underneath problem area
	i = 0
	for c in command:
		if(i < errorStartLength or i > len(command)-errorEndLength-1):
			print("~", end="")
		else:
			print(" ", end="")
		i = i + 1
	print()

	#exit the program
	exit()

#determines what type of command this is (declaration? function?)
def formatCommand(command:str):

	if("**BEGIN SCRIPT**" == command):
		return CF.ScriptBegin()
	elif("::" == command[-2:]):
		return CF.HotKey(command)
	elif("while(" == command[:6]):
		return CF.While(command)
	elif("for(" == command[:4]):
		return CF.For(command)
	elif("if(" == command[:3]):
		return CF.If(command)
	elif(":" == command[-1:]):
		return CF.Language(command)
	elif("paste(" == command[:6]):
		return CF.Paste(command)
	elif("highlight(" == command[:10]):
		return CF.Highlight(command)
	elif("startCursor(" == command[:12]):
		return CF.StartCursor(command)
	elif("moveCursor(" == command[:11]):
		return CF.MoveCursor(command)
	else:
		return CF.Declaration(command)

#open a file, read its contents line by line
def readScriptLineByLine(fileName:str) -> list:
	return open(fileName, "r").readlines()

#convert each line to a command. commands are a tuple: (tabs:int, command:str)
def convertLinesToTuples(fileName:list) -> list:

	lines = readScriptLineByLine(fileName)

	#create the list of commands
	commands = []

	#for every line...
	lineIndex = 0
	for l in lines:

		#count how many tabs before the command
		i = 0
		tabs = 0
		tabsFound = False
		command = ""

		#for every character in the line...
		while(i < len(l)):

			#if the character is a tab, add to total tabs
			if(i < len(l) - 1 and l[i] == '\t' and tabsFound == False):
				tabs = tabs + 1

			#otherwise add character to command string
			else:
				if(l[i] != '\n'):
					command = command + l[i]
				tabsFound = True
			i = i + 1

		#delete empty lines
		if(command != ""):

			try:
				formattedCommand = formatCommand(command)
			except Exception as e:
				print("\nLine " + str(lineIndex+1) + ": " + command)
				print(e)
				exit()


			#print(formattedCommand)
			#print("TEST")
			#formattedCommand.print()

			tabCommandTuple = (tabs, formattedCommand, lineIndex)
			commands.append(tabCommandTuple)

		#go to next line
		lineIndex = lineIndex + 1

	#return final list of commands
	return commands

#fill a node with children using list of commands and tabs. tabs dictate child/parent relationships between commands
def fillNode(node:TreeNode, commands:list, commandIndex:int, tabs:int):

	#for every command...
	while(commandIndex < len(commands)):

		#read all next commands until a command with the same number of tabs is found
		if(commands[commandIndex][0] == tabs):
			break

		#if the number of tabs of this command is only 1 more than the current command's tabs, it will be a child
		if(commands[commandIndex][0] == tabs + 1):
			newNode = TreeNode(commands[commandIndex][1], commands[commandIndex][2]+1)
			fillNode(newNode, commands, commandIndex + 1, tabs + 1) #fill child as well (recursion)
			node.insertChild(newNode)
		commandIndex = commandIndex + 1

#perform all necessary methods to create a command tree from a file name
def createCommandTree(fileName:str) -> TreeNode:

	#read a script line by line, convert to an array of commands. a command is a tuple: (tabs:int, code:str, line:int)
	tupleArray = convertLinesToTuples(fileName)

	#create the head of a tree. it will be called **BEGIN SCRIPT**.
	headNode = TreeNode(CF.ScriptBegin(), 0)

	#fill this tree using the commands. the number of tabs on a tree represent what level it is on the tree.
	fillNode(headNode, tupleArray, 0, -1)

	return headNode


#head = createCommandTree(input("Input file name: "))
#head.solveAndPrint()
