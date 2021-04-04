class File():
    '''
    Holds the file's metadata that can be read from the file header inside the 
    zip(src) file which starts at offset
    '''
    def __init__(self, src, offset):
        with open(src,"rb") as input:
            input.seek(int(offset),0)
            self.sig =              formal_chunk(input.read(4))
            self.zipver =           formal_chunk(input.read(2))
            self.gpflag =           formal_chunk(input.read(2))
            self.cmpmethod =        formal_chunk(input.read(2))
            self.lastmodtime =      formal_chunk(input.read(2))
            self.lastmoddate =      formal_chunk(input.read(2))
            self.crc =              formal_chunk(input.read(4))
            self.compressed =   int(formal_chunk(input.read(4)),16)
            self.uncmpressed =  int(formal_chunk(input.read(4)),16)
            filename_len =      int(formal_chunk(input.read(2)),16) 
            extra_len =                      int(input.read(2).hex(),16)
            self.name =                          input.read(filename_len)
            self.extra =            formal_chunk(input.read(extra_len))
            self.ratio = self.uncmpressed / self.compressed


    def __str__(self) -> str:
        return(f"""
        {self.name} : {'{'}
            method : {self.cmpmethod}
            cmprsd : {self.compressed}
            uncmpd : {self.uncmpressed}
        {'}'}
        """)


format_byte = lambda byte: r"\x" + byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()

strip_byte = lambda byte: format_byte(hex(byte))[2:]

format_chunk = lambda chunk : [strip_byte(byte) for byte in chunk[::-1]]

formal_chunk = lambda chunk : "0x" + "".join(format_chunk(chunk))

