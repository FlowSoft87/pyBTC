import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import btc

def main():
    serializer = btc.BTagCompound()
    serializer.setInt("someint",2133)
    serializer.setDouble("doub",2.132243)
    other_tag = btc.BTagCompound()
    serializer.setTag("other_tag",other_tag)
    serializer.setString("str","hello world!")
    other_tag.setFloat("f_valued",0.324123443e-10)
    other_tag.setDouble("d_valued",0.324123443e-10)
    print serializer.toString(0)
    print serializer.getValue("str")
    print serializer.getValue("doub")
    print serializer.getValue("someint")
    file1 = open("temp.txt",'w')
    serializer.serialize(file1)
    file1.close()

    deserializer = btc.BTagCompound()
    file2 = open("temp.txt",'r')
    deserializer.deserialize(file2)
    file2.close()
    print deserializer.toString(0)
#    print serialization.deserializeByte(file2)
#    print serialization.deserializeShort(file2)
#    print serialization.deserializeInt(file2)
#    print serialization.deserializeLong(file2)
#    print serialization.deserializeIntVar(file2)
#    print serialization.deserializeFloat(file2)
#    print serialization.deserializeString(file2)

if __name__ == "__main__":
    main()
