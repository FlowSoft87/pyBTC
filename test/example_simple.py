import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import btc.serialization

def main():
    file1 = open("temp.txt",'w')
    btc.serialization.serializeByte(file1,23)
    btc.serialization.serializeShort(file1,23)
    btc.serialization.serializeInt(file1,23)
    btc.serialization.serializeLong(file1,2329234143422)
    btc.serialization.serializeIntVar(file1,23422)
    btc.serialization.serializeFloat(file1,0.753823472348243823583459435993543e-12)
    file1.close()

    file2 = open("temp.txt",'r')
    print btc.serialization.deserializeByte(file2)
    print btc.serialization.deserializeShort(file2)
    print btc.serialization.deserializeInt(file2)
    print btc.serialization.deserializeLong(file2)
    print btc.serialization.deserializeIntVar(file2)
    print btc.serialization.deserializeFloat(file2)
    file2.close()

if __name__ == "__main__":
    main()
