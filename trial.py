import glob
import os
import youtube_dl
import requests
import bs4
import re
import glob
import shutil


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


class SubtitleProcessor:
    """
    Extracting subtitles from video
    """

    def __init__(self):
        pass

    def extract_text_only(self, file):
        return ""


class VideoProcessor:
    """

    """

    def __init__(self, locale):
        self.locale = locale
        self.path = f"subs\\{self.locale}"

    def set_locale(self, locale):
        self.locale = locale
        self.path = f"subs\\{self.locale}"

    def get_video_list(self, n_videos=20):
        url = f"https://www.youtube.com/feed/trending?gl={self.locale}&hl=en"
        soup = bs4.BeautifulSoup(
            requests.get(url).content.decode("utf-8", "ignore"), "html.parser"
        )
        hrefs = []
        code = soup.find(class_="content-region").text
        # if region wasn't set for required locale, it means youtube doesn't have this locale
        if code == self.locale:
            for a in soup.find_all("a", href=True):
                if re.search(r"[^com]\/watch", str(a)):
                    hrefs.append(a["href"])
            hrefs = [f"https://www.youtube.com{link}" for link in hrefs[::2]]
        # Return only most important links: some locales have    too many trends
        return hrefs[:n_videos]

    def download_subs(self, lang="en"):
        opts = {
            "skip_download": True,
            "writeinfojson": True,
            "subtitlelangs": lang,
            "writesubtitles": True,
            "writeautomaticsub": "%(id)s",
            "subtitlesformat": "srv1",
        }

        hrefs = self.get_video_list()
        if len(hrefs):
            with youtube_dl.YoutubeDL(opts) as yt:
                yt.download(hrefs)
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
        srvs = glob.glob("*.srv1")
        # Move .srv1 and .json files to locale dir
        for file in srvs:
            print(f"Moving file {file} to {self.locale}")
            shutil.move(file, dest_dir)
            jsonfile = f"{file[:-8]}.info.json"
            shutil.move(jsonfile, dest_dir)
        # Remove remaining .json files
        left_jsons = glob.glob("*.info.json")
        for file in left_jsons:
            os.remove(file)
        return 0

    def read_subtitles_into_dict(self):

        path = f"{self.path}\\*.srv1"
        text_lang = {}
        for filename in glob.glob(path):
            processor = SubtitleProcessor()
            with open(filename, "r") as f:
                data = f.readlines()
            # FIXME: edit these two lines
            text = processor.extract_text_only(data)
            text_lang[locale] = text
        return text_lang


if __name__ == "__main__":
    with open("locales.txt", "r") as locfile:
        locales = locfile.readlines()
    for locale in locales[:5]:
        vp = VideoProcessor(locale[:-1])
        result = vp.download_subs("en")
        if not result:
            print(f"Failed to download subtitle for {locale[:-1]}")
