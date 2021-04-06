#########
#IMPORT$#
#########
import enum
from os.path import getsize
from typing import List
from functools import lru_cache

from EOCD import EOCD
from CentralDir import CentralDir
from File import File

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

    def __init__(self, src) -> None:
        self.name = src
        self.eocd = EOCD(src)
        self.cdfh_offset = self.eocd.get_cdfh_offset()
        self.cdfh = CentralDir(src, self.cdfh_offset)
        self.files = {}
        for name, header in self.cdfh.get_files():
            self.files[name] = (header, File(src, header.file_offset))

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
        size = 0
        for name in self.files:
            size += max(map(lambda item: item.compressed, self.files[name]))
        return size

    def is_zipbomb(self) -> Bomb:
        if self.cdfh.check_for_overlaps():
            return Bomb.OVERLAPING_FILES
        if self.cdfh.check_for_same_file_ref():
            return Bomb.SAME_FILE_REF
        if abs(self.uncmprssd_size() / self.compressed_size() - DEFLATE_LIM) < EPSILON:
            return Bomb.BIG_TOTAL_RATIO
        if any(abs(file.get_ratio() - DEFLATE_LIM) < EPSILON for file in self.get_file_list()):
            return Bomb.FILE_WITH_BIG_RATIO

        return Bomb.CLEAR

    def short_str(self) -> str:
        files = "\n".join(name for name in self.files)
        ratio = self.uncmprssd_size() / self.compressed_size()
        eocd_offset = self.eocd.offset

        return(
            f"""
{self.name} :  {'{'}
    {files}
    cmpression ratio : {ratio}
    uncmprssd : {self.uncmprssd_size()}
    cmprssd : {self.compressed_size()}
    EOCD offset(from EOF) : {eocd_offset}
    CDFH offset : {self.cdfh_offset}
{'}'}
    """
        )

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
    # print(zf.uncmprssd_size())
    print(zf.is_zipbomb())
    # print(zf)


if __name__ == "__main__":
    main()
