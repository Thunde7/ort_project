from typing import Dict

from utils import formal_chunk

def read_zip_header(zipfile: str) -> Dict[str,str]:
    metadata = {}
    with open(zipfile,"rb") as input:
        metadata["sig"] = formal_chunk(input.read(4))
        metadata["ver"] = formal_chunk(input.read(2))
        metadata["gpflag"] = formal_chunk(input.read(2))
        metadata["cmpmethod"] = formal_chunk(input.read(2))
        metadata["lastmodtime"] = formal_chunk(input.read(2))
        metadata["lastmoddate"] = formal_chunk(input.read(2))
        metadata["crc"] = formal_chunk(input.read(4))
        metadata["cmprssd"] = formal_chunk(input.read(4))
        metadata["uncmprssd"] = formal_chunk(input.read(4))
        filename_len = int(formal_chunk(input.read(2)),16) 
        print(filename_len)
        extra_len = int(input.read(2).hex(),16)
        metadata["name"] =  input.read(filename_len)
    print(metadata)
