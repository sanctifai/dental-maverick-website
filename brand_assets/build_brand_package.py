from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


ROOT = Path(r"c:\devtest\dental")
PACKAGE = ROOT / "brand-package"
ASSETS = PACKAGE / "assets"
SOURCE_ASSETS = ROOT / "assets"

INK = "#1A1D2E"
GRAPHITE = "#4B5568"
STONE = "#B9B4AA"
CLOUD = "#E7E4DE"
PORCELAIN = "#F8F6F1"
WHITE = "#FFFFFF"


def hex_rgba(value: str, alpha: int = 255):
    rgb = ImageColor.getrgb(value)
    return (rgb[0], rgb[1], rgb[2], alpha)


def load_font(size: int):
    return ImageFont.truetype(str(SOURCE_ASSETS / "PlusJakartaSans-Bold.ttf"), size)


def load_mark():
    return Image.open(SOURCE_ASSETS / "logo.png").convert("RGBA")


def recolor_mark(mark: Image.Image, color: str):
    target = ImageColor.getrgb(color)
    out = Image.new("RGBA", mark.size, (0, 0, 0, 0))
    src = mark.load()
    dst = out.load()
    for y in range(mark.height):
        for x in range(mark.width):
            _, _, _, a = src[x, y]
            if a:
                dst[x, y] = (target[0], target[1], target[2], a)
    return out


def fit_mark(mark: Image.Image, height: int):
    scale = height / mark.height
    width = int(mark.width * scale)
    return mark.resize((width, height), Image.LANCZOS)


def draw_text_measure(text: str, font):
    probe = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(probe)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return left, top, right, bottom


def draw_centered_text(draw, image_width, y, text, font, fill):
    left, top, right, bottom = draw_text_measure(text, font)
    width = right - left
    draw.text(((image_width - width) / 2 - left, y - top), text, font=font, fill=fill)
    return bottom - top


def save_image(image: Image.Image, name: str):
    image.save(ASSETS / name)


