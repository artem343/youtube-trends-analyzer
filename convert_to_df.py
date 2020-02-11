import pandas as pd


def create_df_for_plotting(save=True):
    """
    Prepares a dataframe for plotting.
    """
    df = pd.read_csv('daily/most_recent.csv')

    df_unstacked = (
        df.groupby(["locale", "category"])["id"]
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
    create_df_for_plotting()
