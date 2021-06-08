#########
#IMPORT$#
#########
import enum
from os.path import getsize
from os import sep
from typing import List
from functools import lru_cache
from hurry.filesize import size, si

from repo.EOCD import EOCD
from repo.CentralDir import CentralDir
from repo.File import File

EPSILON = 100
DEFLATE_LIM = 1032


class Bomb(enum.Enum):
    CLEAR = ("The Archive is safe")
    OVERLAPING_FILES = ("The Archive has overlapping files,\nIt's dangerous")
    SAME_FILE_REF = (
        "The Archive maps all files to the same file,\nIt's dangerous")
    BIG_TOTAL_RATIO = (
        "The Archive has an unusually big compression ratio,\nmight be dangerous")
    FILE_WITH_BIG_RATIO = (
        "The Archive has at least one file with an unusually big compression ratio,\nmight be dangerous")

    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class Zipfile():

    def __init__(self, src, print_type=None):
        self.name = src.split(sep)[-1]
        self.eocd = EOCD(src)
        self.cdfh_offset = self.eocd.get_cdfh_offset()
        self.cdfh = CentralDir(src, self.cdfh_offset)
        self.files = {}
        for name, header in self.cdfh.get_files():
            self.files[name] = (header, File(src, header.file_offset))
        self.print_type = print_type
        self.fullpath = src

    def get_file_list(self) -> List[File]:
        return [self.files[name][1] for name in self.files]

    @lru_cache
    def uncmprssd_size(self) -> int:
        size = 0
        for name in self.files:
            size += max(map(lambda item: item.uncmpressed, self.files[name]))
        return size

    @lru_cache
    def compressed_size(self) -> int:
        return getsize(self.fullpath)

    def is_zipbomb(self) -> Bomb:
        if self.cdfh.check_for_overlaps():
            return Bomb.OVERLAPING_FILES
        if self.cdfh.check_for_same_file_ref():
            return Bomb.SAME_FILE_REF
        if abs((self.uncmprssd_size() / self.compressed_size()) - DEFLATE_LIM) < EPSILON:
            return Bomb.BIG_TOTAL_RATIO
        if any(abs(file.get_ratio() - DEFLATE_LIM) < EPSILON for file in self.get_file_list()):
            return Bomb.FILE_WITH_BIG_RATIO

        return Bomb.CLEAR

    def __str__(self) -> str:
        if self.print_type == "short":
            files = "\n".join(name for name in self.files)
            ratio = self.uncmprssd_size() / self.compressed_size()
            eocd_offset = self.eocd.offset

            return(
                f"""
            {self.name} :  {'{'}
            files : {files}
            cmpression ratio : {ratio}
            uncmprssd : {self.uncmprssd_size()}
            cmprssd : {self.compressed_size()}
            EOCD offset(from EOF) : {eocd_offset}
            CDFH offset : {self.cdfh_offset}
            {'}'}
            """
            )
        elif self.print_type == "long":
            files = "\n".join(str(file) for file in self.get_file_list())
            return(
                f"""
{self.name} : {'{'}
    files : {'{'}
        {files}
    {'}'},
    cdfh : {'{'} {str(self.cdfh)},
    {str(self.eocd)}
{'}'}            
    """
            )
        else:
            return str(self.is_zipbomb())

    def to_dict(self):
        return {"name": self.name,
                "files": [file.to_dict() for file in self.get_file_list()],
                "CDFH": self.cdfh.to_dict(),
                "EOCD": self.eocd.to_dict(), 
                "compressedSize": size(self.compressed_size(), system=si) + "b",
                "uncompressedSize": size(self.uncmprssd_size(), system=si) + 'b',
                "cmpraw" : self.compressed_size(),
                "uncpmraw": self.uncmprssd_size(), 
                "ratio":  "{:.2f}".format(self.uncmprssd_size() / self.compressed_size()),
                "isBomb": str(self.is_zipbomb())}


def main():
    #zf = Zipfile("nexus.zip")
    # print(zf.uncmprssd_size())
    # print(zf.is_zipbomb())
    # print(zf)
    pass


if __name__ == "__main__":
    main()
