import Reader
import sys



def cSharpWrite(keys):
    with open("C:/Users/hager/Documents/cSharp.txt","w") as f:
        for key in keys:
            f.write(key+"\n")



def formatKeys(hotkeys):
    KeysToBeFormated = ["CTRL_L","CTRL_R","ALT_L","ALT_R","SHIFT_L","SHIFT_R"]
    finalList = []
    for keyset in hotkeys:
        KeyFinal = ""
        for key in keyset:
            if key in KeysToBeFormated:
                keysplit = key.split('_')
                if keysplit[1] == "L":
                    side = "left"
                else:
                    side = "right"
                KeyFinal+= (side+" "+keysplit[0].lower()+"+")
            else:
                KeyFinal+= key.lower()

        #checks for a plus at the end
        if KeyFinal[-1] == "+":
            KeyFinal = KeyFinal[:-1]

        finalList.append(KeyFinal)
    cSharpWrite(finalList)
    return finalList


file = sys.argv[1]

tree = Reader.createCommandTree(file)
HKList = tree.getHKList()

keylist = []
for hotkey in HKList:
    keylist.append(hotkey[0])

keys = formatKeys(keylist) 
