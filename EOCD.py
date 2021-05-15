from os.path import getsize
import struct

from utils import formal_chunk


class EOCD():
    def __init__(self, src) -> None:
        self.find_eocd(src)
        with open(src, "rb") as infile:
            infile.seek(int(self.offset), 2)
            # End of central directory signature
            self.sig = formal_chunk(infile.read(4))
            self.disk_number, = struct.unpack("<H",
                                              infile.read(2))
            # Number of this disk
            # Disk where central directory starts
            self.cdfh_start, = struct.unpack("<H", infile.read(2))
            # Number of central directory records on this disk
            self.cdfh_count, = struct.unpack("<H", infile.read(2))
            # Total number of central directory records
            self.total_cdfh, = struct.unpack("<H", infile.read(2))
            # Size of central directory (bytes)
            self.cdfh_size, = struct.unpack("<I", infile.read(4))
            # Offset of start of central directory, relative to start of archive
            self.cdfh_offset, = struct.unpack("<I", infile.read(4))
            comment_len, = struct.unpack(
                "<H", infile.read(2))          # Comment length (n)
            self.comment = formal_chunk(infile.read(comment_len))    # Comment

    def find_eocd(self, src: str):
        '''
        Finds the end of the final central directory record in the file,
        Retruns the offset from the end of the file.
        Args:
            src (str) - the zipfile
        Returns:
            offset (int) - offset from the end of the zip file
        '''
        search_offset = -1 * min(getsize(src), 1024)
        with open(src, "rb") as infile:
            infile.seek(search_offset, 2)
            offset = formal_chunk(infile.read(-1))[2:].index("06054B50")
        self.offset = - (offset // 2 + 4)

    def get_cdfh_offset(self):
        return self.cdfh_offset

    def __str__(self) -> str:
        return (
            f"""EOCD : {'{'} 
            signature : {self.sig},
            Disk Start Index : {self.disk_number},
            CDFH Disk Start Index : {self.cdfh_start},
            CDFH Count On Disk : {self.cdfh_count},
            CDFH Total Count : {self.total_cdfh},
            CDFH Size : {self.cdfh_size},
            CDFH Offset : {self.cdfh_offset},
            COMMENT : {self.comment}
            {'}'}
        """
        )
