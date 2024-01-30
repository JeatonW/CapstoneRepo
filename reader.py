class TreeNode:

	#every node contains data (command), the line that the original command in the text file was on, a list of children, and a parent
	def __init__(self, data:str, line:int):
		self.data = data
		self.children = []
		self.parent = None
		self.line = line
		self.type = self.determineType()

	#determines what type of command this is (declaration? function?)
	def determineType(self) -> str:

		# :num -> beginning 2
		# -num: -> end 2

		if("**BEGIN SCRIPT**" == self.data):
			return "begin"
		if("::" == ):
			return "hotkey"
		if(":" in self.data):
			return "lang"
		if("=" in self.data and not "(" in self.data):
			return "dec"
		if("while(" in self.data):
			return "while"
		if("if(" in self.data):
			return "if"
		if("paste(" in self.data):
			return "paste"
		if("highlight(" in self.data):
			return "highlight"
		if("startCursor(" in self.data):
			return "start"
		if("moveCursor(" in self.data):
			return "move"

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

	#print tree in preorder traversal
	def printTree(self):
		self.printTreeHelper(0)
	def printTreeHelper(self, tabs):
		for i in range(0, tabs):
			print("   ", end="")
		print(self.data)
		for i in self.children:
			i.printTreeHelper(tabs + 1)

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

	#validate all commands
	def validateAllCommands(self):
		if(self.parent != None):
			self.parent.validateAllCommands()
		else:
			for hotkey in self.children:
				for lang in hotkey.children:
					for command in lang.children:
						command.vacHelper()
	def vacHelper(self):
		validateCommand(self.data, self.line)
		for c in self.children:
			c.vacHelper()

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

#open a file, read its contents line by line
def readScriptLineByLine(fileName:str) -> list:
	return open(fileName, "r").readlines()

#convert each line to a command. commands are a tuple: (tabs:int, command:str)
def convertLinesToCommands(fileName:list) -> list:

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
			tabCommandTuple = (tabs, command, lineIndex)
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

#input validation to check if each key is a real key
def checkKey(command:str, keyList:list, line:int):

	#for every key in key list...
	for i in keyList:

		#if the key is a single character but is NOT (0-9, a-z, A-Z) exit program with syntax error
		if(len(i) == 1):
			if(isNumOrLet(i[0])):
				continue
			printSyntaxError(command, line, len(command), 0, "\"" + i + "\" is not a valid key.")
			exit()

		#if the key is not a single character but is NOT (CTRL, SHIFT, TAB, ENTER, ALT) exit program with syntax error
		else:
			match i:
				case "CTRL_L":
					continue
				case "SHIFT_L":
					continue
				case "ALT_L":
					continue
				case "CTRL_R":
					continue
				case "SHIFT_R":
					continue
				case "ALT_R":
					continue
				case "TAB":
					continue
				case "ENTER":
					continue
				case "F1":
					continue
				case "F2":
					continue
				case "F3":
					continue
				case "F4":
					continue
				case "F5":
					continue
				case "F6":
					continue
				case "F7":
					continue
				case "F8":
					continue
				case "F9":
					continue
				case "F10":
					continue
				case "F11":
					continue
				case "F12":
					continue
				case _:
					printSyntaxError(command, line, len(command), 0, "\"" + i + "\" is not a valid key.")
					exit()

#read script text line to determine a user-defined hotkey and return a list of keys. results in syntax error if keys dont exist
def createHotKeys() -> list:

	#create list of hotkeys
	allHotKeys = []

	#hotkey nodes have 0 tabs, so get only children of the head
	hotKeyNodes = head.getChildren()

	#for every hotkey convert the text data into a list of keys i.e. "CTRL + SHIFT + F:" -> ["CTRL", "SHIFT", "F"]
	for i in hotKeyNodes:
		text = i.data
		curLine = i.line

		#ensure line ends with colon
		if(text[len(text)-1] != ':'):
			printSyntaxError(text, curLine, 0, 1, "Expected \":\"")

		#convert text data into array of keys (split string at +'s)
		curHotKey = []
		text = text.replace(' ', '')
		text = text[:-1]
		curHotKey = text.split('+')

		#ensure all keys exist
		checkKey(i.data, curHotKey, curLine)

		#add current hotkey to list of hotkeys
		allHotKeys.append(HotKey(curHotKey))

	#return list of hotkeys
	return allHotKeys

#read a script line by line, convert to an array of commands. a command is a tuple: (tabs:int, code:str, line:int)
commandsArray = convertLinesToCommands("pseudolang2.txt")

#create the head of a tree. it will be called **BEGIN SCRIPT**.
head = TreeNode("**BEGIN SCRIPT**", 0)

#fill this tree using the commands. the number of tabs on a tree represent what level it is on the tree.
fillNode(head, commandsArray, 0, -1)

hotkeys = createHotKeys()

keysPressedByUser = ["CTRL_L", "ALT_L", "F"]