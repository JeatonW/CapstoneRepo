import Reader
import sys




def CallFunction(file):
	tree = Reader.createCommandTree(file)
	tree.solveAndPrint()
	




try:
	file = sys.argv[1]
	CallFunction(file)


except Exception as e:
	print(e)
	print("error")