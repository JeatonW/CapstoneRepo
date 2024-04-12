from LinkedList import LinkedList
from LinkedList import LinkedListNode
import EquationSolver as es

#returns true if the string is a comparison operator
def isCompOperator(string:str) -> bool:

	string = str(string)

	if(len(string) == 1):

		match(string[0]):
			case "<":
				return True
			case ">":
				return True
			case _:
				return False

	elif(len(string) == 2):

		match(string):
			case "==":
				return True
			case "!=":
				return True
			case "<=":
				return True
			case ">=":
				return True
			case _:
				return False

	return False

#splits the string into a list of items. values and operators are items.
def splitToItems(string:str) -> LinkedList:

	#destroy spaces
	string = string.replace(" ", "")

	#create a list for all items
	subStrings = LinkedList()

	#current string being recorded
	curSubString = ""

	#read each character. if it is an operator, then add the curSubString as well as the operator
	#to the linked list of substrings. operators can be one or two characters long, so account for that
	i = 0
	while(i < len(string) - 1):
		if(isCompOperator(string[i] + string[i+1])):
			subStrings.append(curSubString)
			subStrings.append(string[i] + string[i+1])
			curSubString = ""
			i = i + 1
		else:
			if(isCompOperator(string[i])):
				subStrings.append(curSubString)
				subStrings.append(string[i])
				curSubString = ""
			else:
				curSubString += string[i]
		i = i + 1

	#if we reached the end of the string, then add the current substring to the list
	if(i == len(string) - 1):
		curSubString += string[i]
	subStrings.append(curSubString)

	#comparisons require an odd number of items to be valid syntax
	#i.e. "3 ==" is invalid, "4 > 3 >" is invalid etc
	if(subStrings.size % 2 != 1):
		raise Exception("Invalid comparison syntax.")

	#odd number elements in the list must not be operators
	#even number elements must be operators
	#ex comparison: "4 > 3 > 2"
	#                1 2 3 4 5
	#                O E O E O
	subStrIndex = 0
	curNode = subStrings.head
	while(curNode != None):
		if(subStrIndex % 2 == 0):
			if(isCompOperator(curNode.data)):
				raise Exception("Invalid comparison syntax.")
		else:
			if(not isCompOperator(curNode.data)):
				raise Exception("Invalid comparison syntax.")
		subStrIndex = subStrIndex + 1
		curNode = curNode.nextNode

	#return the final list of items/substrings
	return subStrings

#solves the list of items. returns a 0 or 1 if the comparison string is true
def solveItemList(subStrings:LinkedList) -> int:

	#figure out how many comparisons are being made
	numOfComparisons = int((subStrings.size - 1) / 2)

	#this is the list of outcomes for each comparison
	outcomes = []

	#we start at the second node
	curNode = subStrings.head.nextNode

	#evaluate a comparison at every even numbered element position (all comparison operators)
	for c in range(0, numOfComparisons):

		#hopefully this code never runs
		if(not isCompOperator(curNode.data) or isCompOperator(curNode.prevNode.data) or isCompOperator(curNode.nextNode.data)):
			raise Exception("Invalid syntax for comparison solver; misaligned elements.")

		#solve the non operators
		curNode.prevNode.data = es.solveEquation(str(curNode.prevNode.data))
		curNode.nextNode.data = es.solveEquation(str(curNode.nextNode.data))

		#perform comparison and record the outcome
		if(curNode.data == "=="):
			if(curNode.prevNode.data == curNode.nextNode.data):
				outcomes.append("1")
			else:
				outcomes.append("0")
		if(curNode.data == "!="):
			if(curNode.prevNode.data != curNode.nextNode.data):
				outcomes.append("1")
			else:
				outcomes.append("0")
		if(curNode.data == "<="):
			if(curNode.prevNode.data <= curNode.nextNode.data):
				outcomes.append("1")
			else:
				outcomes.append("0")
		if(curNode.data == ">="):
			if(curNode.prevNode.data >= curNode.nextNode.data):
				outcomes.append("1")
			else:
				outcomes.append("0")
		if(curNode.data == "<"):
			if(curNode.prevNode.data < curNode.nextNode.data):
				outcomes.append("1")
			else:
				outcomes.append("0")
		if(curNode.data == ">"):
			if(curNode.prevNode.data > curNode.nextNode.data):
				outcomes.append("1")
			else:
				outcomes.append("0")

		#move up 2 nodes to the next operator (last comparison does not have a next operator; dont nullpoint)
		curNode = curNode.nextNode
		if(curNode != None):
			curNode = curNode.nextNode

	#if any zeroes are found, comparison is false
	for o in outcomes:
		if(o == "0"):
			return "0"

	#if no zeroes were found, comparison is true
	return "1"

#split the comparison string by the keyword "or". solve each of the substrings
#separately, and if any are true, return 1 otherwise 0
def splitByAnd(eq:str) -> str:

	#split string
	comparisonList = eq.split("and")

	#solve each substring using splitByAnd()
	compIndex = 0
	for s in comparisonList:
		comparisonList[compIndex] = splitByOr(s)
		compIndex = compIndex + 1

	#if any substring results in a 0, return 0
	for i in comparisonList:
		if (i == "0"):
			return "0"

	#if no substring results in a 0, return 1
	return "1"

#split the comparison string by the keyword "and". solve each of the substrings
#separately, and if any are false, return 0 otherwise 1
def splitByOr(eq:str) -> str:

	#split string
	comparisonList = eq.split("or")
	solvedItemList = []

	#solve each substring using solveItemList(splitToItems())
	compIndex = 0
	for s in comparisonList:
		comparisonList[compIndex] = solveItemList(splitToItems(s))

	#if any substring results in a 1, return 1
	for i in comparisonList:
		if(i == "1"):
			return "1"

	#if no substring results in a 1, return 0
	return "0"

#takes in a comparison string, returns a 1 or a 0
def solveEquation(eq:str) -> int:
	return splitByAnd(eq)

#print(solveEquation(input("Input comparison string: ")))
#print(solveItemList(splitToItems(input("input comp string: "))))
