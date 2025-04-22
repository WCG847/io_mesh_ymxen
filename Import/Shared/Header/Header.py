from struct import unpack
from makefourcc import MAKEFOURCC
from Utilities.Constants import ADDEND

HEADER = MAKEFOURCC('Y', 'O', 'B', 'J',) # Flips to 'JBOY' due to endianness


def CheckJBOY(file):
	MAGIC = unpack('>I', file.read(4))[0] # Will be JBOY
	if HEADER != MAGIC:
		raise ValueError(f'Illegal Magic: {MAGIC}')

def GetSizeToRelocation(file):
	file.seek(12)
	_ = unpack('>I', file.read(4))[0]
	Size = (_ + ADDEND)


