class TreeNode:

	#every node contains data (command), a list of children, and a parent
	def __init__(self, data:str, line:int):
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

	#print tree left to right
	def printTreeLeftToRight(self):
		if(self.parent == None):
			print(self.data)
		for i in self.children:
			print(i.data)
		for i in self.children:
			i.printTreeLeftToRight()

	#print tree in preorder traversal
	def printTreeUpToDown(self):
		print(self.data)
		for i in self.children:
			i.printTreeUpToDown()

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

class HotKey:

	def __init__(self, keys:list):
		self.keys = keys

#open a file, read its contents line by line
def readScriptLineByLine(fileName:str) -> list:
	return open(fileName, "r").readlines()

#convert each line to a command. commands are a tuple: (# of tabs, command string)
def convertLinesToCommands(lines:list) -> list:

	#create the list of commands
	commands = []

	lineIndex = 0

	#for every line...
	for l in lines:

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

		lineIndex = lineIndex + 1

	return commands

#fill a node with children using list of commands and tabs. tabs dictate child/parent relationships between commands
def fillNode(node:TreeNode, commandIndex:int, tabs:int):

	#for every command...
	while(commandIndex < len(commands)):

		#read all next commands until a command with the same number of tabs is found
		if(commands[commandIndex][0] == tabs):
			break

		#if the number of tabs of this command is only 1 more than the current command's tabs, it will be a child
		if(commands[commandIndex][0] == tabs + 1):
			newNode = TreeNode(commands[commandIndex][1], commands[commandIndex][2]+1)
			fillNode(newNode, commandIndex + 1, tabs + 1) #fill child as well (recursion)
			node.insertChild(newNode)
		commandIndex = commandIndex + 1

#input validation to check if each key is a real key
def checkKey(keyList:list, line:int):

	#for every key in key list...
	for i in keyList:

		#if the key is a single character but is NOT (0-9, a-z, A-Z) exit program with syntax error
		if(len(i) == 1):
			asciiVal = ord(i[0])
			if(asciiVal >= 65 and asciiVal <= 90):
				continue
			if(asciiVal >= 97 and asciiVal <= 122):
				continue
			if(asciiVal >= 48 and asciiVal <= 57):
				continue
			print("Line " + str(line) + ": \"" + i + "\" is not a valid key.")
			exit()

		#if the key is not a single character but is NOT (CTRL, SHIFT, TAB, ENTER, ALT) exit program with syntax error
		else:
			match i:
				case "CTRL":
					continue
				case "SHIFT":
					continue
				case "TAB":
					continue
				case "ENTER":
					continue
				case "ALT":
					continue
				case _:
					print("Line " + str(line) + ": \"" + i + "\" is not a valid key.")
					exit()


#read script text line to determine a user-defined hotkey and return a list of keys
def readHotKeys() -> list:

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
			print("Incorrect Syntax, expected \":\"")

		#convert text data into array of keys (split string at +'s)
		curHotKey = []
		text = text.replace(' ', '')
		text = text[:-1]
		curHotKey = text.split('+')

		#ensure all keys exist
		checkKey(curHotKey, curLine)

		#add current hotkey to list of hotkeys
		allHotKeys.append(curHotKey)

	#return list of hotkeys
	return allHotKeys

#read a script line by line, convert to a tree of commands. **BEGIN SCRIPT** will be head of the tree
commands = convertLinesToCommands(readScriptLineByLine("pseudolang.txt"))
head = TreeNode("**BEGIN SCRIPT**", 0)
fillNode(head, 0, -1)

#gather hotkeys and evaluate for syntax. exit with error if there is one. print hotkeys
hotKeys = readHotKeys()
print(hotKeys)

