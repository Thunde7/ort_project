#########
#IMPORT$#
#########
from os.path import getsize


from EOCD import EOCD
from CentralDir import CentralDir
from File import File

EPSILON = 100


class Zipfile():
    
    def __init__(self,src) -> None:
        self.name = src
        self.eocd = EOCD(src)
        self.cdfh_offset = self.eocd.get_cdfh_offset()
        self.cdfh = CentralDir(src,self.cdfh_offset)
        self.files = {}
        for name,header in self.cdfh.get_files():
            self.files[name] = (header, File(src,header.file_offset))


    def uncmprssd_size(self) -> int:
        size = 0
        for name in self.files:
            size += max(map(lambda item : item.uncmpressed, self.files[name]))
        return size

    def is_zipbomb(self) -> bool:
        if self.cdfh.check_for_same_file_ref():
            return True
        if (self.uncmprssd_size() / getsize(self.name) - 1030) < EPSILON:
            return True
        if any(file.get_ratio() > 1000 for name, header, file in self.files.items()):
            return True

        return False




    def __str__(self) -> str:
        return( "{" + "\n".join(f"{v[1]}" for v in self.files.values()) + "}")


def main():
    zf = Zipfile("zbsm.zip")
    print(zf.uncmprssd_size())
    print(zf.is_zipbomb())

if __name__ == "__main__":
    main()