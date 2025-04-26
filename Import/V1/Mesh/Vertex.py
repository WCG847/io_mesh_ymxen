from Shared.Utilities.Constants import ADDEND
from SubObject.Table import CSubObject
from ctypes import BigEndianStructure as Struct, sizeof, c_float, c_ubyte, cast, POINTER
from typing import List, Dict, Any




class CSkinModel(Struct):
	_fields_ = [
		("position", c_float * 3),
		("normal", c_float * 3),
		("colour", c_ubyte * 4)
	]

class CSkinModelParser:
	def __init__(self, subobject_entries: List[Dict[str, Any]]):
		self.Entries = subobject_entries
		self.Vertices = []

	def UnpackVertex(self, file):
		for JBOY in self.Entries:
			VertexPTR = JBOY['VertexPTR']
			VertexCount = JBOY['VertexCount']
			file.seek(VertexPTR + ADDEND)

			total_size = sizeof(CSkinModel) * VertexCount

			# Read once
			raw_data = file.read(total_size)

			array_type = CSkinModel * VertexCount 
			vertices_array = cast(raw_data, POINTER(array_type)).contents

			self.Vertices.append(vertices_array)

		return self.Vertices