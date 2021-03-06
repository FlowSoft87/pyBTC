"""
Fundamental serialization functions for the primitive types.
"""

import math

# Check numpy availability
ASSERT_NUMPY = True
try:
    import numpy
except ImportError:
    ASSERT_NUMPY = False

def serializeByte(outstream, byte):
    """
    Serialize a single byte.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        byte: Integer value in the range (0 <= byte < 255).
    """

    outstream.write(chr(byte))

def deserializeByte(instream):
    """
    Deserialize a single byte.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    return int(instream.read(1).encode('hex'), 16)

def serializeShort(outstream, short_integer):
    """
    Serialize a short integer.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        short_integer: Integer value in the range (0 <= byte < 65536).
    """

    data = int(short_integer)
    serializeByte(outstream,data%256)
    serializeByte(outstream,data/256)

def deserializeShort(instream):
    """
    Deserialize a short integer.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    data = deserializeByte(instream)
    data += deserializeByte(instream)*256
    return data

def serializeInt(outstream, integer):
    """
    Serialize an integer.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        integer: Integer value in the range (0 <= byte < 4294967296).
    """

    data = long(integer)
    serializeShort(outstream, data%65536)
    serializeShort(outstream, data/65536)

def deserializeInt(instream):
    """
    Deserialize an integer.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    data = long(deserializeShort(instream))
    data += long(deserializeShort(instream))*65536
    return(data)

def serializeLong(outstream, long_integer):
    """
    Serialize a long integer.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        long_integer: Integer value in the range (0 <= byte < 2^64).
    """

    data = long(long_integer)
    serializeInt(outstream, data%4294967296)
    serializeInt(outstream, data/4294967296)

def deserializeLong(instream):
    """
    Deserialize an integer.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    data = long(deserializeInt(instream))
    data += long(deserializeInt(instream))*4294967296
    return(data)

def serializeIntVar(outstream, int_val):
    """
    Serialize an arbitrary integer of maximum size of 8 byte.
    Depending on how large the number is the correct representation is chosen.
    For this purpose an extra byte is stored in front of the number which tells 
    of what type the representation is.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        int_val: Integer value in the range (0 <= byte < 2^64).
    """

    if int_val <= 256:
        serializeByte(outstream,0)
        serializeByte(outstream,int_val)
    elif (int_val > 256) and (int_val <= 65536):
        serializeByte(outstream,1)
        serializeShort(outstream,int_val)
    elif (int_val > 65536) and (int_val <= 4294967296):
        serializeByte(outstream,2)
        serializeInt(outstream,int_val)
    else:
        serializeByte(outstream,3)
        serializeLong(outstream,int_val)

def deserializeIntVar(instream):
    type_val = deserializeByte(instream)
    if type_val == 0:
        return deserializeByte(instream)
    elif type_val == 1:
        return deserializeShort(instream)
    elif type_val == 2:
        return deserializeInt(instream)
    else:
        return deserializeLong(instream)

def serializeFloat(outstream, float_val):
    """
     * Serialize a floating point number of size 4 byte.
     * The number is decomposed numerically and stored in a uint32_t variable
     * in the format |s|exp|mant| where s is 1 bit, exp is 8 bits and mant
     * 23 bits long.
     * It is then serialized as a uint32_t to get rid of byte order issues.
    """

    data = long(0)
    mant, exp = math.frexp(float_val)
    # Write sign
    if (mant < 0):
        mant = -mant
        data += 2147483648L  # Set bit 31: 2^31
    exp += 127
    # Special cases
    # TODO Eliminate the dependence on the limits include (Flo)
    if float_val == 0:
        mant = 0.5
        exp = 255
    elif math.isinf(float_val):
        # Handle inf case
        mant = 0.75
        exp = 255
    elif(math.isnan(float_val)):
        # Handle quiet NaN case
        mant = 0.875
        exp = 255
    # Write exponent
    data += exp*8388608L  # Set bits 23-30: 2^23
    # Write mantissa
    mant -= 0.5  # Subtract hidden bit
    data += int(mant*16777216.)  # Set bits 0-22: (0 <= mant < 0.5)
    serializeInt(outstream,data)

