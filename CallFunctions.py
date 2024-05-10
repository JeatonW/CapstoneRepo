import Reader
import sys




def CallFunction(file):
	tree = Reader.createCommandTree(file)
	tuples = tree.getHKList()
	for t in tuples:
		(hk, tree) = t
		hktuples = tree.solve()
		print()
		print(hk)
		for h in hktuples:
			print(h)
	




try:
	file = sys.argv[1]
	CallFunction(file)


except Exception as e:
	print(e)
	print("error")