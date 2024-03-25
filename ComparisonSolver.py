from LinkedList import LinkedList
from LinkedList import LinkedListNode
import EquationSolver as es

def isCompOperator(string:str) -> bool:

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

def splitToItems(string:str) -> LinkedList:


	string = string.replace(" ", "")

	subStrings = LinkedList()


	curSubString = ""

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

	if(i == len(string) - 1):
		curSubString += string[i]
	subStrings.append(curSubString)

	if(subStrings.size > 3):
		raise Exception("Item list size cannot currently be longer than 3.")

	return subStrings


def solveItemList(subStrings:LinkedList) -> int:

	curNode = subStrings.head

	index = 0
	while(curNode != None):

		if(isCompOperator(curNode.data)):
			curNode.prevNode.data = es.solveEquation(curNode.prevNode.data)
			curNode.nextNode.data = es.solveEquation(curNode.nextNode.data)

			if(curNode.data == "=="):

				if(curNode.prevNode.data == curNode.nextNode.data):
					curNode.data = "1"
				else:
					curNode.data = "0"

			if(curNode.data == "!="):

				if(curNode.prevNode.data != curNode.nextNode.data):
					curNode.data = "1"
				else:
					curNode.data = "0"

			if(curNode.data == "<="):

				if(curNode.prevNode.data <= curNode.nextNode.data):
					curNode.data = "1"
				else:
					curNode.data = "0"

			if(curNode.data == ">="):

				if(curNode.prevNode.data >= curNode.nextNode.data):
					curNode.data = "1"
				else:
					curNode.data = "0"

			if(curNode.data == "<"):

				if(curNode.prevNode.data < curNode.nextNode.data):
					curNode.data = "1"
				else:
					curNode.data = "0"

			if(curNode.data == ">"):

				if(curNode.prevNode.data > curNode.nextNode.data):
					curNode.data = "1"
				else:
					curNode.data = "0"


			subStrings.remove(index - 1)
			subStrings.remove(index)

			index = index - 1


		curNode = curNode.nextNode
		index = index + 1

	if(subStrings.head.data == "1.0"):
		subStrings.head.data = "1"
	elif(subStrings.head.data == "0.0"):
		subStrings.head.data = "0"

	return(subStrings.head.data)

def solveEquation(eq:str) -> int:

	itemList = splitToItems(eq)
	return solveItemList(itemList)