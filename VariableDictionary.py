class VariableDictionary:

	varDict = {}

	def __init__(self):
		self.varDict["false"] = 0
		self.varDict["true"] = 1

	def getKeyList(self) -> list:
		return list(self.varDict.keys())

	def set(self, variable:str, value):
		self.varDict[variable] = value

	def get(self, variable:str):
		return self.varDict[variable]

	def remove(self, variable):
		del self.varDict[variable]

	def contains(self, variable) -> bool:
		if(variable in self.varDict):
			return True
		return False

	def getType(self, variable:str) -> str:
		if(self.isStrNum(self.varDict[variable])):
			return "Float"
		else:
			return "String"

	def print(self):
		for e in self.varDict:
			print(e, end=" = ")
			print(self.varDict[e])

	#returns true if an entire string is made up of numbers
	def isStrNum(self, string:str) -> bool:

		string = str(string)

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