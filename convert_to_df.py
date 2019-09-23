import glob
import os
import json
import pandas as pd
import numpy as np

# class Video:
#     """
#     One youtube video with subtitles and data.
#     """

#     def __init__(self, locale, id, url, title, duration, text):
#         self.id = id
#         self.locale = locale
#         self.url = url
#         self.title = title
#         self.duration = duration
#         self.text = text

#     def __repr__(self):
#         print(f'<Video "{self.title[:10]}" from {self.locale} (id {self.id})>')

#     def determine_text_topic(self):
#         """

#         """
#         pass


def create_df_videos():
    with open("locales.txt", "r") as locfile:
        locales = locfile.readlines()

    df_videos = pd.DataFrame()
    for locale in locales:
        try:
            locale_df = create_df_videos_for_locale(locale[:-1])
            df_videos = df_videos.append(locale_df, ignore_index=True)
        except Exception as e:
            print(f"No json for {locale}. {e}")

    print(f"df_videos.shape = {df_videos.shape}")
    # df_videos.to_csv('videos.csv')
    return df_videos


def create_df_videos_for_locale(locale):
    df_video_locale = pd.DataFrame()
    with open(f"subs/{locale}/data.json", "r") as f:
        j = json.load(f)

    for video in j[locale]:
        new_row = {
            "locale": locale,
            "id": video["id"],
            "text": video["text"],
            "topics": [],
            "main_topic": "",
        }
        df_video_locale = df_video_locale.append(new_row, ignore_index=True)

    return df_video_locale


if __name__ == "__main__":
    create_df_videos()
