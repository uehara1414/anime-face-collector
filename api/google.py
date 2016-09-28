import requests
import base64
import json


class ImageLinkCollector:

    CUSTOM_SEARCH_API_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, key, cx, word, index=1, limit=100):
        self.index = index
        self.key = key
        self.cx = cx
        self.word = word
        self.limit = limit
        self.cnt = 0
        self.links = list()

    def __iter__(self):
        return self

    def __next__(self):
        if self.cnt > self.limit:
            raise StopIteration()
        if len(self.links) <= 0:
            self.links = self.get_next_links(10)

        self.cnt += 1
        return self.links.pop(0)

    def get_next_links(self, num=10):
        q = {
            "key": self.key,
            "q": self.word,
            "cx": self.cx,
            "start": self.index,
            "num": num,
            "searchType": "image"
        }
        self.index += num
        ret = requests.get(ImageLinkCollector.CUSTOM_SEARCH_API_URL, params=q)
        if ret.status_code == 400:
            raise StopIteration("全件検索が終了しました")
        ret = json.loads(ret.text)
        json.dump(ret, open("out.json", "w", encoding="utf8"), indent=4)
        self.index = int(ret["queries"]["nextPage"][0]["startIndex"])

        links = list()
        for item in ret["items"]:
            link = item["link"]
            links.append(link)
        return links