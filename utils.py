from typing import Iterator


########
#CONSTS#
########
CHUNKSIZE = 2**3 #1KB


def file_to_bytes_gen(filename: str) -> Iterator[str]:
    '''
    Generates the bytes from 'filename'
    reads in chunk to not overflood the memory
    Args:
        filename (str): the file's full name (including path)
    Returns:
        Iterator of the hex strings of the bytes
    '''
    with open(filename,"rb") as input:
        while True:
            chunk = input.read(CHUNKSIZE)
            if chunk:
                yield from format_chunk(chunk)
            else:
                break

format_byte = lambda byte: r"\x" + byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()

strip_byte = lambda byte: format_byte(hex(byte))[2:]

format_chunk = lambda chunk : [strip_byte(byte) for byte in chunk[::-1]]

formal_chunk = lambda chunk : "0x" + "".join(format_chunk(chunk))

if __name__ == "__main__":
    for byte in file_to_bytes_gen("nexus.zip"):
        print(byte)