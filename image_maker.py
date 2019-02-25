import requests
from PIL import ImageFont, Image, ImageDraw
from io import BytesIO


def create_blank_image():
    return Image.new("RGBA", (525, 825), (255, 255, 255))


def make_report_image(stat, with_frame=False):
    image_obj = create_blank_image()
    font_low = ImageFont.truetype("/fonts/Roboto-Medium.ttf", 20, encoding="unic")
    font_high = ImageFont.truetype("/fonts/OpenSans-Light.ttf", 35, encoding="unic")
    draw = ImageDraw.Draw(image_obj)

    for i, stat_el in enumerate(stat):
        offset = i * 75
        if 'http' in stat_el['image_URL']:
            cover_response = requests.get(stat_el['image_URL'])
            cover_img = Image.open(BytesIO(cover_response.content))
            cover_width, cover_height = cover_img.size
            if with_frame:
                frame_coords = [49, 49 + offset, 50 + cover_width, 50 + cover_height + offset]
                draw.rectangle(frame_coords, (0, 0, 0))
            image_obj.paste(cover_img, (50, 50 + offset))
        draw.text((140, 68 + offset), u"{}".format(stat_el['artist_name']), (0, 0, 0), font=font_low)
        draw.text((450, 55 + offset), "{}".format(stat_el['play_count']), (0, 0, 0), font=font_high)
    return image_obj


def save_image(image_obj, name):
    image_obj.save('static/{}.png'.format(name))
