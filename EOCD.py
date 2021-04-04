from os.path import getsize

class EOCD():
    def __init__(self,src) -> None:
        self.find_eocd(src)
        with open(src,"rb") as input:
            input.seek(int(self.offset),2)
            self.sig =             formal_chunk(input.read(4))
            self.disk_number =     formal_chunk(input.read(2))
            self.cdfh_start =      formal_chunk(input.read(2))
            self.cdfh_count =  int(formal_chunk(input.read(2)),16)
            self.total_cdfh =  int(formal_chunk(input.read(2)),16)
            self.cdfh_size =   int(formal_chunk(input.read(4)),16)
            self.cdfh_offset = int(formal_chunk(input.read(4)),16)
            comment_len =      int(formal_chunk(input.read(2)),16)
            self.comment =         formal_chunk(input.read(comment_len))

    def find_eocd(self,src: str):
        '''
        Finds the end of the final central directory record in the file,
        Retruns the offset from the end of the file.
        Args:
            src (str) - the zipfile
        Returns:
            offset (int) - offset from the end of the zip file
        '''
        search_offset = -1 * min(getsize(src),1024)
        with open(src,"rb") as input:
            input.seek(search_offset,2)
            offset = formal_chunk(input.read(-1))[2:].index("06054B50")
        self.offset = - (offset // 2 + 4)

    def get_cdfh_offset(self):
        return self.cdfh_offset






format_byte = lambda byte: r"\x" + byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()

strip_byte = lambda byte: format_byte(hex(byte))[2:]

format_chunk = lambda chunk : [strip_byte(byte) for byte in chunk[::-1]]

formal_chunk = lambda chunk : "0x" + "".join(format_chunk(chunk))

