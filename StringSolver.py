from LinkedList import LinkedList
from LinkedList import LinkedListNode

#reads the line of code, evaluates syntax, puts each sub string into an element in a linked list
def splitToItems(string:str) -> LinkedList:

	#string addition cannot begin without quotations
	firstIndex = 0
	for c in string:

		#ignore spaces
		if(ord(c) == 32):
			pass

		elif(ord(c) == 34):
			break

		else:
			raise Exception("Expected opening quotations before first string.")

		firstIndex = firstIndex + 1

	#remove spaces before first quotation
	string = string[firstIndex:]

	#create the list for all strings to be added
	subStrings = LinkedList()

	#the current string being recorded
	curString = ""

	#inside/outside of quotations
	inString = False

	#whether or not addition operator has been found outside of quotations
	addFound = True

	#evaluate every ascii value in the string
	index = 0
	for c in string:
		asciiVal = ord(c)

		#found open quotations, begin recording string inside
		if(asciiVal == 34 and not inString and addFound):
			inString = True
			addFound = False

		#found end quotations, reset string and stop recording string
		# \" < means quotation is apart of string; skip these
		elif(asciiVal == 34 and inString and ord(string[index-1]) != 92):
			subStrings.append(curString)
			inString = False
			curString = ""

		#currently inside quotations, record each character
		elif(inString):
			curString = curString + c

		#currently outside quotations, deal with operators
		elif(not inString):

			#ignore spaces
			if(asciiVal == 32):
				pass

			#quotation was found before addition operator
			elif(asciiVal == 34):
				raise Exception("Expected addition operators in between strings.")

			#plus sign was found
			elif(asciiVal == 43 and not addFound):
				addFound = True

			#more than one plus sign is not allowed
			elif(asciiVal == 43 and addFound):
				raise Exception("Expected string in between operators.")

			#other characters are not allowed
			else:
				raise Exception("Only addition operators allowed outside of quotations.")

		index = index + 1

	#quotations never closed
	if(inString):
		raise Exception("Expected closing quotations after last string.")

	#original string ends with an addition operator
	if(addFound):
		raise Exception("Expected string after last addition operator.")

	return subStrings

#combines all substrings from the linked list into one string
def combineItems(subStrings:LinkedList) -> str:

	combinedString = ""

	curNode = subStrings.head
	while(curNode != None):
		combinedString = combinedString + curNode.data
		curNode = curNode.nextNode

	return combinedString

#performs all necessary methods in order to solve a string
def solveString(string:str) -> str:
	itemList = splitToItems(string)
	return combineItems(itemList)

#string = "\"This is a string. \" + \"And another one. \" + \"And a third for good measure. \" + \"\\\"This string has quotations\\\"\""
#print(solveString(string))