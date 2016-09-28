from PIL import Image
import cv2
import requests

from .util import get_suffix


class InvalidImageFormatError(BaseException):
    pass


def get_faces(img_path, cascade_file = "lbpcascade_animeface.xml"):
    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(24, 24))
    return faces


def crop_face(image_path, face, min_size=(120, 120)):
    if not get_suffix(image_path):
        raise InvalidImageFormatError("拡張子がよくない")

    img = Image.open(image_path)
    x1, y1 ,x2, y2 = (face[0], face[1], face[0] + face[2], face[1] + face[3])
    cropped = img.crop((x1, y1, x2, y2))

    if cropped.size[0] <= min_size[0] or cropped.size[1] <= min_size[1]:
        raise InvalidImageFormatError("サイズちいさすぎる")

    return cropped


def download_image(link):
    ret = requests.get(link, allow_redirects=False)

    suffix = get_suffix(link)
    if not suffix:
        raise InvalidImageFormatError("不正なファイルです ( 処理が面倒くさいから省いてるだけ )")

    filename = "images/tmp/tmp{}".format(suffix)
    open(filename, "wb").write(ret.content)
    return filename
