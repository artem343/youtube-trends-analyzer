import glob
import os
import json
import pandas as pd
import numpy as np


def create_df_videos():
    with open("locales.txt", "r") as locfile:
        locales = locfile.readlines()

    df_videos = pd.DataFrame()
    for locale in locales:
        try:
            locale_df = create_df_videos_for_locale(locale[:-1])
            df_videos = df_videos.append(locale_df, ignore_index=True)
        except Exception:
            print(f"No json for {locale}")

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
            "title": video["title"],
            "categories": video["categories"],
        }
        df_video_locale = df_video_locale.append(new_row, ignore_index=True)

    return df_video_locale


def create_df_for_plotting(save=True):
    """
    Prepares a dataframe for plotting 
    """
    df_videos = create_df_videos()
    df = df_videos
    df["categories"] = df["categories"].apply(lambda x: x[0])

    df_unstacked = (
        df.groupby(["locale", "categories"])["id"]
        .count()
        .unstack()
        .fillna(0.0)
        .astype(int)
    )
    df_unstacked = df_unstacked.div(df_unstacked.sum(axis=1), axis=0)
    df_unstacked.index.name = "locale2"

    df_locale = pd.read_csv("locales.csv")
    df_locale.drop(["Numeric code"], axis=1, inplace=True)
    df_locale.columns = ["name", "locale2", "locale3", "lat_avg", "lon_avg"]

    for column in df_locale.columns:
        df_locale[column] = df_locale[column].str.replace('"', "")
        df_locale[column] = df_locale[column].str.strip()

    df_locale.drop_duplicates("locale2", keep="last", inplace=True)
    df_locale.set_index("locale2", inplace=True)

    df = df_locale.merge(df_unstacked, left_index=True, right_index=True)

    if save:
        df.to_csv("main.csv")

    return df


if __name__ == "__main__":
    df = create_df_for_plotting(save=True)
