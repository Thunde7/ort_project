def format_byte(byte): return r"\x" + \
    byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()


def strip_byte(byte): return format_byte(hex(byte))[2:]


def format_chunk(chunk): return [strip_byte(byte) for byte in chunk[::-1]]


def formal_chunk(chunk): return "0x" + "".join(format_chunk(chunk))
