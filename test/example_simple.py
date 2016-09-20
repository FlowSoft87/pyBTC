import os
import sys
import numpy

sys.path.insert(0, os.path.abspath('..'))
import btc

def main():
    serializer = btc.BTagCompound()
    serializer.setInt("someint",2133)
    serializer.setDouble("doub",2.132243)
    other_tag = btc.BTagCompound()
    serializer.setTag("other_tag",other_tag)
    serializer.setString("str","hello world!")
    other_tag.setFloat("f_valued",numpy.float32(0.324123443e-10))
    other_tag.setDouble("d_valued",numpy.float64(0.324123443e-10))
    intarray = range(10)
    other_tag.setIntArray("longarr",intarray)
    print serializer
    print serializer.getEntry("str")
    print serializer.getEntry("doub")
    print serializer.getEntry("someint")
    print other_tag.getEntry("f_valued")
    file1 = open("temp.txt",'w')
    serializer.serialize(file1)
    file1.close()

    deserializer = btc.BTagCompound()
    file2 = open("temp.txt",'r')
    deserializer.deserialize(file2)
    file2.close()
    print deserializer
    print deserializer.getTag("other_tag")
    print type(deserializer.getTag("other_tag").getEntry("longarr")[0])
#    print serialization.deserializeByte(file2)
#    print serialization.deserializeShort(file2)
#    print serialization.deserializeInt(file2)
#    print serialization.deserializeLong(file2)
#    print serialization.deserializeIntVar(file2)
#    print serialization.deserializeFloat(file2)
#    print serialization.deserializeString(file2)

if __name__ == "__main__":
    main()
