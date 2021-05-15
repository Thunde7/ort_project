def format_byte(byte):
    '''
    Formats a general byte 0xX or 0xXX to a uniform format 0xXX
    '''
    return "0x" + byte[2:].upper() if len(byte) == 4 else "0x0" + byte[2:].upper()


def strip_byte(byte):
    '''
    Strips the byte from his "\x" or "0x" prefix
    '''
    return format_byte(hex(byte))[2:]


def format_chunk(chunk): 
    '''
    Formats an entire chunk to be little endian and make 
    sure each byte is two characters long
    '''
    return [strip_byte(byte) for byte in chunk[::-1]]


def formal_chunk(chunk):
    '''
    Formats and adds a 0x prefix to the chunk
    '''
    return "0x" + "".join(format_chunk(chunk))
