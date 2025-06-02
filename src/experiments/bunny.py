import mitsuba as mi

from utils.utils import save_image

# print(f"variants: {mi.variants()}")
mi.set_variant("llvm_ad_rgb")

scene = mi.load_dict(
    {
        "type": "scene",
        "integrator": {"type": "path"},
        "sensor": {
            "type": "perspective",
            "fov": 45,
            "to_world": mi.ScalarTransform4f().look_at(
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
            "filename": "assets/models/bunny.ply",
            "face_normals": False,
            "to_world": mi.ScalarTransform4f().translate([0, -0.1, 0]),
            "bsdf": {
                "type": "plastic",
                "diffuse_reflectance": {
                    "type": "rgb",
                    "value": [1.0, 0.3, 0.3],
                },
                "specular_reflectance": {
                    "type": "rgb",
                    "value": [1, 1, 1]
                }
            },
        },
        "my_sphere_light": {
            "type": "sphere",
            "center": [0, 0.2, 0],
            "radius": 0.1,
            "emitter": {
                "type": "area",
                "radiance": {"type": "rgb", "value": [1.0, 1.0, 1.0]},
            },
        },
    }
)

image = mi.render(scene)
save_image(image, "bunny_render.png", show=True)
