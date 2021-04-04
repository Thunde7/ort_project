#########
#IMPORT$#
#########
from os.path import getsize
from typing import List


from EOCD import EOCD
from CentralDir import CentralDir
from File import File

EPSILON = 100
DEFLATE_LIM = 1032


class Zipfile():
    
    def __init__(self,src) -> None:
        self.name = src
        self.eocd = EOCD(src)
        self.cdfh_offset = self.eocd.get_cdfh_offset()
        self.cdfh = CentralDir(src,self.cdfh_offset)
        self.files = {}
        for name,header in self.cdfh.get_files():
            self.files[name] = (header, File(src,header.file_offset))


    def get_file_list(self) -> List[File]:
        return [self.files[name][1] for name in self.files]

    def uncmprssd_size(self) -> int:
        size = 0
        for name in self.files:
            size += max(map(lambda item : item.uncmpressed, self.files[name]))
        return size

    def is_zipbomb(self) -> bool:
        if self.cdfh.check_for_same_file_ref():
            return True
        if (self.uncmprssd_size() / getsize(self.name) - DEFLATE_LIM) < EPSILON:
            return True
        if any(file.get_ratio() - DEFLATE_LIM < EPSILON for file in self.get_file_list()):
            return True

        return False



    def __str__(self) -> str:
        files = "\n".join(str(file) for file in self.get_file_list())
        return(
            f"""
{self.name} : {'{'}
    {files},
    {str(self.cdfh)},
    {str(self.eocd)}
{'}'}            
            """
        )

def main():
    zf = Zipfile("nexus.zip")
    #print(zf.uncmprssd_size())
    #print(zf.is_zipbomb())
    print(zf)

if __name__ == "__main__":
    main()