from struct import unpack
from Shared.Utilities.Shaders import YSHADERS
from typing import BinaryIO

class CSubObject:
	def __init__(self):
		self.Entries = []

	def CollectSubObjects(file: BinaryIO, count:int) -> dict:
		for i in range(count):



