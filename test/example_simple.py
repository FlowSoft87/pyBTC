import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import btc

def main():
    #file1 = open("temp.txt",'w')
    serializer = btc.BTagCompound()
    serializer.setInt("someint",2133)
    serializer.setDouble("doub",2.132243)
    serializer.setString("str","hello world!")
    print serializer.toString(0)
    print serializer.getValue("str")
    print serializer.getValue("doub")
    print serializer.getValue("someint")
    #file1.close()

#    file2 = open("temp.txt",'r')
#    print serialization.deserializeByte(file2)
#    print serialization.deserializeShort(file2)
#    print serialization.deserializeInt(file2)
#    print serialization.deserializeLong(file2)
#    print serialization.deserializeIntVar(file2)
#    print serialization.deserializeFloat(file2)
#    print serialization.deserializeString(file2)
#    file2.close()

if __name__ == "__main__":
    main()
