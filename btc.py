"""
The binary tag coumpound object.
"""

import bisect

import serialization

class DataType:
    """
    Simple enum type.
    """

    COMPOUND = 0
    STRING = 1
    UINT8 = 2
    UINT16 = 3
    UINT32 = 4
    UINT64 = 5
    FLOAT = 6
    DOUBLE = 7
    STRING_ARR = 64
    UINT8_ARR = 65
    UINT16_ARR = 66
    UINT32_ARR = 67
    UINT64_ARR = 68
    FLOAT_ARR = 69
    DOUBLE_ARR = 70

class BTagByte(object):
    """
    BTagBase class for the unsigned char type.
    """

    def __init__(self):
        self.data = 0

    def __init__(self, byte_value):
        self.data = byte_value

    def getTypeID(self):
        return DataType.UINT8

    def serialize(self, outstream):
        serialize.serializeByte(outstream, self.data)

    def deserialize(self, instream):
        self.data = serialize.deserializeByte(instream)

    def toString(self, increment):
        return "b{"+str(self.data)+"}"

class BTagShort(object):
    """
    BTagBase class for the unsigned short type.
    """

    def __init__(self):
        self.data = 0

    def __init__(self, short_value):
        self.data = short_value

    def getTypeID(self):
        return DataType.UINT16

    def serialize(self, outstream):
        serialize.serializeShort(outstream, self.data)

    def deserialize(self, instream):
        self.data = serialize.deserializeShort(instream)

    def toString(self, increment):
        return "s{"+str(self.data)+"}"

class BTagInt(object):
    """
    BTagBase class for the unsigned long type.
    """

    def __init__(self):
        self.data = 0

    def __init__(self, int_value):
        self.data = int_value

    def getTypeID(self):
        return DataType.UINT32

    def serialize(self, outstream):
        serialize.serializeInt(outstream, self.data)

    def deserialize(self, instream):
        self.data = serialize.deserializeInt(instream)

    def toString(self, increment):
        return "i{"+str(self.data)+"}"

class BTagLong(object):
    """
    BTagBase class for the unsigned long long type.
    """

    def __init__(self):
        self.data = 0

    def __init__(self, long_value):
        self.data = long_value

    def getTypeID(self):
        return DataType.UINT64

    def serialize(self, outstream):
        serialize.serializeLong(outstream, self.data)

    def deserialize(self, instream):
        self.data = serialize.deserializeLong(instream)

    def toString(self, increment):
        return "l{"+str(self.data)+"}"

class BTagFloat(object):
    """
    BTagBase class for the float type.
    """

    def __init__(self):
        self.data = 0.

    def __init__(self, float_value):
        self.data = float_value

    def getTypeID(self):
        return DataType.FLOAT

    def serialize(self, outstream):
        serialize.serializeFloat(outstream, self.data)

    def deserialize(self, instream):
        self.data = serialize.deserializeFloat(instream)

    def toString(self, increment):
        return "f{"+str(self.data)+"}"

class BTagDouble(object):
    """
    BTagBase class for the double type.
    """

    def __init__(self):
        self.data = 0.

    def __init__(self, double_value):
        self.data = double_value

    def getTypeID(self):
        return DataType.DOUBLE

    def serialize(self, outstream):
        serialize.serializeDouble(outstream, self.data)

    def deserialize(self, instream):
        self.data = serialize.deserializeDouble(instream)

    def toString(self, increment):
        return "d{"+str(self.data)+"}"

class BTagString(object):
    """
    BTagBase class for the string type.
    """

    def __init__(self):
        self.data = ""

    def __init__(self, string_value):
        self.data = string_value

    def getTypeID(self):
        return DataType.STRING

    def serialize(self, outstream):
        serialize.serializeString(outstream, self.data)

    def deserialize(self, instream):
        self.data = serialize.deserializeString(instream)

    def toString(self, increment):
        return "st{\""+str(self.data)+"\"}"

class BTagCompound(object):
    """
    Binary tag compound class.
    """

    def __init__(self):
        """
        Standard constructor.
        """

        self._tagmap = []
        self._tags = []
        self._datalist = []

    def setTag(self, tag, btag_obj):
        """
        Set key-value pair in the list.
        """

        # Search for the tag
        if (len(self._tagmap) > 0):
            i = bisect.bisect_left(self._tags, tag)
            # Tag exists -> store new value
            if i != len(self._tagmap) and self._tagmap[i][0] == tag:
                self._datalist[self._tagmap[i][1]] = (tag, btag_obj)
                return
        self._tagmap.append((tag, len(self._datalist)))
        self._tags.append(tag)
        if len(self._tagmap) > 1:
            self._tagmap.sort(key=lambda x: x[0])
            for i in range(len(self._tagmap)):
                self._tags[i] = self._tagmap[i][0]
        self._datalist.append((tag, btag_obj))

    def setByte(self, tag, byte_val):
        self.setTag(tag, BTagByte(byte_val))

    def setShort(self, tag, short_val):
        self.setTag(tag, BTagShort(short_val))

    def setInt(self, tag, int_val):
        self.setTag(tag, BTagInt(int_val))

    def setLong(self, tag, long_val):
        self.setTag(tag, BTagLong(long_val))

    def setFloat(self, tag, float_val):
        self.setTag(tag, BTagFloat(float_val))

    def setDouble(self, tag, double_val):
        self.setTag(tag, BTagDouble(double_val))

    def setString(self, tag, string_val):
        self.setTag(tag, BTagString(string_val))

    def getValue(self, tag):
        # Search for the tag
        if (len(self._tagmap) > 0):
            i = bisect.bisect_left(self._tags, tag)
            # Tag exists -> store new value
            if i != len(self._tagmap) and self._tagmap[i][0] == tag:
                return self._datalist[self._tagmap[i][1]][1].data
            else:
                return None
        else:
            return None

    def size(self):
        return len(self._datalist)

    def getTypeID(self):
        return DataType.COMPOUND

    def toString(self, increment):
        rep = "c{"
        if self.size() == 0:
            return rep+'}'
        for i in range(self.size()):
            rep += '\n'
            for j in range((increment+1)*2):
                rep += ' '
            rep += '('+str(i)+",\'"+self._datalist[i][0]+"\'):"
            rep += self._datalist[i][1].toString(increment+1)
        rep += '\n'
        for i in range(increment*2):
            rep += ' '
        rep += "}"
        return rep

