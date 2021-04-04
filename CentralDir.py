import math

class CentralDir():
    '''
    Holds the data in the CDFH in the zipfile(src)
    '''
    def __init__(self, src, offset) -> None:
        self.files = {}
        self.offset = offset
        with open(src,"rb") as input:
            input.seek(offset,0)
            while True:
                sig = formal_chunk(input.read(4))
                if sig == "0x02014B50":
                    file = CDFH_File(input,sig)
                    self.files[file.name] = file
                else:
                    break

        self.filecount = len(self.files)

    def get_files(self):
        return self.files.items()


    def check_for_same_file_ref(self) -> bool:
        offsets = set()
        for _, cdheader in self.files.items():
            offsets.add(cdheader.get_header_offset())
        if len(offsets) < self.filecount: # overlapping files
            return True
        diffs = set()
        soffsets = sorted(list(offsets))
        for i in range(len(soffsets)-1):
            diffs.add(soffsets[i+1] - soffsets[i])
        if len(diffs) <= (math.log(self.filecount) + 1) ** 2: return True
        #quoting local file headers(filename len should differ with at most O(logn), but I wanted some more headroom)
        return False


    def __str__(self) -> str:
        return ( "CDFH : {\n" + "\n".join(str(file) for name, file in self.get_files()) + "\t\t\n}" )



class CDFH_File():
    '''
    Holds the cdfh record for a specific file
    '''
    def __init__(self,input,sig) -> None:
        self.sig = sig                                                              # Central directory file header signature
        self.zipver =                   formal_chunk(input.read(2))                 # Version made by
        self.zipexver =                 formal_chunk(input.read(2))                 # Version needed to extract (minimum)
        self.gpflag =                   formal_chunk(input.read(2))                 # General purpose bit flag
        self.cmpmethod =                formal_chunk(input.read(2)[::-1])           # Compression method
        self.lastmodtime =              formal_chunk(input.read(2))                 # File last modification time
        self.lastmoddate =              formal_chunk(input.read(2))                 # File last modification date
        self.crc =                      formal_chunk(input.read(4))                 # CRC-32 of uncompressed data
        self.compressed =           int(formal_chunk(input.read(4)),16)             # Compressed size
        self.uncmpressed =          int(formal_chunk(input.read(4)),16)             # Uncompressed size
        filename_len =              int(formal_chunk(input.read(2)),16)             
        extra_len =                 int(formal_chunk(input.read(2)),16)             
        comment_len =               int(formal_chunk(input.read(2)),16)             
        self.first_disk_index =     int(formal_chunk(input.read(2)),16)             # Disk number where file starts
        self.intattr =                  formal_chunk(input.read(2))                 # Internal file attributes
        self.extattr =                  formal_chunk(input.read(4))                 # External file attributes
        self.file_offset =          int(formal_chunk(input.read(4)),16)             # Relative offset of local file header
        self.name =                                 (input.read(filename_len)).decode("utf-8")      
        self.extra =                    formal_chunk(input.read(extra_len))         
        self.comment =                  formal_chunk(input.read(comment_len))       
        self.ratio = self.uncmpressed / self.compressed                             # Compression Ratio

    def get_header_offset(self) -> int:
        return self.file_offset

    def __str__(self) -> str:
        return (
        f"""
        {self.name} : {'{'} 
            Signature : {self.sig},
            Made by Zip Version : {self.zipver},
            Can be extracted by Zip Version : {self.zipexver},
            General Purpose Flag : {self.gpflag},
            Compression method : {self.cmpmethod},
            Last modification time : {self.lastmodtime},
            Last modification date : {self.lastmoddate},
            CRC of uncompressed data : {self.crc},
            Compressed size : {self.compressed},
            Uncompressed size : {self.uncmpressed},
            Disk Start Index : {self.first_disk_index},
            Name : {self.name},
            Extra : {self.extra},
            COMMENT : {self.comment},
            Compresssion Ratio : {self.ratio}
            {'}'}
        """
        )





format_byte = lambda byte: r"\x" + byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()

strip_byte = lambda byte: format_byte(hex(byte))[2:]

format_chunk = lambda chunk : [strip_byte(byte) for byte in chunk[::-1]]

formal_chunk = lambda chunk : "0x" + "".join(format_chunk(chunk))


