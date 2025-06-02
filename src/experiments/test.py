import mitsuba as mi
from utils.utils import save_image

print(f"variants: {mi.variants()}")
mi.set_variant("llvm_ad_rgb")

# from mitsuba.core import Thread, ScalarTransform4f
# from mitsuba.render import Scene

# .ply ファイルを読み込む（例: assets/models/bunny.ply）
scene = mi.load_dict({
    "type": "scene",
    "integrator": {
        "type": "path"  # 基本的なパストレーサ
    },
    "sensor": {
        "type": "perspective",
        "fov": 45,
        "to_world": mi.ScalarTransform4f().look_at(
            origin=mi.ScalarPoint3f(0, 0, 3),  # カメラ位置
            target=mi.ScalarPoint3f(0, 0, 0),
            up=mi.ScalarPoint3f(0, 1, 0)
        ),
        "film": {
            "type": "hdrfilm",
            "width": 512,
            "height": 512,
            "rfilter": { "type": "box" }
        }
    },
    "bunny": {
        "type": "ply",
        "filename": "assets/models/bunny.ply",  # 🔁 パスは適宜修正
        "to_world": mi.ScalarTransform4f().scale(mi.ScalarPoint3f(10, 10, 10))  # 必要なら拡大
    },
    "light": {
        "type": "constant"  # または "envmap" など
    }
})

image = mi.render(scene)
save_image(image, "bunny_render.png")