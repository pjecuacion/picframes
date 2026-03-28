from PIL import Image, ImageDraw, ImageFont

BG = (15, 23, 42)
FG = (245, 158, 11)
SIZES = [16, 32, 48, 64, 128, 256]

def make_frame(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r = int(size * 0.18)
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=r, fill=BG)
    font_size = int(size * 0.68)
    font = None
    for path in [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/verdanab.ttf",
    ]:
        try:
            font = ImageFont.truetype(path, font_size)
            break
        except Exception:
            pass
    if font is None:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), "P", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1]
    draw.text((x, y), "P", font=font, fill=FG)
    return img

frames = [make_frame(s) for s in SIZES]
frames[-1].save("assets/app_icon.png")
frames[-1].save(
    "assets/app_icon.ico",
    format="ICO",
    sizes=[(s, s) for s in SIZES],
    append_images=frames[:-1],
)
print("Done")
