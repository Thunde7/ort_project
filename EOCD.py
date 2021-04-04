from os.path import getsize

from utils import formal_chunk


class EOCD():
    def __init__(self, src) -> None:
        self.find_eocd(src)
        with open(src, "rb") as input:
            input.seek(int(self.offset), 2)
            # End of central directory signature
            self.sig = formal_chunk(input.read(4))
            self.disk_number = formal_chunk(
                input.read(2))              # Number of this disk
            # Disk where central directory starts
            self.cdfh_start = formal_chunk(input.read(2))
            # Number of central directory records on this disk
            self.cdfh_count = int(formal_chunk(input.read(2)), 16)
            # Total number of central directory records
            self.total_cdfh = int(formal_chunk(input.read(2)), 16)
            # Size of central directory (bytes)
            self.cdfh_size = int(formal_chunk(input.read(4)), 16)
            # Offset of start of central directory, relative to start of archive
            self.cdfh_offset = int(formal_chunk(input.read(4)), 16)
            comment_len = int(formal_chunk(input.read(2)),
                              16)          # Comment length (n)
            self.comment = formal_chunk(input.read(comment_len))    # Comment

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
        with open(src, "rb") as input:
            input.seek(search_offset, 2)
            offset = formal_chunk(input.read(-1))[2:].index("06054B50")
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
