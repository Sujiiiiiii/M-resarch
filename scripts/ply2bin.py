import os

import trimesh

ply_path = "/Users/hironakasuji/Documents/GitHub/M-resarch/assets/models/bunny.ply"


def convert_ply_to_binary(ply_path):
    mesh = trimesh.load(ply_path)
    out_path = os.path.splitext(ply_path)[0] + "_binary.ply"
    mesh.export(out_path, file_type="ply")
    print(f"Converted to binary PLY format at {out_path}")


if __name__ == "__main__":
    convert_ply_to_binary(ply_path)
