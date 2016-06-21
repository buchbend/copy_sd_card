from PIL import Image

def get_date_taken(path):
    return Image.open(path)._getexif()[36867]
