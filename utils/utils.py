import datetime
import os

import drjit as dr
import matplotlib.pyplot as plt
import mitsuba as mi

from scripts.args import results_path


def save_image(image, filename, path=results_path, log=True, show=False):
    bitmap = mi.Bitmap(image)
    bitmap = bitmap.convert(
        pixel_format=mi.Bitmap.PixelFormat.RGB,
        component_format=mi.Struct.Type.UInt8,
    )
    images_path = os.path.join(path, "images")
    os.makedirs(images_path, exist_ok=True)
    full_path = os.path.join(images_path, filename)
    bitmap.write(mi.Thread.thread().file_resolver().resolve(full_path))

    if log:
        print(f"{filename} saved to {images_path}")
    if show:
        plt.imshow(image)
        plt.axis("off")
        plt.show()


def mse(image, image_ref):
    return dr.mean(dr.sqr(image - image_ref))
