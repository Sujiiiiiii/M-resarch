import os

import trimesh

stl_path = "/Users/hironakasuji/Documents/GitHub/M-resarch/assets/models/lamp_A/LED Lamp Kit-001 lamp type A.stl"


def convert_stl_to_binary_ply(stl_path):
    mesh = trimesh.load(stl_path, force="mesh")
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError(f"Failed to load a mesh from {stl_path}")

    out_path = os.path.splitext(stl_path)[0] + "_binary.ply"
    mesh.export(out_path, file_type="ply", encoding="binary_little_endian")
    print(f"Converted to binary PLY format at {out_path}")


if __name__ == "__main__":
    convert_stl_to_binary_ply(stl_path)
