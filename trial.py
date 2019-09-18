import glob
import os
import youtube_dl
import requests
import bs4
import re
import glob
import shutil


class SubtitleProcessor:
    """
    
    """

    def __init__(self):
        pass

    def extract_text_only(self, lines):
        linelist = []
        for line in lines:
            if re.match(r'^[A-Za-z\s\']*$', line):
                line = re.sub(r'[^\w\s]+', '', line)
                line = line.strip()
                if line:
                    linelist.append(line)
        linelist = linelist[1::2]
        return ' '.join(linelist)

    def extract_text_with_timestamps(self, lines):
        return ""


class SubtitleDownloader:
    """

    """

    def __init__(self, locale):
        self.locale = locale
        self.path = f"subs\\{self.locale}"

    def set_locale(self, locale):
        self.locale = locale
        self.path = f"subs\\{self.locale}"

    def get_video_list(self):
        url = f"https://www.youtube.com/feed/trending?gl={self.locale}&hl=en"
        soup = bs4.BeautifulSoup(
            requests.get(url).content.decode("utf-8", "ignore"), "html.parser"
        )

        hrefs = []
        for a in soup.find_all("a", href=True):
            if re.search(r"[^com]\/watch", str(a)):
                hrefs.append(a["href"])
        hrefs = [f"https://www.youtube.com{link}" for link in hrefs[::2]]
        return hrefs

    def download_subs(self, lang="en"):
        opts = {
            "skip_download": True,
            "writeinfojson": True,
            "subtitlelangs": lang,
            "writesubtitles": True,
            "writeautomaticsub": "%(id)s",
            "subtitlesformat": "vtt",
        }

        urls = self.get_video_list()
        with youtube_dl.YoutubeDL(opts) as yt:
            yt.download(urls)
        self.move_subs(self.locale)

    def move_subs(self, locale):
        """
        Move subtitles to a respective folder. Call immediately after downloading.
        """
        dest_dir = self.path
        os.makedirs(dest_dir, exist_ok=True)
        for file in glob.glob(r"*.vtt"):
            print(file)
            shutil.move(file, dest_dir)

    def read_subtitles_into_dict(self):

        path = f"{self.path}\\*.vtt"
        text_lang = {}
        for filename in glob.glob(path):
            processor = SubtitleProcessor()
            with open(filename, "r") as f:
                data = f.readlines()
            text = processor.extract_text_only(data)
            
        return text_lang


if __name__ == "__main__":
    d = SubtitleDownloader("RU")
    # d.download_subs("en")
    sub_dict = d.read_subtitles_into_dict()
    # print(sub_dict)
