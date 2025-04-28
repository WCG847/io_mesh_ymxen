from struct import unpack
from Shared.Utilities.Shaders import YSHADERS
from typing import BinaryIO
from Shared.Utilities.Constants import ADDEND


class CSubObject:
    def __init__(self):
        self.Entries = []

    def CollectSubObjects(self, file: BinaryIO, count: int, ptr: int) -> dict:
        file.seek(ptr + ADDEND)
        for i in range(count):
            VertexCount = unpack(">I", file.read(4))[0]
            FaceCount = unpack(">I", file.read(4))[0]
            BoneCount = unpack(">I", file.read(4))[0]
            AllBoneIndices = []
            for k in range(BoneCount):
                BoneIndices = unpack(">20I", file.read(80))
                ValidBoneIndices = [
                    index for index in BoneIndices if index != 0xFFFFFFFF
                ]
                AllBoneIndices.append(ValidBoneIndices)
                BoneWeightCount = unpack(">I", file.read(4))[
                    0
                ]  # typically rigid skinned
                VertexGroupIndices = unpack(">I", file.read(4))[0]
                BonePaletteSize = unpack(">I", file.read(4))[0]
                VertexPTR = unpack(">I", file.read(4))[0]
                WeightPTR = unpack(">I", file.read(4))[0]
                UVWQPTR = unpack(">I", file.read(4))[
                    0
                ]  # https://learn.microsoft.com/en-us/windows/win32/direct3d9/texture-support-in-d3dx
                RenderPriority = unpack(">I", file.read(4))[0]
                ShaderName = (
                    unpack("16s", file.read(16)).decode("latin1").rstrip("\x00")
                )
                if ShaderName not in YSHADERS:  # Just print a warning
                    print(f"WARNING: {ShaderName} may not be valid. Proceeding...")
                ShaderFamily = unpack(">I", file.read(4))[0]
                ShaderEnum = unpack(">I", file.read(4))[0]
                MaterialCount = unpack(">I", file.read(4))[0]
                MaterialPTR = unpack(">I", file.read(4))[0]
                FacePTR = unpack(">I", file.read(4))[0]
                file.seek(4, 1)  # We can decode the top Vertex Count.
                Centre = unpack(">3f", file.read(12))  # X, Y, Z center
                Radius = unpack(">f", file.read(4))  # Radius
                self.Entries.append(
                    {
                        "VertexCount": VertexCount,
                        "FaceCount": FaceCount,
                        "BoneCount": BoneCount,
                        "BoneIndices": AllBoneIndices,
                        "BoneWeightCount": BoneWeightCount,
                        "VGIndices": VertexGroupIndices,
                        "PaletteSize": BonePaletteSize,
                        "VertexPTR": VertexPTR,
                        "WeightPTR": WeightPTR,
                        "UVWQPTR": UVWQPTR,
                        "RenderPriority": RenderPriority,
                        "ShaderName": ShaderName,
                        "Family": ShaderFamily,
                        "Enum": ShaderEnum,
                        "MaterialCount": MaterialCount,
                        "MaterialPTR": MaterialPTR,
                        "FacePTR": FacePTR,
                        "bsphere": {"centre": Centre, "radius": Radius},
                    }
                )
        return self.Entries