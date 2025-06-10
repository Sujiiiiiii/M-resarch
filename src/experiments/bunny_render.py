import drjit as dr
import mitsuba as mi
from tqdm import tqdm

mi.set_variant("llvm_ad_rgb")

from mitsuba import ScalarTransform4f as T

from utils.utils import mse, save_image

cam_to_world = T().look_at(
    origin=[0, 0, 5],
    target=[0, 0, 0],
    up=[0, 1, 0],
)
cam_res = 512

bunny_to_world = T().translate([0, -0.1, 0])

cube_to_world = T().translate([0, 0, 0])

light_pos = [0, 0, 0]
light_r = 0.25

scene = mi.load_dict(
    {
        "type": "scene",
        "integrator": {"type": "path"},
        "sensor": {
            "type": "perspective",
            "fov": 45,
            "to_world": cam_to_world,
            "film": {
                "type": "hdrfilm",
                "width": cam_res,
                "height": cam_res,
                "rfilter": {"type": "box"},
            },
        },
        "cube": {
            "type": "cube",
            "to_world": cube_to_world,
            "flip_normals": True,
            "bsdf": {
                "type": "diffuse",
                "reflectance": {"type": "rgb", "value": [1.0, 1.0, 1.0]},
            },
        },
        "my_sphere_light": {
            "type": "sphere",
            "center": light_pos,
            "radius": light_r,
            "emitter": {
                "type": "area",
                "radiance": {"type": "rgb", "value": [5.0, 5.0, 5.0]},
            },
        },
    }
)

image = mi.render(scene)
save_image(image, "initial.png", show = True)
