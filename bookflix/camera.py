from pyzbar.pyzbar import decode
from PIL import Image, ImageOps, ImageEnhance
import os

# import easyocr

# reader = easyocr.Reader( ["en"])  # this needs to run only once to load the model into memory


def scan_barcode(image_path):
    img = Image.open(image_path).convert("L")
    # preprocess the photo to make it easier to read the barcode: binarize, resize
    # max center crop
    img = ImageOps.exif_transpose(img)
    img = ImageOps.autocontrast(img)
    for size in range(2, 6):
        img_scaled = ImageOps.cover(
            img, (size * 128, size * 128), Image.Resampling.BILINEAR
        )
        for sharpness in [1, 0.5, 2]:
            img_blurred = ImageEnhance.Sharpness(img_scaled.copy()).enhance(sharpness)

            barcodes = decode(img_blurred)
            print(size * 128, sharpness, barcodes, img_blurred.size)
            if barcodes:
                img_blurred.save(image_path)
                # move to uploads/worked/ folder
                os.makedirs("uploads/worked", exist_ok=True)
                os.rename(
                    image_path,
                    f"uploads/worked/{os.path.basename(image_path)}",
                )
                return barcodes[0].data.decode("utf-8")

            img_blurred = img_blurred.point(lambda p: 255 if p > 128 else 0)
            barcodes = decode(img_blurred)
            print(size * 128, sharpness, barcodes, img_blurred.size)
            if barcodes:
                img_blurred.save(image_path)
                # move to uploads/worked/ folder
                os.makedirs("uploads/worked", exist_ok=True)
                os.rename(
                    image_path,
                    f"uploads/worked/{os.path.basename(image_path)}",
                )
                return barcodes[0].data.decode("utf-8")
    os.makedirs("uploads/failed", exist_ok=True)
    os.rename(image_path, f"uploads/failed/{os.path.basename(image_path)}")

    # result = reader.readtext( f"uploads/failed/{os.path.basename(image_path)}", detail=0)
    # print(result)
    return None
