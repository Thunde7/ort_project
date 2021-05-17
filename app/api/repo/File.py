import struct
from repo.utils import formal_chunk


class File():
    '''
    Holds the file's metadata that can be read from the file header inside the 
    zip(src) file which starts at offset
    '''

    def __init__(self, src, offset):
        with open(src, "rb") as input:
            input.seek(int(offset), 0)
            # Local file header signature
            self.sig = formal_chunk(input.read(4))
            # Version needed to extract (minimum)
            self.zipver, = struct.unpack("<H", input.read(2))
            # General purpose bit flag
            self.gpflag = formal_chunk(input.read(2))
            # Compression method
            self.cmpmethod = formal_chunk(input.read(2))
            # File last modification time
            self.lastmodtime, = struct.unpack("<H", input.read(2))
            # File last modification date
            self.lastmoddate, = struct.unpack("<H", input.read(2))
            # CRC-32 of uncompressed data
            self.crc = formal_chunk(input.read(4))
            # Compressed size
            self.compressed, = struct.unpack("<I", input.read(4))
            # Uncompressed size
            self.uncmpressed, = struct.unpack("<I", input.read(4))
            filename_len, = struct.unpack("<H", input.read(2))
            extra_len, = struct.unpack("<H", input.read(2))
            self.name = input.read(filename_len).decode("utf-8")
            self.extra = formal_chunk(input.read(extra_len))
            # Compression Ratio
            self.ratio = self.uncmpressed / self.compressed if self.compressed != 0 else float('inf') 

    def get_ratio(self) -> int:
        return self.ratio

    def __str__(self) -> str:
        return (
            f"""
        {self.name} : {'{'} 
            Signature : {self.sig},
            Can be extracted by Zip Version : {self.zipver},
            General Purpose Flag : {self.gpflag},
            Compression method : {self.cmpmethod},
            Last modification time : {self.lastmodtime},
            Last modification date : {self.lastmoddate},
            CRC of uncompressed data : {self.crc},
            Compressed size : {self.compressed},
            Uncompressed size : {self.uncmpressed},
            Name : {self.name},
            Extra : {self.extra},
            Compresssion Ratio : {self.ratio if self.ratio != float('inf') else "NaN"}
            {'}'}
        """
        )

    def to_dict(self):
        return ({
            "name" :self.name,
            "Signature" : self.sig,
            "Can be extracted by Zip Version" : self.zipver,
            "General Purpose Flag" : self.gpflag,
            "Compression method" : self.cmpmethod,
            "Last modification time" : self.lastmodtime,
            "Last modification date" : self.lastmoddate,
            "CRC of uncompressed data" : self.crc,
            "Compressed size" : self.compressed,
            "Uncompressed size" : self.uncmpressed,
            "Extra" : self.extra,
            "Compresssion Ratio" : eval(self.ratio if self.ratio != float('inf') else "NaN")
        })
