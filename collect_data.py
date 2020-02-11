import pandas as pd
import numpy as np
import datetime

# YouTube API
import os
# import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_popular_videos(locale: str, n_videos: int = 20) -> list:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBTyEBWte34jgNMt4bltz3vUgmTWkGLUac"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(api_service_name, api_version,
                                              developerKey=DEVELOPER_KEY)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        maxResults=n_videos,
        regionCode=locale
    )
    videos = request.execute()

    return videos


def select_locales() -> list:
    """
    Return country codes only for countries that are available on YouTube,
    stored in 'available_countries.txt'.
    """
    df_locale = pd.read_csv("locales.csv")

    with open('available_countries.txt', 'r') as f:
        countries = f.read()
    country_names = countries.split('\n')

    df_locale = df_locale[df_locale['Country'].isin(country_names)]
    locales = df_locale["Alpha-2 code"].tolist()
    locales = ['NA' if x is np.nan else x for x in locales]
    return locales


def collect_data():
    """
    Main method for daily data collection.
    Stores results in daily/<date>.csv and
    daily/most_recent.csv for future plotting.
    """
    df = pd.DataFrame()
    df_categories = pd.read_csv("categories.csv")
    locales = select_locales()
    for locale in locales[:2]:
        print(f"Processing {locale}...")
        j_videos = get_popular_videos(locale, n_videos=20)
        videos = []
        for video in j_videos['items']:
            try:
                videos.append([
                    video['id'],
                    video['snippet']['categoryId'],
                    video['statistics']['viewCount'],
                    video['statistics']['likeCount'],
                    video['statistics']['dislikeCount'],
                    video['statistics']['commentCount'],
                    video['snippet']['title']
                ])
            except KeyError as e:
                print(f"{repr(e)} at {video['id']} of {locale}")
        df_videos = pd.DataFrame(videos,
                                 columns=['id', 'category', 'views',
                                          'likes', 'dislikes',
                                          'comments', 'video_name'])
        df_videos['locale'] = locale
        df = pd.concat([df, df_videos])

    df['date_requested'] = datetime.date.today()
    df['date_requested'] = pd.to_datetime(df['date_requested'])
    df = df.astype({'category': 'int32', 'views': 'int32',
                    'likes': 'int32', 'dislikes': 'int32',
                    'comments': 'int32'})
    df = df.merge(df_categories, left_on='category', right_on='id')
    df.drop(['category', 'id_y'], axis=1, inplace=True)
    df.rename({'title': 'category', 'video_name': 'title', 'id_x': 'id'},
              axis=1, inplace=True)
    df.set_index('id', inplace=True)
    df.to_csv(f'daily/{datetime.date.today()}.csv')
    df.to_csv(f'daily/most_recent.csv')


if __name__ == "__main__":
    collect_data()