def build_primary_horizontal():
    text = "DENTAL MAVERICK AI"
    font = load_font(72)
    mark = fit_mark(recolor_mark(load_mark(), INK), 120)
    left, top, right, bottom = draw_text_measure(text, font)
    text_w = right - left
    text_h = bottom - top
    padding_x = 48
    padding_y = 40
    gap = 30
    width = padding_x * 2 + mark.width + gap + text_w
    height = max(mark.height, text_h) + padding_y * 2

    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    image.alpha_composite(mark, (padding_x, (height - mark.height) // 2))
    draw.text((padding_x + mark.width + gap - left, (height - text_h) // 2 - top), text, font=font, fill=INK)
    save_image(image, "logo-primary-horizontal-dark.png")

    light_mark = fit_mark(recolor_mark(load_mark(), WHITE), 120)
    light = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    light_draw = ImageDraw.Draw(light)
    light.alpha_composite(light_mark, (padding_x, (height - light_mark.height) // 2))
    light_draw.text((padding_x + light_mark.width + gap - left, (height - text_h) // 2 - top), text, font=font, fill=WHITE)
    save_image(light, "logo-primary-horizontal-light.png")


def build_stacked():
    text = "DENTAL MAVERICK AI"
    font = load_font(52)
    mark = fit_mark(recolor_mark(load_mark(), INK), 140)
    left, top, right, bottom = draw_text_measure(text, font)
    text_w = right - left
    text_h = bottom - top
    width = max(mark.width, text_w) + 80
    height = mark.height + text_h + 120

    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    image.alpha_composite(mark, ((width - mark.width) // 2, 28))
    draw_centered_text(draw, width, mark.height + 54, text, font, INK)
    save_image(image, "logo-secondary-stacked-dark.png")

    light_mark = fit_mark(recolor_mark(load_mark(), WHITE), 140)
    light = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    light_draw = ImageDraw.Draw(light)
    light.alpha_composite(light_mark, ((width - light_mark.width) // 2, 28))
    draw_centered_text(light_draw, width, light_mark.height + 54, text, font, WHITE)
    save_image(light, "logo-secondary-stacked-light.png")


def build_mark_assets():
    dark_mark = fit_mark(recolor_mark(load_mark(), INK), 512)
    save_image(dark_mark, "logo-mark-dark.png")

    light_mark = fit_mark(recolor_mark(load_mark(), WHITE), 512)
    save_image(light_mark, "logo-mark-light.png")


def build_icons():
    base_mark_dark = fit_mark(recolor_mark(load_mark(), INK), 420)
    base_mark_light = fit_mark(recolor_mark(load_mark(), WHITE), 420)

    light_icon = Image.new("RGBA", (512, 512), hex_rgba(PORCELAIN))
    light_icon.alpha_composite(base_mark_dark, ((512 - base_mark_dark.width) // 2, (512 - base_mark_dark.height) // 2))
    save_image(light_icon, "icon-square-light.png")

    dark_icon = Image.new("RGBA", (512, 512), hex_rgba(INK))
    dark_icon.alpha_composite(base_mark_light, ((512 - base_mark_light.width) // 2, (512 - base_mark_light.height) // 2))
    save_image(dark_icon, "icon-square-dark.png")

    save_image(light_icon, "favicon-512.png")
    light_icon.resize((192, 192), Image.LANCZOS).save(ASSETS / "favicon-192.png")
    light_icon.resize((32, 32), Image.LANCZOS).save(ASSETS / "favicon-32.png")


def build_social_assets():
    title_font = load_font(86)
    subtitle_font = load_font(30)
    mark = fit_mark(recolor_mark(load_mark(), INK), 180)

    banner = Image.new("RGBA", (1600, 600), hex_rgba(PORCELAIN))
    draw = ImageDraw.Draw(banner)
    draw.rounded_rectangle((70, 70, 1530, 530), radius=40, fill=hex_rgba(WHITE))
    draw.line((70, 480, 1530, 480), fill=hex_rgba(CLOUD), width=2)
    banner.alpha_composite(mark, (130, 210))
    draw.text((360, 230), "DENTAL MAVERICK AI", font=title_font, fill=INK)
    draw.text((366, 338), "Modern-tech branding for bold dental intelligence.", font=subtitle_font, fill=GRAPHITE)
    draw.text((366, 392), "Precision / clarity / confident care", font=subtitle_font, fill=STONE)
    save_image(banner, "social-banner.png")

    profile = Image.new("RGBA", (800, 800), hex_rgba(PORCELAIN))
    pdraw = ImageDraw.Draw(profile)
    pdraw.rounded_rectangle((60, 60, 740, 740), radius=80, fill=hex_rgba(WHITE))
    large_mark = fit_mark(recolor_mark(load_mark(), INK), 360)
    profile.alpha_composite(large_mark, ((800 - large_mark.width) // 2, 170))
    pdraw.text((188, 610), "DENTAL MAVERICK AI", font=load_font(32), fill=INK)
    save_image(profile, "social-profile.png")


def build_marketing_assets():
    card_w, card_h = 1050, 600
    front = Image.new("RGBA", (card_w, card_h), hex_rgba(WHITE))
    draw = ImageDraw.Draw(front)
    draw.rounded_rectangle((0, 0, card_w - 1, card_h - 1), radius=32, outline=hex_rgba(CLOUD), width=2)
    mark = fit_mark(recolor_mark(load_mark(), INK), 120)
    front.alpha_composite(mark, (80, 90))
    draw.text((240, 112), "DENTAL MAVERICK AI", font=load_font(46), fill=INK)
    draw.text((84, 300), "Name Surname", font=load_font(32), fill=INK)
    draw.text((84, 356), "Chief Executive Officer", font=load_font(24), fill=GRAPHITE)
    draw.text((84, 450), "hello@dentalmaverick.ai", font=load_font(22), fill=GRAPHITE)
    draw.text((84, 492), "www.dentalmaverick.ai", font=load_font(22), fill=GRAPHITE)
    save_image(front, "business-card-front.png")

    back = Image.new("RGBA", (card_w, card_h), hex_rgba(INK))
    back_mark = fit_mark(recolor_mark(load_mark(), WHITE), 170)
    back.alpha_composite(back_mark, ((card_w - back_mark.width) // 2, 160))
    bdraw = ImageDraw.Draw(back)
    bdraw.text((290, 390), "DENTAL MAVERICK AI", font=load_font(34), fill=WHITE)
    save_image(back, "business-card-back.png")

    deck = Image.new("RGBA", (1600, 900), hex_rgba(PORCELAIN))
    ddraw = ImageDraw.Draw(deck)
    ddraw.rectangle((0, 0, 260, 900), fill=hex_rgba(INK))
    deck_mark = fit_mark(recolor_mark(load_mark(), WHITE), 120)
    deck.alpha_composite(deck_mark, (70, 84))
    ddraw.text((340, 250), "DENTAL MAVERICK AI", font=load_font(70), fill=INK)
    ddraw.text((344, 360), "Brand Presentation", font=load_font(34), fill=GRAPHITE)
    ddraw.text((344, 430), "Modern-tech identity system", font=load_font(28), fill=STONE)
    save_image(deck, "presentation-cover.png")

    page = Image.new("RGBA", (1240, 1754), hex_rgba(WHITE))
    pdraw = ImageDraw.Draw(page)
    pdraw.rectangle((0, 0, 1240, 180), fill=hex_rgba(PORCELAIN))
    letter_mark = fit_mark(recolor_mark(load_mark(), INK), 72)
    page.alpha_composite(letter_mark, (90, 56))
    pdraw.text((220, 74), "DENTAL MAVERICK AI", font=load_font(34), fill=INK)
    pdraw.line((90, 210, 1150, 210), fill=hex_rgba(CLOUD), width=3)
    pdraw.text((90, 280), "Letterhead Sample", font=load_font(28), fill=GRAPHITE)
    save_image(page, "letterhead.png")


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    build_primary_horizontal()
    build_stacked()
    build_mark_assets()
    build_icons()
    build_social_assets()
    build_marketing_assets()
    print("Brand package assets generated.")


if __name__ == "__main__":
    main()