def deserializeFloat(instream):
    """
    Deserialize a floating point number of size 4 byte.
    """

    data = deserializeInt(instream)
    val = 0.5
    # Get sign
    s = data/2147483648L
    data %= 2147483648L
    # Get exponent
    exp = data/8388608L
    data %= 8388608L
    # Get mantissa
    val += (float(data))/16777216.
    # Special cases
    if (val == 0.5) and (exp == 255):
        # Handle zero case
        if(s == 1):
            val = -0.
        else:
            val = 0.
        return val
    elif (val == 0.75) and (exp == 255):
        # Handle inf case
        if(s == 1):
            val = -float('inf')
        else:
            val = float('inf')
        return val
    elif (val == 0.875) and (exp == 255):
        # Handle quiet NaN case
        if (s == 1):
            val = -float('nan')
        else:
            val = float('nan')
        return val
    # Normal number
    if (s == 1):
        val = -val
    exp -= 127
    # Multiply them together
    val = math.ldexp(val,exp)
    return(val)

def serializeDouble(outstream, double_val):
    """
     * Serialize a floating point number of size 8 byte.
     * The number is decomposed numerically and stored in a uint32_t variable
     * in the format |s|exp|mant| where s is 1 bit, exp is 11 bits and mant
     * 52 bits long.
     * It is then serialized as a uint64_t to get rid of byte order issues.
    """

    data = long(0)
    mant, exp = math.frexp(double_val)
    # Write sign
    if (mant < 0):
        mant = -mant
        data += 9223372036854775808L  # Set bit 31: 2^63
    exp += 1023
    # Special cases
    # TODO Eliminate the dependence on the limits include (Flo)
    if double_val == 0:
        mant = 0.5
        exp = 2047
    elif math.isinf(double_val):
        # Handle inf case
        mant = 0.75
        exp = 2047
    elif(math.isnan(double_val)):
        # Handle quiet NaN case
        mant = 0.875
        exp = 2047
    # Write exponent
    data += long(exp)*4503599627370496L  # Set bits 52-62: 2^52
    # Write mantissa
    mant -= 0.5  # Subtract hidden bit
    data += long(mant*9007199254740992.)  # Set bits 0-51: (0 <= mant < 0.5)
    serializeLong(outstream,data)

def deserializeDouble(instream):
    """
    Deserialize a floating point number of size 8 byte.
    """

    data = deserializeLong(instream)
    val = 0.5
    # Get sign
    s = data/9223372036854775808L
    data %= 9223372036854775808L
    # Get exponent
    exp = data/4503599627370496L
    data %= 4503599627370496L
    # Get mantissa
    val += (float(data))/9007199254740992.
    # Special cases
    if (val == 0.5) and (exp == 2047):
        # Handle zero case
        if(s == 1):
            val = -0.
        else:
            val = 0.
        return val
    elif (val == 0.75) and (exp == 2047):
        # Handle inf case
        if(s == 1):
            val = -float('inf')
        else:
            val = float('inf')
        return val
    elif (val == 0.875) and (exp == 2047):
        # Handle quiet NaN case
        if (s == 1):
            val = -float('nan')
        else:
            val = float('nan')
        return val
    # Normal number
    if (s == 1):
        val = -val
    exp -= 1023
    # Multiply them together
    val = math.ldexp(val,exp)
    return(val)

def serializeString8(outstream, string):
    """
    Serialize a string with a length in the range (0 <= len < 256).
    """

    serializeByte(outstream, len(string))
    outstream.write(string)

def deserializeString8(instream):
    """
    Deserialize a string with a length in the range (0 <= len < 256).
    """

    string_len = deserializeByte(instream)
    return instream.read(string_len)

def serializeString16(outstream, string):
    """
    Serialize a string with a length in the range (0 <= len < 2^16).
    """

    serializeShort(outstream, len(string))
    outstream.write(string)

def deserializeString16(instream):
    """
    Deserialize a string with a length in the range (0 <= len < 2^16).
    """

    string_len = deserializeShort(instream)
    return instream.read(string_len)

def serializeString32(outstream, string):
    """
    Serialize a string with a length in the range (0 <= len < 2^32).
    """

    serializeInt(outstream, len(string))
    outstream.write(string)

def deserializeString32(instream):
    """
    Deserialize a string with a length in the range (0 <= len < 2^32).
    """

    string_len = deserializeInt(instream)
    return instream.read(string_len)

def serializeString64(outstream, string):
    """
    Serialize a string with a length in the range (0 <= len < 2^64).
    """

    serializeLong(outstream, len(string))
    outstream.write(string)

def deserializeString64(instream):
    """
    Deserialize a string with a length in the range (0 <= len < 2^64).
    """

    string_len = deserializeLong(instream)
    return instream.read(string_len)

def serializeString(outstream, string):
    """
    Serialize a string with a length in the range (0 <= len < 256).
    """

    serializeIntVar(outstream, len(string))
    outstream.write(string)

