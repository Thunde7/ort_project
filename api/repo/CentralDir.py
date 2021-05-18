import math
import struct

from repo.utils import formal_chunk


class CentralDir():
    '''
    Holds the data in the CDFH in the zipfile(src)
    '''

    def __init__(self, src, offset) -> None:
        self.files = {}
        self.offset = offset
        with open(src, "rb") as input:
            input.seek(offset, 0)
            sig = formal_chunk(input.read(4))
            while sig == "0x02014B50":
                file = CDFH_File(input, sig)
                self.files[file.name] = file
                sig = formal_chunk(input.read(4))

        self.filecount = len(self.files)

    def get_files(self):
        return self.files.items()

    def check_for_overlaps(self) -> bool:
        offsets = set()
        for cdheader in self.files.values():
            offsets.add(cdheader.get_header_offset())
        if len(offsets) < self.filecount:  # overlapping files
            return True
        return False

    def check_for_same_file_ref(self) -> bool:
        soffsets = sorted(header.get_header_offset()
                          for header in self.files.values())
        diffs = {soffsets[i+1] - soffsets[i] for i in range(len(soffsets)-1)}
        if len(diffs) < math.log(self.filecount):
            return True
        # quoting local file headers(filename len should differ with at most O(logn))
        return False

    def __str__(self) -> str:
        return ("CDFH : {\n" + "\n".join(str(f) for _, f in self.get_files()) + "\t\t\n}")

    def to_dict(self):
        return {name : f.to_dict() for name, f in self.get_files()}


class CDFH_File():
    '''
    Holds the cdfh record for a specific file
    '''

    def __init__(self, input, sig) -> None:
        # Central directory file header signature
        self.sig = sig
        self.zipver, = struct.unpack("<H", input.read(
            2))                 # Version made by
        # Version needed to extract (minimum)
        self.zipexver, = struct.unpack("<H", input.read(2))
        # General purpose bit flag
        self.gpflag = formal_chunk(input.read(2))
        self.cmpmethod = formal_chunk(input.read(
            2)[::-1])           # Compression method
        # File last modification time
        self.lastmodtime, = struct.unpack("<H", input.read(2))
        # File last modification date
        self.lastmoddate, = struct.unpack("<H", input.read(2))
        # CRC-32 of uncompressed data
        self.crc = formal_chunk(input.read(4))
        self.compressed, = struct.unpack(
            "<I", input.read(4))             # Compressed size
        # Uncompressed size
        self.uncmpressed, = struct.unpack("<I", input.read(4))
        filename_len, = struct.unpack("<H", input.read(2))
        extra_len, = struct.unpack("<H", input.read(2))
        comment_len, = struct.unpack("<H", input.read(2))
        # Disk number where file starts
        self.first_disk_index, = struct.unpack("<H", input.read(2))
        # Internal file attributes
        self.intattr = formal_chunk(input.read(2))
        # External file attributes
        self.extattr = formal_chunk(input.read(4))
        # Relative offset of local file header
        self.file_offset, = struct.unpack("<I", input.read(4))
        self.name = (input.read(filename_len)).decode("utf-8")
        self.extra = formal_chunk(input.read(extra_len))
        self.comment = formal_chunk(input.read(comment_len))
        # Compression Ratio
        self.ratio = self.uncmpressed / self.compressed if self.compressed != 0 else float('inf')

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
            Compresssion Ratio : {self.ratio if self.ratio != float('inf') else "NaN"}
            {'}'}
        """
        )

    def to_dict(self):
        return ({
            "name" :self.name,
            "Signature" : self.sig,
            "Can be extracted by Zip Version" : self.zipexver,
            "General Purpose Flag" : self.gpflag,
            "Compression method" : self.cmpmethod,
            "Last modification time" : self.lastmodtime,
            "Last modification date" : self.lastmoddate,
            "CRC of uncompressed data" : self.crc,
            "Compressed size" : self.compressed,
            "Uncompressed size" : self.uncmpressed,
            "Disk Start Index" : self.first_disk_index,
            "Extra" : self.extra,
            "COMMENT" : {self.comment},
            "Compresssion Ratio" : eval(self.ratio if self.ratio != float('inf') else "NaN")
        })
