import EquationSolver as es
import StringSolver as ss
import ComparisonSolver as cs
from VariableDictionary import VariableDictionary as VD

varDict = VD()

#a formatted command is a line of code taken from the script that is checked for syntax errors and formatted into useable variables
class FormattedCommand:

	#every formatted command has a command type (declaration, if, while, etc) and the original code line text
	def __init__(self, comType:str, originalCodeLine:str):
		self.comType = comType
		self.originalCodeLine = originalCodeLine

	#a solve function is required in children classes
	def solve(self):
		pass

	#if no print function is given in the child class, only the command type will be printed
	def print(self):
		print(self.comType)

	#returns true if a character is a letter or an underscore
	def isLet(self, character:str) -> bool:

		asciiVal = ord(character)

		if(asciiVal >= 65 and asciiVal <= 90):
			return True
		if(asciiVal >= 97 and asciiVal <= 122):
			return True
		if(asciiVal == 95):
			return True

		return False

	#returns true if a string is a number
	def isNum(self, string:str) -> bool:

		for c in string:
			asciiVal = ord(c)
			if(asciiVal < 48 or asciiVal > 57):
				return False

		return True

	#returns true if a character is a letter, number, or underscore
	def isNumOrLet(self, character:str) -> bool:

		asciiVal = ord(character)

		if(asciiVal >= 65 and asciiVal <= 90):
			return True
		if(asciiVal >= 97 and asciiVal <= 122):
			return True
		if(asciiVal >= 48 and asciiVal <= 57):
			return True
		if(asciiVal == 95):
			return True

		return False

	#returns true if a string contains an operator
	def strContainsOp(self, string:str) -> bool:

		for c in string:
			if(self.isOperator(c)):
				return True

		return False

	#returns true if the string is an existing key
	def checkKey(self, string:str) -> bool:

		match(string):
			case "CTRL_L":
				return True
			case "CTRL_R":
				return True
			case "SHIFT_L":
				return True
			case "SHIFT_R":
				return True
			case "ALT_L":
				return True
			case "ALT_R":
				return True
			case "TAB":
				return True
			case "ESC":
				return True
			case "ENTER":
				return True
			case "SPACE":
				return True
			case "M1":
				return True
			case "M2":
				return True
			case "M3":
				return True
			case _:
				return self.isNumOrLet(string)

	#returns true only if a singular character is a mathematical operator
	def isOperator(self, character:str) -> bool:

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
	def isStrNum(self, string:str) -> bool:

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

	#replace the nth substring
	def replaceNth(self, s, sub, repl, n):
		find = s.find(sub)

		#if find is not -1 we have found at least one match for the substring
		i = find != -1

		#loop until match found
		while(find != -1 and i != n):

			#start searching from after the last match
			find = s.find(sub, find + 1)
			i += 1
	    
	    #replace substring
		if(i == n):
			return s[:find] + repl + s[find+len(sub):]

		#return completed string
		return s

	#solve the equation
	def solveEquation(self, string:str):

		string = self.replaceVarsWithVals(string)

		if(string == "true" or string == " true"):
			return 1
		elif(string == "false" or string == " false"):
			return 0
		elif("\"" in string):
			value = ss.solveString(string)
		else:
			self.checkUndeclared(string)
			value = es.solveEquation(string)

		return value

	#check the string for any pre-declared variables. if any exist, replace them with their value
	def replaceVarsWithVals(self, string:str) -> str:

		#remove beginning space(s)
		while(string[0] == " "):
			string = string[1:]

		#determine if equation starts with quote or not
		if(string[0] == "\""):
			startWithQuote = True
		else:
			startWithQuote = False

		#split the string at each quotation mark
		stringNoQuotations = string.split("\"")

		#delete empty elements
		stringNoQuotations = list(filter(None, stringNoQuotations))

		#split this array of strings into string inside and outside quotations
		#we only want to replace variables with values outside of quotation marks
		quotes = []
		noQuotes = []
		quoteSwitch = startWithQuote
		for i in stringNoQuotations:
			if(startWithQuote):
				quotes.append(i)
			else:
				noQuotes.append(i)
			quoteSwitch = not quoteSwitch

		#check for every key in the equation
		keyList = varDict.getKeyList()
		for k in keyList:

			#handle each substring that was found outside of quotation marks
			i = 0
			while(i < len(noQuotes)):

				#a variable has been found
				if k in noQuotes[i]:

					#determine if the variable is float or string type
					match(varDict.getType(k)):

						case "Float":
							#print(string + " " + str(varDict.get(k)))
							noQuotes[i] = string.replace(k, str(varDict.get(k)))
						case "String":
							noQuotes[i] = self.replaceOutsideQuotes(noQuotes[i], k)

				i = i + 1

		#add the strings back together in order to form final string
		finalString = ""
		if(startWithQuote):
			i = 0
			while(i < len(quotes) or i < len(noQuotes)):
				if(i < len(quotes)):
					finalString = finalString + "\"" + quotes[i] + "\""
				if(i < len(noQuotes)):
					finalString = finalString + noQuotes[i]
				i = i + 1
		else:
			i = 0
			while(i < len(quotes) or i < len(noQuotes)):
				if(i < len(noQuotes)):
					finalString = finalString + noQuotes[i]
				if(i < len(quotes)):
					finalString = finalString + "\"" + quotes[i] + "\""
				i = i + 1

		return finalString

	#when modifying string equations, only replace variables if they are outside quotation marks
	def replaceOutsideQuotes(self, string:str, k:str) -> str:

		#split the string at every instance of the desired variable
		stringWithoutVar = string.split(k)

		#count how many quotation marks come before the variable in the string
		quoteFound = 0
		index = 0
		for i in stringWithoutVar:
			quoteFound = quoteFound + stringWithoutVar[1].count("\"")

			#if there is an even number of quotations before the variable, we can replace it with its value
			if(quoteFound % 2 == 0):
				string = self.replaceNth(string, k, "\"" + str(varDict.get(k)) + "\"", index)

			index = index + 1

		return string

	#if there are letters left in the string, it means a variable is undeclared
	def checkUndeclared(self, string:str):

		for c in string:
			if(self.isLet(c) and string != "true" and string != " true" and string != "false" and string != " false"):
				raise Exception("Undefined variable: \"" + string + "\"")

	#makes sure there is an appropriate number of variables, and that no variable is undeclared
	def argumentSyntax(self, string:str, args:int):

		#replace variables with their values
		string = self.replaceVarsWithVals(string)

		vals = string.split(",")

		#invalid # of args
		if(len(vals) != args):
			raise Exception(self.comType + " method takes " + str(args) + " argument, but " + str(len(vals)) + " were given.")

		#no args were given
		if(len(vals) == 1 and vals[0] == ""):
			raise Exception(self.comType + " method takes " + str(args) + " argument, but 0 were given.")

		#check for any undeclared variables
		index = 0
		for v in vals:
			self.checkUndeclared(v)
			index = index + 1

		return vals