def deserializeString(instream):
    """
    Deserialize a string with a length in the range (0 <= len < 256).
    """

    string_len = deserializeIntVar(instream)
    return instream.read(string_len)

def serializeByteArray(outstream, byte_arr):
    """
    Serialize a single byte.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        byte: Integer value in the range (0 <= byte < 255).
    """

    serializeIntVar(outstream, len(byte_arr))
    for x in byte_arr:
        serializeByte(outstream, x)

def deserializeByteArray(instream):
    """
    Deserialize a single byte.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    array_len = deserializeIntVar(instream)
    array = None
    if ASSERT_NUMPY:
        array = numpy.empty(array_len, dtype=numpy.uint8)
    else:
        array = [None]*array_len
    for i in range(array_len):
        array[i] = deserializeByte(instream)
    return array

def serializeShortArray(outstream, short_arr):
    """
    Serialize a short integer.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        short_integer: Integer value in the range (0 <= byte < 65536).
    """

    serializeIntVar(outstream, len(short_arr))
    for x in short_arr:
        serializeShort(outstream, x)

def deserializeShortArray(instream):
    """
    Deserialize a short integer.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    array_len = deserializeIntVar(instream)
    array = None
    if ASSERT_NUMPY:
        array = numpy.empty(array_len, dtype=numpy.uint16)
    else:
        array = [None]*array_len
    for i in range(array_len):
        array[i] = deserializeShort(instream)
    return array

def serializeIntArray(outstream, integer_arr):
    """
    Serialize an integer.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        integer: Integer value in the range (0 <= byte < 4294967296).
    """

    serializeIntVar(outstream, len(integer_arr))
    for x in integer_arr:
        serializeInt(outstream, x)

def deserializeIntArray(instream):
    """
    Deserialize an integer.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    array_len = deserializeIntVar(instream)
    array = None
    if ASSERT_NUMPY:
        array = numpy.empty(array_len, dtype=numpy.uint32)
    else:
        array = [None]*array_len
    for i in range(array_len):
        array[i] = deserializeInt(instream)
    return array

def serializeLongArray(outstream, long_arr):
    """
    Serialize a long integer.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        long_integer: Integer value in the range (0 <= byte < 2^64).
    """

    serializeIntVar(outstream, len(long_arr))
    for x in long_arr:
        serializeLong(outstream, x)

def deserializeLongArray(instream):
    """
    Deserialize an integer.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    array_len = deserializeIntVar(instream)
    array = None
    if ASSERT_NUMPY:
        array = numpy.empty(array_len, dtype=numpy.uint64)
    else:
        array = [None]*array_len
    for i in range(array_len):
        array[i] = deserializeLong(instream)
    return array

def serializeFloatArray(outstream, float_arr):
    """
    Serialize a long integer.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        long_integer: Integer value in the range (0 <= byte < 2^64).
    """

    serializeIntVar(outstream, len(float_arr))
    for x in float_arr:
        serializeFloat(outstream, x)

def deserializeFloatArray(instream):
    """
    Deserialize an integer.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    array_len = deserializeIntVar(instream)
    array = None
    if ASSERT_NUMPY:
        array = numpy.empty(array_len, dtype=numpy.float32)
    else:
        array = [None]*array_len
    for i in range(array_len):
        array[i] = deserializeFloat(instream)
    return array

def serializeDoubleArray(outstream, double_arr):
    """
    Serialize a long integer.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        long_integer: Integer value in the range (0 <= byte < 2^64).
    """

    serializeIntVar(outstream, len(double_arr))
    for x in double_arr:
        serializeDouble(outstream, x)

def deserializeDoubleArray(instream):
    """
    Deserialize an integer.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    array_len = deserializeIntVar(instream)
    array = None
    if ASSERT_NUMPY:
        array = numpy.empty(array_len, dtype=numpy.float64)
    else:
        array = [None]*array_len
    for i in range(array_len):
        array[i] = deserializeDouble(instream)
    return array

def serializeStringArray(outstream, string_arr):
    """
    Serialize a long integer.

    Args:
        outstream: Stream object inheriting (io.RawIOBase).
        long_integer: Integer value in the range (0 <= byte < 2^64).
    """

    serializeIntVar(outstream, len(string_arr))
    for x in string_arr:
        serializeString(outstream, x)

def deserializeStringArray(instream):
    """
    Deserialize an integer.

    Args:
        instream: Stream object inheriting (io.RawIOBase).
    """

    array_len = deserializeIntVar(instream)
    array = [None]*array_len
    for i in range(array_len):
        array[i] = deserializeString(instream)
    return array

