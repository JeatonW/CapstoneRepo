import CommandFormatter as CF

error = None

class CommandTree:

	def __init__(self, head):
		self.head = head

	def getHKList(self):

		listOfHotKeys = []

		for i in self.head.children:

			if(len(i.data.keys) == 0):
				i.data.solve()

			theAmazingTuple = (i.data.keys, i)

			listOfHotKeys.append(theAmazingTuple)

		return listOfHotKeys

	def solve(self):
		s = self.head.solve()
		if(not isinstance(s, str)):
			print("\nCompilation successful.")
		return s
	def solveAndPrint(self):
		s = self.head.solveAndPrint()
		if(not isinstance(s, str)):
			print("\nCompilation successful.")
		return s

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

	#prints out the tree in the form of tuples (lines, code, tabs)
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

	#solves and prints the entire tree 
	def solveAndPrint(self) -> list:
		return self.solveAndPrintHelper(0)
	def solveAndPrintHelper(self, tabs) -> list:

		executables = []
		
		#print the number of tabs before printing the code line
		for i in range(0, tabs):
			print("   ", end="")

		#try to solve the current line. save and print the error if there is one
		try:
			self.data.solve()
		except Exception as e:
			error = "\nLine " + str(self.line) + ": " + str(self.data.originalCodeLine) + "\n" + str(e)
			print(error)
			exit()
		self.data.print()

		if(self.data.comType == "Key Press"):

			childExec = []
			for i in self.children:
				childExec += i.solveAndPrintHelper(tabs + 1)

			tupleNameAndVar = ("Key Press", self.data.key, self.data.pressCount, childExec)
			executables.append(tupleNameAndVar)

		#perform if logic if current line is an if statement (solve and print children if necessary)
		elif(self.data.comType == "If"):
			if(self.data.comparisonAnswer == "1"):

				#solve and print children
				for i in self.children:
					executables += i.solveAndPrintHelper(tabs + 1)

		#perform while logic if current line is a while loop (solve and print children if necessary)
		elif(self.data.comType == "While"):
			while(self.data.comparisonAnswer == "1"):

				#solve and print children
				for i in self.children:
					executables += i.solveAndPrintHelper(tabs + 1)

				#try to solve and print the while loop again for each child; values have changed. store and print error if there is one
				try:
					for i in range(0, tabs):
						print("   ", end="")
					self.data.solve()
					self.data.print()
				except Exception as e:
					error = "\nLine " + str(self.line) + ": " + str(self.data.originalCodeLine) + "\n" + str(e)
					print(error)
					exit()

		#perform for logic if current line is a for loop (solve and print children if necessary)
		elif(self.data.comType == "For"):
			for i in range(0, int(self.data.loopCount)):

				#solve and print children
				for i in self.children:
					executables += i.solveAndPrintHelper(tabs + 1)

				#try to solve and print the for loop again for each child; values have changed. store and print error if there is one
				try:
					for i in range(0, tabs):
						print("   ", end="")
					self.data.solve()
					self.data.print()
				except Exception as e:
					error = "\nLine " + str(self.line) + ": " + str(self.data.originalCodeLine) + "\n" + str(e)
					print(error)
					exit()

		#normal one-lined logic (declaration, paste, highlight, etc)
		else:
			for i in self.children:
				executables += i.solveAndPrintHelper(tabs + 1)

		if(self.data.comType == "Exit"):
			tupleName = ("Exit")
			executables.append(tupleName)
		if(self.data.comType == "Paste"):
			tupleNameAndVar = ("Paste", str(self.data.string))
			executables.append(tupleNameAndVar)
		if(self.data.comType == "Highlight"):
			tupleNameAndVar = ("Highlight", self.data.distance)
			executables.append(tupleNameAndVar)
		if(self.data.comType == "Start Cursor"):
			tupleNameAndVar = ("Start Cursor", self.data.startX, self.data.startY)
			executables.append(tupleNameAndVar)
		if(self.data.comType == "Move Cursor"):
			tupleNameAndVar = ("Move Cursor", self.data.moveX, self.data.moveY)
			executables.append(tupleNameAndVar)

		return executables

	#solves the entire tree
	def solve(self) -> list:

		executables = []

		#try to solve the current line. save and print the error if there is one
		try:
			self.data.solve()
		except Exception as e:
			error = "\nLine " + str(self.line) + ": " + str(self.data.originalCodeLine) + "\n" + str(e)
			print(error)
			exit()
		
		if(self.data.comType == "Key Press"):

			childExec = []
			for i in self.children:
				childExec += i.solve()

			tupleNameAndVar = ("Key Press", self.data.key, self.data.pressCount, childExec)
			executables.append(tupleNameAndVar)

		#perform if logic if current line is an if statement (solve and print children if necessary)
		elif(self.data.comType == "If"):
			if(self.data.comparisonAnswer == "1"):

				#solve children
				for i in self.children:
					executables += i.solve()

		#perform while logic if current line is a while loop (solve and print children if necessary)
		elif(self.data.comType == "While"):
			while(self.data.comparisonAnswer == "1"):

				#solve children
				for i in self.children:
					executables += i.solve()

				#try to solve the while loop again for each child; values have changed. store and print error if there is one
				try:
					self.data.solve()
				except Exception as e:
					error = "\nLine " + str(self.line) + ": " + str(self.data.originalCodeLine) + "\n" + str(e)
					print(error)
					exit()

		#perform for logic if current line is a for loop (solve and print children if necessary)
		elif(self.data.comType == "For"):
			for i in range(0, int(self.data.loopCount)):

				#solve children
				for i in self.children:
					executables += i.solve()

				#try to solve the for loop again for each child; values have changed. store and print error if there is one
				try:
					self.data.solve()
				except Exception as e:
					error = "\nLine " + str(self.line) + ": " + str(self.data.originalCodeLine) + "\n" + str(e)
					print(error)
					exit()

		#solve normal one-lined logic (declaration, paste, highlight, etc)
		else:
			for i in self.children:
				executables += i.solve()

		if(self.data.comType == "Exit"):
			tupleNameAndVar = ("Exit", 0)
			executables.append(tupleNameAndVar)
		if(self.data.comType == "Paste"):
			tupleNameAndVar = ("Paste", str(self.data.string))
			executables.append(tupleNameAndVar)
		if(self.data.comType == "Highlight"):
			tupleNameAndVar = ("Highlight", self.data.distance)
			executables.append(tupleNameAndVar)
		if(self.data.comType == "Start Cursor"):
			tupleNameAndVar = ("Start Cursor", self.data.startX, self.data.startY)
			executables.append(tupleNameAndVar)
		if(self.data.comType == "Move Cursor"):
			tupleNameAndVar = ("Move Cursor", self.data.moveX, self.data.moveY)
			executables.append(tupleNameAndVar)

		return executables

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
def formatCommand(tabs:int, command:str):

	if("**BEGIN SCRIPT**" == command):
		return CF.ScriptBegin()
	elif("exit" == command):
		return CF.Exit(command)
	elif(tabs == 0):
		return CF.HotKey(command)
	elif("while(" == command[:6]):
		return CF.While(command)
	elif("for(" == command[:4]):
		return CF.For(command)
	elif("if(" == command[:3]):
		return CF.If(command)
	elif("key(" == command[:4]):
		return CF.KeyPress(command)
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

			#try to format the command. if there is an error, save it and print it
			try:
				formattedCommand = formatCommand(tabs, command)
			except Exception as e:
				error = "\nLine " + str(lineIndex+1) + ": " + command + "\n" + str(e)
				print(error)
				exit()

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
def createCommandTree(fileName:str) -> CommandTree:

	#read a script line by line, convert to an array of commands. a command is a tuple: (tabs:int, code:str, line:int)
	tupleArray = convertLinesToTuples(fileName)

	#create the head of a tree. it will be called **BEGIN SCRIPT**.
	headNode = TreeNode(CF.ScriptBegin(), 0)

	#fill this tree using the commands. the number of tabs on a tree represent what level it is on the tree.
	fillNode(headNode, tupleArray, 0, -1)

	return CommandTree(headNode)

#me test print stuff
def MeTest():

	#put the whole script into a tree
	ct = createCommandTree(input("Input file name: "))

	#get all ur information; list of tuples (keyArray, treeBranch)
	hks = ct.getHKList()

	#unpack each tuple
	i = 1
	for hk in hks:
		print(f"\nthis is hk#{i}: ")
		
		#take out the contents of the tuple
		(keyArray, treeBranch) = hk

		#this is the list of keys for a particular hotkey
		print(keyArray)

		#these are branches of the ct that you solve individually now
		tuplesOfJustice = treeBranch.solveAndPrint()

		#print the TUPLES
		for t in tuplesOfJustice:
			print(t)

		i = i + 1

#only run if this is main
if __name__ == '__main__':
	MeTest()