"""
The binary tag coumpound object.
"""

import bisect

from pyBTC.serialization import *

class DataType(object):
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

class ABTag(object):
    """
    Abstract base class of all BTag objects.
    """

    def __init__(self, obj_value):
        self._data = obj_value

    def get_type_id(self):
        """
        Get the identifier for the data type.
        """

        raise Exception("Not implemented!"+self.__class__)

    def get_data(self):
        """
        Get the data wrapped by this object.
        """

        return self._data

    def serialize(self, out_stream):
        """
        Serialize the object to the stream.
        """

        raise Exception("Not implemented!"+self.__class__)

    def deserialize(self, instream):
        """
        Deserialize the object from stream.
        """

        raise Exception("Not implemented!"+self.__class__)

    def to_string(self, increment):
        """
        Get a string representation of the object.
        """

        raise Exception("Not implemented!"+self.__class__)

class BTagByte(ABTag):
    """
    BTagBase class for the unsigned char type.
    """

    def __init__(self, byte_value=0):
        super(BTagByte, self).__init__(byte_value)

    def get_type_id(self):
        return DataType.UINT8

    def serialize(self, outstream):
        serializeByte(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeByte(instream)

    def to_string(self, increment):
        return "b{"+str(self._data)+"}"

    def __str__(self):
        return self.to_string(0)

class BTagShort(ABTag):
    """
    BTagBase class for the unsigned short type.
    """

    def __init__(self, short_value=0):
        super(BTagShort, self).__init__(short_value)

    def get_type_id(self):
        return DataType.UINT16

    def serialize(self, outstream):
        serializeShort(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeShort(instream)

    def to_string(self, increment):
        return "s{"+str(self._data)+"}"

    def __str__(self):
        return self.to_string(0)

class BTagInt(ABTag):
    """
    BTagBase class for the unsigned long type.
    """

    def __init__(self, int_value=0):
        super(BTagInt, self).__init__(int_value)

    def get_type_id(self):
        return DataType.UINT32

    def serialize(self, outstream):
        serializeInt(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeInt(instream)

    def to_string(self, increment):
        return "i{"+str(self._data)+"}"

    def __str__(self):
        return self.to_string(0)

class BTagLong(ABTag):
    """
    BTagBase class for the unsigned long long type.
    """

    def __init__(self, long_value=0):
        super(BTagLong, self).__init__(long_value)

    def get_type_id(self):
        return DataType.UINT64

    def serialize(self, outstream):
        serializeLong(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeLong(instream)

    def to_string(self, increment):
        return "l{"+str(self._data)+"}"

    def __str__(self):
        return self.to_string(0)

class BTagFloat(ABTag):
    """
    BTagBase class for the float type.
    """

    def __init__(self, float_value=0.):
        super(BTagFloat, self).__init__(float_value)

    def get_type_id(self):
        return DataType.FLOAT

    def serialize(self, outstream):
        serializeFloat(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeFloat(instream)

    def to_string(self, increment):
        return "f{"+str(self._data)+"}"

    def __str__(self):
        return self.to_string(0)

class BTagDouble(ABTag):
    """
    BTagBase class for the double type.
    """

    def __init__(self, double_value=0.):
        super(BTagDouble, self).__init__(double_value)

    def get_type_id(self):
        return DataType.DOUBLE

    def serialize(self, outstream):
        serializeDouble(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeDouble(instream)

    def to_string(self, increment):
        return "d{"+str(self._data)+"}"

    def __str__(self):
        return self.to_string(0)

class BTagString(ABTag):
    """
    BTagBase class for the string type.
    """

    def __init__(self, string_value=""):
        super(BTagString, self).__init__(string_value)

    def get_type_id(self):
        return DataType.STRING

    def serialize(self, outstream):
        serializeString(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeString(instream)

    def to_string(self, increment):
        return "st{\""+str(self._data)+"\"}"

    def __str__(self):
        return self.to_string(0)

class BTagByteArr(ABTag):
    """
    BTagBase class for the unsigned char* type.
    """

    def __init__(self, byte_array=[]):
        super(BTagByteArr, self).__init__(byte_array)

    def get_type_id(self):
        return DataType.UINT8_ARR

    def serialize(self, outstream):
        serializeByteArray(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeByteArray(instream)

    def to_string(self, increment):
        return "ba{len="+str(len(self._data))+"}"

    def __str__(self):
        return self.to_string(0)

class BTagShortArr(ABTag):
    """
    BTagBase class for the unsigned short type.
    """

    def __init__(self, short_array=[]):
        super(BTagShortArr, self).__init__(short_array)

    def get_type_id(self):
        return DataType.UINT16_ARR

    def serialize(self, outstream):
        serializeShortArray(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeShortArray(instream)

    def to_string(self, increment):
        return "sa{len="+str(len(self._data))+"}"

    def __str__(self):
        return self.to_string(0)

class BTagIntArr(ABTag):
    """
    BTagBase class for the unsigned long type.
    """

    def __init__(self, int_array=[]):
        super(BTagIntArr, self).__init__(int_array)

    def get_type_id(self):
        return DataType.UINT32_ARR

    def serialize(self, outstream):
        serializeIntArray(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeIntArray(instream)

    def to_string(self, increment):
        return "ia{len="+str(len(self._data))+"}"

    def __str__(self):
        return self.to_string(0)

class BTagLongArr(ABTag):
    """
    BTagBase class for the unsigned long long type.
    """

    def __init__(self, long_array=[]):
        super(BTagLongArr, self).__init__(long_array)

    def get_type_id(self):
        return DataType.UINT64_ARR

    def serialize(self, outstream):
        serializeLongArray(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeLongArray(instream)

    def to_string(self, increment):
        return "la{len="+str(len(self._data))+"}"

    def __str__(self):
        return self.to_string(0)

class BTagFloatArr(ABTag):
    """
    BTagBase class for the float type.
    """

    def __init__(self, float_array=[]):
        super(BTagFloatArr, self).__init__(float_array)

    def get_type_id(self):
        return DataType.FLOAT_ARR

    def serialize(self, outstream):
        serializeFloatArray(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeFloatArray(instream)

    def to_string(self, increment):
        return "fa{len="+str(len(self._data))+"}"

    def __str__(self):
        return self.to_string(0)

class BTagDoubleArr(ABTag):
    """
    BTagBase class for the double type.
    """

    def __init__(self, double_array=[]):
        super(BTagDoubleArr, self).__init__(double_array)

    def get_type_id(self):
        return DataType.DOUBLE_ARR

    def serialize(self, outstream):
        serializeDoubleArray(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeDoubleArray(instream)

    def to_string(self, increment):
        return "da{len="+str(len(self._data))+"}"

    def __str__(self):
        return self.to_string(0)

class BTagStringArr(ABTag):
    """
    BTagBase class for the string type.
    """

    def __init__(self, string_array=[]):
        super(BTagStringArr, self).__init__(string_array)

    def get_type_id(self):
        return DataType.STRING_ARR

    def serialize(self, outstream):
        serializeStringArray(outstream, self._data)

    def deserialize(self, instream):
        self._data = deserializeStringArray(instream)

    def to_string(self, increment):
        return "sta{len="+str(len(self._data))+"}"

    def __str__(self):
        return self.to_string(0)

class BTagCompound(ABTag):
    """
    Binary tag compound class.
    """

    def __init__(self):
        super(BTagCompound, self).__init__([])
        self._tagmap = []
        self._tags = []

    def setTag(self, tag, btag_obj):
        """
        Set key-value pair in the list.
        """

        # Search for the tag
        if (len(self._tagmap) > 0):
            i = bisect.bisect_left(self._tags, tag)
            # Tag exists -> store new value
            if i != len(self._tagmap) and self._tagmap[i][0] == tag:
                self._data[self._tagmap[i][1]] = (tag, btag_obj)
                return
        self._tagmap.append((tag, len(self._data)))
        self._tags.append(tag)
        if len(self._tagmap) > 1:
            self._tagmap.sort(key=lambda x: x[0])
            for i in range(len(self._tagmap)):
                self._tags[i] = self._tagmap[i][0]
        self._data.append((tag, btag_obj))

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

    def setByteArray(self, tag, byte_arr):
        self.setTag(tag, BTagByteArr(byte_arr))

    def setShortArray(self, tag, short_arr):
        self.setTag(tag, BTagShortArr(short_arr))

    def setIntArray(self, tag, int_arr):
        self.setTag(tag, BTagIntArr(int_arr))

    def setLongArray(self, tag, long_arr):
        self.setTag(tag, BTagLongArr(long_arr))

    def setFloatArray(self, tag, float_arr):
        self.setTag(tag, BTagFloatArr(float_arr))

    def setDoubleArray(self, tag, double_arr):
        self.setTag(tag, BTagDoubleArr(double_arr))

    def setStringArray(self, tag, string_arr):
        self.setTag(tag, BTagStringArr(string_arr))

    def getTag(self, tag):
        # Search for the tag
        if (len(self._tagmap) > 0):
            i = bisect.bisect_left(self._tags, tag)
            # Tag exists -> store new value
            if i != len(self._tagmap) and self._tagmap[i][0] == tag:
                return self._data[self._tagmap[i][1]][1]
            else:
                return None
        else:
            return None

    def getEntry(self, tag):
        result = self.getTag(tag)
        if result != None:
            return result.data
        return result

    def size(self):
        return len(self._data)

    def items(self):
        return self._data

    def get_type_id(self):
        return DataType.COMPOUND

    def serialize(self, outstream):
        # Serialize number of data entries
        serializeIntVar(outstream, len(self._data))
        for dataobj in self._data:
            # Tag
            serializeString8(outstream, dataobj[0])
            # Data type
            serializeByte(outstream, dataobj[1].get_type_id())
            # Object
            dataobj[1].serialize(outstream)

    def deserialize(self, instream):
        data_len = deserializeIntVar(instream)
        type_temp = 0
        for i in range(data_len):
            tag = deserializeString8(instream)
            type_temp = deserializeByte(instream)
            if type_temp == DataType.COMPOUND:
                self._data.append((tag, BTagCompound()))
            elif type_temp == DataType.STRING:
                self._data.append((tag, BTagString()))
            elif type_temp == DataType.UINT8:
                self._data.append((tag, BTagByte()))
            elif type_temp == DataType.UINT16:
                self._data.append((tag, BTagShort()))
            elif type_temp == DataType.UINT32:
                self._data.append((tag, BTagInt()))
            elif type_temp == DataType.UINT64:
                self._data.append((tag, BTagLong()))
            elif type_temp == DataType.FLOAT:
                self._data.append((tag, BTagFloat()))
            elif type_temp == DataType.DOUBLE:
                self._data.append((tag, BTagDouble()))
            elif type_temp == DataType.STRING_ARR:
                self._data.append((tag, BTagStringArr()))
            elif type_temp == DataType.UINT8_ARR:
                self._data.append((tag, BTagByteArr()))
            elif type_temp == DataType.UINT16_ARR:
                self._data.append((tag, BTagShortArr()))
            elif type_temp == DataType.UINT32_ARR:
                self._data.append((tag, BTagIntArr()))
            elif type_temp == DataType.UINT64_ARR:
                self._data.append((tag, BTagLongArr()))
            elif type_temp == DataType.FLOAT_ARR:
                self._data.append((tag, BTagFloatArr()))
            elif type_temp == DataType.DOUBLE_ARR:
                self._data.append((tag, BTagDoubleArr()))
            self._tagmap.append((tag, len(self._data)-1))
            self._tags.append(tag)
            self._data[-1][1].deserialize(instream)
        if len(self._tagmap) > 1:
            self._tagmap.sort(key=lambda x: x[0])
            for i in range(len(self._tagmap)):
                self._tags[i] = self._tagmap[i][0]

    def to_string(self, increment):
        rep = "c{"
        if self.size() == 0:
            return rep+'}'
        for i in range(self.size()):
            rep += '\n'
            for j in range((increment+1)*2):
                rep += ' '
            rep += '('+str(i)+",\'"+self._data[i][0]+"\'):"
            rep += self._data[i][1].to_string(increment+1)
        rep += '\n'
        for i in range(increment*2):
            rep += ' '
        rep += "}"
        return rep

    def __str__(self):
        return self.to_string(0)

