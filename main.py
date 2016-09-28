import json
import os
import sys
import argparse

from api.google import ImageLinkCollector
from api.image import download_image, InvalidImageFormatError, get_faces, crop_face
from api.util import get_suffix


google_cloud_api_key = json.load(open("settings.json", "r"))["key"]
custom_search_id = json.load(open("settings.json", "r"))["custom_search_id"]


def main():
    parser = argparse.ArgumentParser(description='キーワードから顔の画像を収集します')
    parser.add_argument('-l', '--limit', type=int, default=1000, required=False, help="ダウンロード数の上限")
    parser.add_argument('-o', type=str, default="images", required=False, help="保存先のパス")
    parser.add_argument('words', nargs='+')

    args = parser.parse_args()

    os.makedirs("{output_dir}/tmp".format(output_dir=args.o), exist_ok=True)

    run(args.words, args.limit, args.o)


def run(words, limit, output_dir):
    count = 0

    words = " ".join(words)
    collector = ImageLinkCollector(google_cloud_api_key, custom_search_id, words, index=1, limit=limit)

    if not os.path.exists("{save_dir}/{words}".format(save_dir=output_dir, words=words)):
        os.mkdir("{save_dir}/{words}".format(save_dir=output_dir, words=words))

    for link_url in collector:
        try:
            filename = download_image(link_url)
        except InvalidImageFormatError as e:
            print(e, file=sys.stderr)
            continue

        try:
            faces = get_faces(filename)
        except Exception as e:
            print(e, file=sys.stderr)
            continue

        for face in faces:
            suffix = get_suffix(filename)
            try:
                img = crop_face(filename, face)
            except InvalidImageFormatError:
                continue
            except Exception as e:
                print(e, file=sys.stderr)
                continue
            face_filename = "{save_dir}/{words}/{count}{suffix}".format(save_dir=output_dir, words=words, count=str(count).zfill(3), suffix=suffix)
            img.save(face_filename)
            count += 1


if __name__ == '__main__':
    main()
