from utils import formal_chunk

class File():
    '''
    Holds the file's metadata that can be read from the file header inside the 
    zip(src) file which starts at offset
    '''
    def __init__(self, src, offset):
        with open(src,"rb") as input:
            input.seek(int(offset),0)
            self.sig =              formal_chunk(input.read(4))                               # Local file header signature
            self.zipver =           formal_chunk(input.read(2))                               # Version needed to extract (minimum)
            self.gpflag =           formal_chunk(input.read(2))                               # General purpose bit flag
            self.cmpmethod =        formal_chunk(input.read(2))                               # Compression method
            self.lastmodtime =      formal_chunk(input.read(2))                               # File last modification time
            self.lastmoddate =      formal_chunk(input.read(2))                               # File last modification date
            self.crc =              formal_chunk(input.read(4))                               # CRC-32 of uncompressed data
            self.compressed =   int(formal_chunk(input.read(4)),16)                           # Compressed size 
            self.uncmpressed =  int(formal_chunk(input.read(4)),16)                           # Uncompressed size 
            filename_len =      int(formal_chunk(input.read(2)),16)
            extra_len =                      int(input.read(2).hex(),16)
            self.name =                          input.read(filename_len).decode("utf-8")
            self.extra =            formal_chunk(input.read(extra_len))                        
            self.ratio = self.uncmpressed / self.compressed                                    # Compression Ratio


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
            Compresssion Ratio : {self.ratio}
            {'}'}
        """
        )



