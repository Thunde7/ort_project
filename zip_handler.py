from os.path import getsize
import sys 
from typing import Dict

from utils import formal_chunk, format_chunk

def find_file_data(zipfile,offset) -> Dict[str,str]:
    '''
    Parses the data in the file header
    Args:
        zipfile (str) - the zip file
        offset (int) - offset from the start of the zip file
    Returns:
        Dict (str, str) - the data in the file header
        {
            ...
            attr : related data 
            ...
        }
    '''
    metadata = {}
    with open(zipfile,"rb") as input:
        input.seek(offset,0)
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
        extra_len = int(input.read(2).hex(),16)
        name = input.read(filename_len)
        metadata["name"] =  name
        extra = formal_chunk(input.read(extra_len))
        metadata["extra"] = extra
    return metadata

def cdfh_parser(zipfile, offset) -> Dict[str, str]:
    '''
    Parses the data in the central directory file header
    Args:
        zipfile (str) - the zip file
        offset (int) - offset from the start of the zip file
    Returns:
        Dict (str, str) - the data in the cdfh
        {
            ...
            attr : related data 
            ...
        }
    '''
    data = {}
    with open(zipfile,"rb") as input:
        input.seek(offset,0)
        while True:
            sig = formal_chunk(input.read(4))
            if sig == "0x02014B50":
                metadata = {"sig" : sig}
                metadata["ver"] = formal_chunk(input.read(2))
                metadata["verex"] = formal_chunk(input.read(2))
                metadata["gpflag"] = formal_chunk(input.read(2))
                metadata["cmpmethod"] = formal_chunk(input.read(2))
                metadata["lastmodtime"] = formal_chunk(input.read(2))
                metadata["lastmoddate"] = formal_chunk(input.read(2))
                metadata["crc"] = formal_chunk(input.read(4))
                metadata["cmprssd"] = formal_chunk(input.read(4))
                metadata["uncmprssd"] = formal_chunk(input.read(4))
                filename_len = int(formal_chunk(input.read(2)),16) 
                extra_len = int(formal_chunk(input.read(2)),16)
                comment_len = int(formal_chunk(input.read(2)),16)
                metadata["first disk index"] = int(formal_chunk(input.read(2)),16)
                metadata["intattr"] = formal_chunk(input.read(2))
                metadata["extattr"] = formal_chunk(input.read(4))
                metadata["offset"] = int(formal_chunk(input.read(4)),16)
                name = input.read(filename_len)
                metadata["name"] =  name
                extra = formal_chunk(input.read(extra_len))
                metadata["extra"] = extra
                comment = formal_chunk(input.read(comment_len))
                metadata["comment"] = comment
                data[name] = metadata
            else:
                break
    return data

def eocd_parser(zipfile, offset) -> Dict[str, str]:
    '''
    Parses the data in the end of central directory
    Args:
        zipfile (str) - the zip file
        offset (int) - offset from the start of the zip file
    Returns:
        Dict (str, str) - the data in the eocd
        {
            ...
            attr : related data 
            ...
        }
    '''
    metadata = {}
    with open(zipfile,"rb") as input:
        input.seek(offset,2)
        metadata["sig"] = formal_chunk(input.read(4))
        metadata["disk number"] = int(formal_chunk(input.read(2)),16)
        metadata["cdfh start disk"] = int(formal_chunk(input.read(2)),16)
        metadata["cdfh count on disk"] = int(formal_chunk(input.read(2)),16)
        metadata["total cdfh count"] = int(formal_chunk(input.read(2)),16)
        metadata["cdfh size"] = int(formal_chunk(input.read(4)),16)
        metadata["cdfh offset"] = int(formal_chunk(input.read(4)),16)
        comment_len = int(formal_chunk(input.read(2)),16)
        comment = formal_chunk(input.read(comment_len))
        metadata["comment"] = comment
    return metadata



def find_eocd(zipfile: str) -> int:
    '''
    Finds the end of the final central directory record in the file,
    Retruns the offset from the end of the file.
    Args:
        zipfile (str) - the zipfile
    Returns:
        offset (int) - offset from the end of the zip file
    '''
    search_offset = -1 * min(getsize(zipfile),1024)
    with open(zipfile,"rb") as input:
        input.seek(search_offset,2)
        offset = formal_chunk(input.read(-1))[2:].index("06054B50")
    return offset // 2 + 4


def find_files(zipfile):
    eocd_offset = - find_eocd(zipfile) #offset from the end
    eocd_data = eocd_parser(zipfile,eocd_offset)
    cdfh_data = cdfh_parser(zipfile,eocd_data["cdfh offset"])
    files = {}
    for file, metadata in cdfh_data.items():
        files[file] = find_file_data(zipfile,metadata["offset"])
    return(files)

def print_format(files):

    print("{")
    for file, data in files.items():
        print(f'{file} : {"{"}')
        for entry, value in data.items():
            print(f"\t{entry} : {value},")
        print('\t},')
    print("}")
if __name__ == "__main__":
    files = find_files(sys.argv[1])
    print_format(files)    