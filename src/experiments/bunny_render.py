import drjit as dr
import mitsuba as mi
from tqdm import tqdm

mi.set_variant("llvm_ad_rgb")

from mitsuba import ScalarTransform4f as T

from utils.utils import mse, save_image

# Cam parameters
origin = [4, 4, 4]
target = [0, 0, 0]
up = [0, 1, 0]
cam_to_world = T().look_at(
    origin=origin,
    target=target,
    up=up,
)
cam_fov = 45
cam_res = 512

# Cube parameters
cube_in_scale = 0.9
cube_in_to_world = T().translate([0, 0, 0]).scale(cube_in_scale)
cube_ex_to_world = T().translate([0, 0, 0])
cube_alpha = 0.2

# Light parameters
light_pos = [0, 0, 0]
light_r = 0.1
light_value = 10.0

# Glass parameters
glass_ior = 1.5
glass_albedo = 0.0
glass_sigma_t = 5.0

# Air parameters
air_ior = 1.0
air_albedo = 0.0
air_sigma_t = 0.0

scene = mi.load_dict(
    {
        "type": "scene",
        "integrator": {
            "type": "volpath",
            "max_depth": 8,
        },
        "sensor": {
            "type": "perspective",
            "fov": cam_fov,
            "to_world": cam_to_world,
            "film": {
                "type": "hdrfilm",
                "width": cam_res,
                "height": cam_res,
                "rfilter": {"type": "box"},
            },
        },
        "cube_in": {
            "type": "cube",
            "to_world": cube_in_to_world,
            "bsdf": {
                "type": "roughdielectric",
                "int_ior": air_ior,
                "ext_ior": glass_ior,
                "alpha": cube_alpha,
            },
        },
        "cube_ex": {
            "type": "cube",
            "to_world": cube_ex_to_world,
            "bsdf": {
                "type": "roughdielectric",
                "int_ior": glass_ior,
                "ext_ior": air_ior,
                "alpha": cube_alpha,
            },
            "interior": {
                "type": "homogeneous",
                "albedo": glass_albedo,
                "sigma_t": glass_sigma_t,
            }
        },
        "sphere_light": {
            "type": "sphere",
            "center": light_pos,
            "radius": light_r,
            "emitter": {
                "type": "area",
                "radiance": {"type": "rgb", "value": [light_value, light_value, light_value]},
            },
        },
    }
)

image = mi.render(scene, spp=64)

max_val = dr.max(image)
print("Max pixel value:", max_val)

save_image(image, "image.png", show = True)