#this is always the head of the tree. it only exists so that all hotkeys can be accessed from one tree
#instead of having a separate tree for each hotkey
class ScriptBegin(FormattedCommand):

	def __init__(self):
		super().__init__("Script Begin", "None")

#hotkeys are always children of the head. they indicate which keys should be pressed for a script to activate
class HotKey(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("HotKey", originalCodeLine)

		self.keys = []
		self.checkSyntax(originalCodeLine)

	def checkSyntax(self, originalCodeLine:str):
		
		if(originalCodeLine[-2:] != "::"):
			raise Exception("Invalid syntax for HotKey.")

	def solve(self):

		#hotkeys should only be solved once. if keys already
		#exist then the hotkey has already been solved
		if(len(self.keys) != 0):
			return

		#remove colons
		eq = self.originalCodeLine[:-2]

		#remove spaces
		eq = eq.replace(" ", "")

		#split the string in between each individual key
		keyList = eq.split("+")

		#make sure each key is valid, and if it is, add it to the list of keys
		for k in keyList:
			if(self.checkKey(k)):
				self.keys.append(k)
			else:
				raise Exception("Invalid key: " + k)

	#print the list of keys
	def print(self):
		if(len(self.keys) == 0):
			print("HotKey (Unsolved): " + self.originalCodeLine)
		else:
			print("HotKey: [", end="")
			index = 0
			for k in self.keys:
				if(index != len(self.keys) - 1):
					print(k, end=", ")
				else:
					print(k, end="")
				index = index + 1
			print("]")


class Language(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("Language", originalCodeLine)

class Declaration(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("Declaration", originalCodeLine)

		#remove spaces from the line of code
		#originalCodeLine = originalCodeLine.replace(" ", "")

		self.variable = []
		self.equation = ""
		self.detVarEq(originalCodeLine)
		self.checkVarSyntax()

	#solves the equation and sets all variables equal to the final value
	def solve(self):

		value = self.solveEquation(self.equation)

		for v in self.variable:
			varDict.set(v, value)

	#reads the string and determines which parts are variables, and which part is the equation
	def detVarEq(self, originalCodeLine:str):

		#check every line for an equation symbol
		equationFound = False
		curItem = ""
		for c in originalCodeLine:

			#if we havent found an equation symbol, we are still on  the same item
			if(c != "="):
				curItem = curItem + c

			#if we found an equation symbol, previous item is a variable
			else:

				#remove ending spaces
				while(curItem[len(curItem)-1] == " "):
					curItem = curItem[:-1]

				#spaces in the variable are not allowed
				if(" " in curItem):
					raise Exception("Variable names cannot contain spaces.")

				#add the item to the list of variables
				self.variable.append(curItem)
				curItem = ""

		#last item is the equation
		self.equation = curItem

	#checks to make sure each variable has proper syntax
	def checkVarSyntax(self):

		#for every variable
		for v in self.variable:

			#first character must be a letter or underscore
			if(not self.isLet(v[0])):
				raise Exception("Variables must start with a letter or underscore.")

			#all characters must be a letter, underscore, or number
			for c in v:
				if(not self.isNumOrLet(c)):
					raise Exception("Variables must only contain letters, underscores, and numbers.")

	def print(self):
		for v in self.variable:
			if(varDict.contains(v)):
				print(v + " : " + str(varDict.get(v)))
			else:
				print(v + " (Unsolved) : " + self.equation)

class Paste(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("Paste", originalCodeLine)
		self.checkSyntax(originalCodeLine)
		self.string = None

	def checkSyntax(self, originalCodeLine:str):
		
		if(originalCodeLine[:6] != "paste(" or originalCodeLine[-1:] != ")"):
			raise Exception("Invalid syntax for Paste method.")

	def solve(self):
		self.string = self.solveEquation(self.originalCodeLine[6:-1])

	def print(self):
		if(self.string == None):
			print("Paste (Unsolved): " + self.originalCodeLine)
		else:
			print("Paste: " + str(self.string))

class Highlight(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("Highlight", originalCodeLine)

		#remove spaces from the line of code
		self.originalCodeLine = self.originalCodeLine.replace(" ", "")

		self.checkSyntax(self.originalCodeLine)
		self.distance = None

	def checkSyntax(self, originalCodeLine:str):
		
		if(originalCodeLine[:10] != "highlight(" or originalCodeLine[-1:] != ")"):
			raise Exception("Invalid syntax for Highlight method.")

	def solve(self):
		val = self.argumentSyntax(self.originalCodeLine[10:-1], 1)[0]
		self.distance = es.solveEquation(val)

	def print(self):
		if(self.distance == None):
			print("Highlight (Unsolved): " + str(self.originalCodeLine))
		else:
			print("Highlight: " + str(self.distance))

class StartCursor(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("Start Cursor", originalCodeLine)

		#remove spaces from the line of code
		self.originalCodeLine = self.originalCodeLine.replace(" ", "")

		self.checkSyntax(self.originalCodeLine)
		self.startX = self.startY = None

	def checkSyntax(self, originalCodeLine:str):
		
		if(originalCodeLine[:12] != "startCursor(" or originalCodeLine[-1:] != ")"):
			raise Exception("Invalid syntax for Start Cursor method.")

	def solve(self):
		vals = self.argumentSyntax(self.originalCodeLine[12:-1], 2)

		self.startX = es.solveEquation(vals[0])
		self.startY = es.solveEquation(vals[1])

	def print(self):
		if(self.startX == self.startY == None):
			print("Start Cursor (Unsolved): " + self.originalCodeLine)
		else:
			print("Start Cursor: " + str(self.startX) + ", " + str(self.startY))

class MoveCursor(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("Move Cursor", originalCodeLine)

		#remove spaces from the line of code
		self.originalCodeLine = self.originalCodeLine.replace(" ", "")

		self.checkSyntax(self.originalCodeLine)
		self.moveX = self.moveY = None

	def checkSyntax(self, originalCodeLine:str):
		
		if(originalCodeLine[:11] != "moveCursor(" or originalCodeLine[-1:] != ")"):
			raise Exception("Invalid syntax for Move Cursor method.")

	def solve(self):
		vals = self.argumentSyntax(self.originalCodeLine[11:-1], 2)

		self.moveX = es.solveEquation(vals[0])
		self.moveY = es.solveEquation(vals[1])

	def print(self):
		if(self.moveX == self.moveY == None):
			print("Move Cursor (Unsolved): " + self.originalCodeLine)
		else:
			print("Move Cursor: " + str(self.moveX) + ", " + str(self.moveY))

class KeyPress(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("Key Press", originalCodeLine)
		self.checkSyntax(originalCodeLine)
		self.key = self.pressCount = None

	def checkSyntax(self, originalCodeLine:str):
		if(originalCodeLine[:4] != "key(" or originalCodeLine[-2:] != "):"):
			raise Exception("Invalid syntax for Key Press method.")

	def argumentKeySyntax(self, string:str):

		string = string.replace(" ", "")
		vals = string.split(",")

		#invalid # of args
		if(len(vals) != 2):
			raise Exception(self.comType + " method takes 2 arguments, but " + str(len(vals)) + " were given.")

		#no args were given
		if(len(vals) == 1 and vals[0] == ""):
			raise Exception(self.comType + " method takes 2 arguments, but 0 were given.")

		#make sure first argument is a key
		if(not self.checkKey(vals[0])):
			raise Exception("Invalid key.")

		#make sure second argument is an integer
		if(not self.isNum(vals[1])):
			print(vals[1])
			raise Exception("Must input an integer into second argument.")

		return vals

	def solve(self):
		vals = self.argumentKeySyntax(self.originalCodeLine[4:-2])

		self.key = vals[0]
		self.pressCount = es.solveEquation(vals[1])

	def print(self):
		if(self.key == self.pressCount == None):
			print("Key Press (Unsolved): " + self.originalCodeLine)
		else:
			print("Key Press: " + str(self.key) + ", " + str(self.pressCount))

class Exit(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("Exit", originalCodeLine)
		self.checkSyntax(originalCodeLine)

	def checkSyntax(self, originalCodeLine:str):

		if(originalCodeLine != "exit"):
			raise Exception("Invalid syntax for exit command.")

	def solve(self):
		pass

	def print(self):
		print("Exit")

class If(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("If", originalCodeLine)
		self.checkSyntax(originalCodeLine)
		self.comparisonAnswer = None

	def checkSyntax(self, originalCodeLine:str):
		if(originalCodeLine[:3] != "if(" or originalCodeLine[-2:] != "):"):
			raise Exception("Invalid syntax for If statement.")

	def solve(self):
		comparisonEquation = self.originalCodeLine[3:-2]
		comparisonEquation = self.replaceVarsWithVals(comparisonEquation)
		self.comparisonAnswer = cs.solveEquation(comparisonEquation)

	def print(self):
		if(self.comparisonAnswer == None):
			print("If (Unsolved): " + self.originalCodeLine)
		else:
			print("If: " + str(self.comparisonAnswer))

class While(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("While", originalCodeLine)
		self.checkSyntax(originalCodeLine)
		self.comparisonAnswer = None

	def checkSyntax(self, originalCodeLine:str):
		if(originalCodeLine[:6] != "while(" or originalCodeLine[-2:] != "):"):
			raise Exception("Invalid syntax for While loop.")

	def solve(self):
		comparisonEquation = self.originalCodeLine[6:-2]
		comparisonEquation = self.replaceVarsWithVals(comparisonEquation)
		self.comparisonAnswer = cs.solveEquation(comparisonEquation)

	def print(self):
		if(self.comparisonAnswer == None):
			print("While (Unsolved): " + self.originalCodeLine)
		else:
			print("While: " + str(self.comparisonAnswer))


class For(FormattedCommand):

	def __init__(self, originalCodeLine:str):
		super().__init__("For", originalCodeLine)
		self.checkSyntax(originalCodeLine)
		self.loopCount = None

	def checkSyntax(self, originalCodeLine:str):
		if(originalCodeLine[:4] != "for(" or originalCodeLine[-2:] != "):"):
			raise Exception("Invalid syntax for For loop.")

	def solve(self):
		val = self.argumentSyntax(self.originalCodeLine[4:-2], 1)[0]
		self.loopCount = es.solveEquation(val)

	def print(self):
		if(self.loopCount == None):
			print("For (Unsolved): " + str(self.originalCodeLine))
		else:
			print("For: " + str(self.loopCount))

# print()
# varTest = Declaration("var1 = 4*4/8")
# varTest2 = Declaration("var2 = 3/3")
# varTest.print()
# varTest2.print()
# varTest.solve()
# varTest2.solve()
# varTest.print()
# varTest2.print()
# print()

# testString = Declaration("stringVar = \"test \"")
# testString.print()
# testString.solve()
# testString.print()
# print()

# pasteTest = Paste("paste(stringVar + \"this is a stringVar string \" + \"that will get pasted.\")")
# pasteTest.print()
# pasteTest.solve()
# pasteTest.print()
# print()

# highTest = Highlight("highlight(var1/2)")
# highTest.print()
# highTest.solve()
# highTest.print()
# print()

# scTest = StartCursor("startCursor(var1,var2)")
# scTest.print()
# scTest.solve()
# scTest.print()
# print()

# mcTest = MoveCursor("moveCursor(12/3, var1)")
# mcTest.print()
# mcTest.solve()
# mcTest.print()
# print()