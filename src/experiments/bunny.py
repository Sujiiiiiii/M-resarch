import mitsuba as mi
from tqdm import tqdm
import drjit as dr

mi.set_variant("llvm_ad_rgb")

from mitsuba import ScalarTransform4f as T

from utils.utils import save_image, mse

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
            "center": [0.1, 0.2, 0.2],
            "radius": 0.1,
            "emitter": {
                "type": "area",
                "radiance": {"type": "rgb", "value": [5.0, 5.0, 5.0]},
            },
        },
    }
)

scene_target = mi.load_dict(
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
        "sphere": {
            "type": "sphere",
            "radius": 0.1,
            "center": [0, 0, 0],
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
            "center": [0.1, 0.2, 0.2],
            "radius": 0.1,
            "emitter": {
                "type": "area",
                "radiance": {"type": "rgb", "value": [5.0, 5.0, 5.0]},
            },
        },
    }
)

image_initial = mi.render(scene)
save_image(image_initial, "initial.png")

image_target = mi.render(scene_target)
save_image(image_target, "target.png")

params = mi.traverse(scene)
# print(params)
key = 'bunny.vertex_positions'

opt = mi.ad.Adam(lr=1e-4)
opt[key] = params[key]
params.update(opt)

iter=500
save_each_iter=10

with tqdm(range(iter), desc="Optimization Progress") as pbar:
    for i in pbar:
        image = mi.render(scene, params)
        loss = mse(image, image_target)
        dr.backward(loss)
        opt.step()
        params.update(opt)
        pbar.set_postfix({"loss": loss})
        if i % save_each_iter == 0:
            print(f"Iteration {i}, Loss: {loss}")
            save_image(image, f"output_{i}.png", log=True)
save_image(image, "final_output.png", log=True)

print("Optimization complete.")

