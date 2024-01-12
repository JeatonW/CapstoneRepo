class TreeNode:

	#every node contains data (command), the line that the original command in the text file was on, a list of children, and a parent
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

class HotKey:

	#languages supported by this hotkey
	langs = []

	#hotkeys are a list of keys
	def __init__(self, keys:list):
		self.keys = keys

	#set which languages are supported by this hotkey
	def setLangs(self, langs:list):
		self.langs = langs

	#print the hotkey to text
	def printHotKey(self):
		print()
		print(self.keys[0], end="")
		i = 1
		while(i < len(self.keys)):
			print(" + " + self.keys[i], end="")
			i = i + 1
		print()

	#print the list of languages to text
	def printLangs(self):
		print(self.langs[0], end="")
		i = 1
		while(i < len(self.langs)):
			print(", " + self.langs[i], end="")
			i = i + 1
		print()

	#print the hotkey and languages to text
	def printAll(self):
		self.printHotKey()
		print("   Languages: ", end="")
		self.printLangs()

#open a file, read its contents line by line
def readScriptLineByLine(fileName:str) -> list:
	return open(fileName, "r").readlines()

#convert each line to a command. commands are a tuple: (# of tabs, command string)
def convertLinesToCommands(lines:list) -> list:

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

#returns true if character is an operator
def isOperator(char:str) -> bool:
	if(len(char) > 1):
		print("Invalid length of string: " + char + ". Must be length of 1 for isOperator().")
		exit()
	if(char == '/' or char == '*' or char == '+' or char == '-'):
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

#read all lines of the script and ensure that functions (paste(), if(), while(), highlight(), etc) use correct syntax
def validateCommand(command:str, line:int):

	#bogus statements are bogus
	if(not "=" in command and not "(" in command):
		printSyntaxError(command, line, len(command), 0, "")

	#evaluate variable declarations, i.e. variable = value
	if("=" in command and not "(" in command):

		#split the string at the equals sign and evaluate both sides
		splitString = command.split("=")
		variable = splitString[0]
		statement = splitString[1]

		#remove all spaces after variable
		while(True):
			if(variable[-1:] == " "):
				variable = variable[:-1]
			else:
				break

		#remove all spaces before statement
		while(True):
			if(statement[:1] == " "):
				statement = statement[1:]
			else:
				break

		#record length of both in case of syntax error
		statementLength = len(statement)
		variableLength = len(variable)

		#remove spaces from statement (inbetween variables and operators)
		statement = statement.replace(" ", "")

		#statements beginning or ending with operators are not allowed
		if(not isNumOrLet(statement[-1:]) or not isNumOrLet(statement[:1])):
			printSyntaxError(command, line, 0, statementLength, "")
		
		#separate variables/numbers/operators into a list of "items"
		items = []
		curItem = ""
		for i in statement:
			#only letters, numbers, and operators are allowed in statement
			if(not isOperator(i) and not isNumOrLet(i)):
				printSyntaxError(command, line, 0, statementLength, "")
			if(not isOperator(i)):
				curItem = curItem + i
			else:
				items.append(curItem)
				items.append(i)
				curItem = ""
		items.append(curItem)

		#if there was a blank item, that means there were 2 operators in a row and that is not allowed
		for i in items:
			if(i == ""):
				printSyntaxError(command, line, 0, statementLength, "")

		#variable should have no spaces or operators
		for i in variable:
			if(not isNumOrLet(i)):
				printSyntaxError(command, line, variableLength, 0, "")

		#true and false statements are allowed
		if(statement == "true" or statement == "false"):
			return

		#all other statements are allowed (for now)
		return

	#available commands:
	#if():
	#while():
	#highlight()
	#paste()
	#startCursor()
	#moveCursor()

	#check if command (methods) matches any available commands. if it does, it is correct syntax. return
	if(command[:3] == "if(" and command[-2:] == "):"):
		return
	elif(command[:6] == "while(" and command[-2:] == "):"):
		return
	elif(command[:10] == "highlight(" and command[-1:] == ")"):
		return
	elif(command[:6] == "paste(" and command[-1:] == ")"):
		return
	elif(command[:12] == "startCursor(" and command[-1:] == ")"):
		return
	elif(command[:11] == "moveCursor(" and command[-1:] == ")"):
		return

	#if command does not match any available commands, syntax is incorrect. display syntax error and exit program
	else:
		textAfterCloseParenth = command.split(")", -1)
		errorEndLength = len(textAfterCloseParenth[len(textAfterCloseParenth)-1])
		printSyntaxError(command, line, len(command.split("(")[0]) + 1, errorEndLength + 1, "")

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
	exit()

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
					printSyntaxError(command, line, len(command), 0, "\"" + i + "\" is not a valid key.")
					exit()

#verify that all languages exist. add list of supported languages to their corresponding hotkey
def validateLangs(hotKeys:list):

	#language nodes have 1 tabs, so get grand children of the head
	hotKeyNodes = head.getChildren()
	hotKeyIndex = 0

	#for every hotkey, look at its languages (children)
	for h in hotKeyNodes:
		curLangNodes = h.getChildren()

		#for every language, check if it is a valid language
		langs = []
		for l in curLangNodes:

			#copy text once so it can be edited without changing original
			text = l.data

			#if there is no colon, syntax error
			if(text[len(text)-1] != ':'):
				printSyntaxError(text, l.line, 0, 1, "Expected \":\"")

			#remove colon and spaces
			text = text.replace(':', '')
			text = text.replace(' ', '')

			#find matches. if theres no match, syntax error
			match text:
				case "python":
					langs.append("python")
				case "java":
					langs.append("java")
				case _:
					printSyntaxError(l.data, l.line, len(l.data), 0, "Language does not exist.")

		#add language lists to appropriate hotkey
		hotKeys[hotKeyIndex].setLangs(langs)
		hotKeyIndex = hotKeyIndex + 1

#read script text line to determine a user-defined hotkey and return a list of keys. results in syntax error if keys dont exist
def validateHotKeys() -> list:

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

#read a script line by line, convert to a tree of commands. **BEGIN SCRIPT** will be head of the tree
commands = convertLinesToCommands(readScriptLineByLine("pseudolang.txt"))
head = TreeNode("**BEGIN SCRIPT**", 0)
fillNode(head, 0, -1)

#gather hotkeys and evaluate for syntax. exit with error if there is one. print hotkeys
hotKeys = validateHotKeys()

#evaluate syntax for languages and add language support to hotkeys
validateLangs(hotKeys)

#evaluate all lines of code to ensure valid syntax
head.validateAllCommands()

#print hotkeys and their supported languages
for h in hotKeys:
	h.printAll()

#if entire program runs with no issues, the syntax is valid (by current standards, anyway)
print("\nValid syntax.")