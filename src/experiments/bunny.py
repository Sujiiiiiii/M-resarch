import mitsuba as mi

mi.set_variant("llvm_ad_rgb")

from mitsuba import ScalarTransform4f as T

from utils.utils import save_image

scene = mi.load_dict(
    {
        "type": "scene",
        "integrator": {"type": "path"},
        "sensor": {
            "type": "perspective",
            "fov": 45,
            "to_world": T().look_at(
                origin=[0, 0, 0.5],
                target=[0, 0, 0],
                up=[0, 1, 0],
            ),
            "film": {
                "type": "hdrfilm",
                "width": 512,
                "height": 512,
                "rfilter": {"type": "box"},
            },
        },
        "bunny": {
            "type": "ply",
            "filename": "assets/models/bunny/bunny_binary.ply",
            "flip_normals": True,
            "to_world": T().translate([0, -0.1, 0]),
            "bsdf": {
                "type": "plastic",
                "diffuse_reflectance": {
                    "type": "rgb",
                    "value": [1.0, 1.0, 1.0],
                },
                "specular_reflectance": {"type": "rgb", "value": [1, 1, 1]},
            },
        },
        "my_sphere_light": {
            "type": "sphere",
            "center": [0.1, 0.2, 0],
            "radius": 0.1,
            "emitter": {
                "type": "area",
                "radiance": {"type": "rgb", "value": [5.0, 5.0, 5.0]},
            },
        },
    }
)

image = mi.render(scene)
save_image(image, "bunny_render.png", show=True)
