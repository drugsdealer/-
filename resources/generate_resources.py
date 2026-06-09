"""
Генерация ресурсов приложения: логотип, иконка, заглушка изображения товара.
Запускать один раз перед первым запуском приложения.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.dirname(__file__)


def create_logo():
    img = Image.new("RGBA", (240, 80), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 239, 79], fill=(44, 62, 80), outline=(52, 152, 219), width=3)
    draw.rectangle([8, 8, 71, 71], fill=(52, 152, 219), outline=(41, 128, 185), width=2)
    draw.polygon([(20, 50), (40, 20), (60, 50)], fill=(255, 255, 255))
    draw.ellipse([30, 38, 50, 58], fill=(243, 156, 18))

    try:
        font_big  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_big  = ImageFont.load_default()
        font_small = font_big

    draw.text((82, 18), "МагазинПро", font=font_big, fill=(255, 255, 255))
    draw.text((82, 50), "Система управления", font=font_small, fill=(174, 214, 241))

    path = os.path.join(OUT_DIR, "logo.png")
    img.save(path, "PNG")
    print(f"Логотип сохранён: {path}")


def create_icon():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, 62, 62], fill=(44, 62, 80), outline=(52, 152, 219), width=3)
    draw.polygon([(15, 45), (32, 12), (49, 45)], fill=(255, 255, 255))
    draw.ellipse([26, 34, 38, 46], fill=(243, 156, 18))
    path = os.path.join(OUT_DIR, "icon.png")
    img.save(path, "PNG")
    print(f"Иконка сохранена: {path}")


def create_placeholder():
    img = Image.new("RGB", (200, 200), (189, 195, 199))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 189, 189], outline=(127, 140, 141), width=3)
    draw.rectangle([40, 60, 160, 140], fill=(149, 165, 166), outline=(127, 140, 141), width=2)
    draw.ellipse([70, 25, 130, 65], fill=(149, 165, 166), outline=(127, 140, 141), width=2)
    draw.line([40, 140, 100, 90], fill=(127, 140, 141), width=3)
    draw.line([100, 90, 160, 130], fill=(127, 140, 141), width=3)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except Exception:
        font = ImageFont.load_default()

    draw.text((50, 155), "Нет фото", font=font, fill=(127, 140, 141))

    path = os.path.join(OUT_DIR, "picture.png")
    img.save(path, "PNG")
    print(f"Заглушка сохранена: {path}")


if __name__ == "__main__":
    create_logo()
    create_icon()
    create_placeholder()
    print("Все ресурсы созданы.")
