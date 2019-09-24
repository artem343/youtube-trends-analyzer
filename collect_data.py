import glob
import os
import youtube_dl
import requests
import bs4
import re
import shutil
import json
import xml.dom.minidom as minidom


class Video:
    """
    A single youtube video with URL and metadata.
    """

    def __init__(self, locale, id, data_json):
        self.id = id
        self.locale = locale
        self.data = data_json
        self.text = ""

    def __repr__(self):
        return f"<{self.id} from {self.locale}>"


class VideoProcessor:
    """

    """

    def __init__(self, locale):
        self.set_locale(locale)

    def set_locale(self, locale):
        self.locale = locale
        self.path = f"subs/{locale}"

    def get_video_list(self, n_videos=20):
        url = f"https://www.youtube.com/feed/trending?gl={self.locale}&hl=en"
        soup = bs4.BeautifulSoup(
            requests.get(url).content.decode("utf-8", "ignore"), "html.parser"
        )
        hrefs = []
        locale_exists = False
        code = soup.find(class_="content-region")
        # if region wasn't set for required locale, it means youtube doesn't have this locale
        try:
            if code.text == self.locale:
                locale_exists = True
            if (code is None) and (self.locale == "US"):
                locale_exists = True
        except:
            pass
        if locale_exists:
            for a in soup.find_all("a", href=True):
                if re.search(r"[^com]\/watch", str(a)):
                    hrefs.append(a["href"])
            hrefs = [f"https://www.youtube.com{link}" for link in hrefs[::2]]
        # Return only most important links: some locales have    too many trends
        return hrefs[:n_videos]

    def clear_locale_folder(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
            print(f"Deleted {self.path}")

    def download_subs(self, lang="en"):
        self.clear_locale_folder()

        opts = {
            "skip_download": True,
            "writeinfojson": True,
        }

        hrefs = self.get_video_list()
        if len(hrefs):
            with youtube_dl.YoutubeDL(opts) as yt:
                try:
                    yt.download(hrefs)
                except youtube_dl.utils.DownloadError as e:
                    print(e)
            # TODO: find options how to download subs directly to folder
            self.move_subs(self.locale)
            return 1
        else:
            return 0

    def move_subs(self, locale):
        """
        Move subtitles to a respective folder. Call immediately after downloading.
        """
        dest_dir = self.path
        os.makedirs(dest_dir, exist_ok=True)
        jsons = glob.glob("*.info.json")
        # Move .srv1 and .json files to locale dir
        for file in jsons:
            print(f"Moving file {file} to {self.locale}")
            shutil.move(file, dest_dir)
        # Remove remaining .json files
        return 0

    def read_locale_into_dict(self):
        """
        Create a dictionary with all the video data from current locale.
        """
        jsons = glob.glob(f"{self.path}/*.info.json")
        locale_dicts = []
        for json_path in jsons:
            # with open(srv_path, "r", encoding="utf-8") as srv_f:
            #     # parse srv
            #     dom = minidom.parse(srv_f)
            #     lines = []
            #     try:
            #         for node in dom.getElementsByTagName("text"):
            #             lines.append(node.firstChild.nodeValue)
            #         text = " ".join(lines)
            #         text = re.sub(r"[^a-zA-Z ]+", "", text).lower()
            #     except Exception:
            #         text = "unknown"
            with open(json_path, "r") as json_f:
                # parse json
                j = json.load(json_f)
                video_dict = {
                    "id": j["id"],
                    "url": j["webpage_url"],
                    "title": j["title"],
                    "duration": j["duration"],
                    "views": j["view_count"],
                    "likes": j["like_count"],
                    "dislikes": j["dislike_count"],
                    "categories": j["categories"]
                }
            locale_dicts.append(video_dict)
        return locale_dicts


if __name__ == "__main__":
    with open("locales.txt", "r") as locfile:
        locales = locfile.readlines()

    vp = VideoProcessor("RU")
    for locale in locales:
        locale = locale[:-1]
        vp.set_locale(locale)
        result = vp.download_subs("en")
        if result:
            locale_dicts = vp.read_locale_into_dict()
            with open(f"{vp.path}/data.json", "w") as outfile:
                json.dump({locale: locale_dicts}, outfile)
        else:
            print(f"Failed to download subtitle for {locale}")
