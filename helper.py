import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import streamlit as st
import numpy as np

netflix_df = pd.read_csv('netflix_titles.csv')
amazon_df = pd.read_csv('amazon_prime_titles.csv')
hotstar_df = pd.read_csv('disney_plus_titles.csv')

dataset = pd.concat([netflix_df,amazon_df,hotstar_df],ignore_index = True)

dataset_shows=dataset[dataset['type']=='TV Show']
dataset_movies=dataset[dataset['type']=='Movie']
netflix_shows=netflix_df[netflix_df['type']=='TV Show']
netflix_movies=netflix_df[netflix_df['type']=='Movie']
amazon_shows=amazon_df[amazon_df['type']=='TV Show']
amazon_movies=amazon_df[amazon_df['type']=='Movie']
hotstar_shows=hotstar_df[hotstar_df['type']=='TV Show']
hotstar_movies=hotstar_df[hotstar_df['type']=='Movie']

def get_unique_countries(df):
    stream_countries = df['country'].unique().tolist()
    result = []
    for item in stream_countries:
        if isinstance(item, str):
            country_list = item.split(',')
            country_list = [country.strip().strip("'") for country in country_list]
            result.extend(country_list)

    unique_countries = list(set(result))
    unique_countries.sort()
    return unique_countries



def generate_content_type_distribution(dataset, country, palette):
    filtered_data = dataset[dataset['country'] == country]
    content_type_counts = filtered_data['type'].value_counts()
    
    # Check if content_type_counts is empty
    if content_type_counts.empty:
        st.error("No data available for the selected country.")
        return None
    
    fig, ax = plt.subplots()
    sns.barplot(x=content_type_counts.index, y=content_type_counts.values, palette=palette)
    ax.set_xlabel('Content Type')
    ax.set_ylabel('Count')
    ax.set_title(f'Content Type Distribution in {country}')
    
    return fig

def generate_platform_content_pie_charts(dataset):
    content_counts = dataset.groupby('platform')['type'].value_counts().unstack()

    for platform in content_counts.index:
        counts = content_counts.loc[platform]
        fig = px.pie(counts, values=counts.values, names=counts.index, title=platform)
        st.plotly_chart(fig, use_container_width=True)

def generate_content_type_bar_distribution(netflix_df, amazon_df, hotstar_df):

    sns.set(style="darkgrid")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    sns.countplot(x="type", data=netflix_df, palette="Set2", ax=axes[0])
    axes[0].set_title("Netflix Content Type Distribution")
    
    sns.countplot(x="type", data=amazon_df, palette="Set2", ax=axes[1])
    axes[1].set_title("Amazon Content Type Distribution")
    
    sns.countplot(x="type", data=hotstar_df, palette="Set2", ax=axes[2])
    axes[2].set_title("Hotstar Content Type Distribution")
    
    st.pyplot(fig)

def generate_movies_by_year_plot(dataset):
    movies_df = dataset[dataset['type'] == 'Movie']

    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(40, 20))
    sns.countplot(x="release_year", data=movies_df, hue="platform", palette="Set1", ax=ax)
    ax.set_title("Number of Movies by Year", fontsize=70)
    ax.tick_params(axis='x', rotation=45,labelsize=30)
    for label in ax.get_legend().get_texts():
        label.set_fontsize(40)
    plt.tight_layout()
    st.pyplot(fig)


def generate_shows_by_year_plot(dataset):
    shows_df = dataset[dataset['type'] == 'TV Show']
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(30, 15))
    sns.countplot(x="release_year", data=shows_df, hue="platform", palette="Set1", ax=ax)
    ax.set_title("Number of Shows by Year", fontsize=50)
    ax.tick_params(axis='x', rotation=45,labelsize=30)
    for label in ax.get_legend().get_texts():
        label.set_fontsize(40)
    plt.tight_layout()
    st.pyplot(fig)

def generate_netflix_shows_update_heatmap(netflix_shows):
    netflix_date = netflix_shows[['date_added']].dropna()
    netflix_date['year'] = netflix_date['date_added'].apply(lambda x: x.split(', ')[-1])
    netflix_date['month'] = netflix_date['date_added'].apply(lambda x: x.lstrip().split(' ')[0])

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][::-1]
    df = netflix_date.groupby('year')['month'].value_counts().unstack().fillna(0)[month_order].T
    
    plt.figure(figsize=(10, 6), dpi=80)
    plt.pcolor(df, cmap='afmhot_r', edgecolors='white', linewidths=2)  # heatmap
    plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns, fontsize=10, fontfamily='serif')
    plt.yticks(np.arange(0.5, len(df.index), 1), df.index, fontsize=10, fontfamily='serif')

    plt.title('Netflix Shows Update', fontsize=12, fontweight='bold', pad=20)
    cbar = plt.colorbar()

    cbar.ax.tick_params(labelsize=10)
    cbar.ax.minorticks_on()

    # Display the figure inside the container
    st.pyplot(plt)

def generate_netflix_movies_update_heatmap(netflix_movies):
    netflix_date = netflix_movies[['date_added']].dropna()
    netflix_date['year'] = netflix_date['date_added'].apply(lambda x: x.split(', ')[-1])
    netflix_date['month'] = netflix_date['date_added'].apply(lambda x: x.lstrip().split(' ')[0])

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][::-1]
    df = netflix_date.groupby('year')['month'].value_counts().unstack().fillna(0)[month_order].T
    
    plt.figure(figsize=(12, 8), dpi=80)
    plt.pcolor(df, cmap='afmhot_r', edgecolors='white', linewidths=2)  # heatmap
    plt.xticks(np.arange(0.9, len(df.columns), 1), df.columns, fontsize=12, fontfamily='serif')
    plt.yticks(np.arange(0.9, len(df.index), 1), df.index, fontsize=12, fontfamily='serif')

    plt.title('Netflix Movies Update', fontsize=16, fontweight='bold', pad=20)
    cbar = plt.colorbar()

    cbar.ax.tick_params(labelsize=14)
    cbar.ax.minorticks_on()
    
    st.pyplot(plt)

def generate_movies_release_year_bar_plot(dataset_movies):
    plt.figure(figsize=(8, 5))
    sns.set(style="darkgrid")
    ax = sns.countplot(y="release_year", data=dataset_movies, palette="Set1",
                       order=dataset_movies['release_year'].value_counts().index[0:15])
    return ax

def generate_shows_release_year_bar_plot(dataset_shows):
    plt.figure(figsize=(8, 5))
    sns.set(style="darkgrid")
    ax = sns.countplot(y="release_year", data=dataset_shows, palette="Set1",
                       order=dataset_shows['release_year'].value_counts().index[0:15])
    return ax

def generate_movies_duration_distribution(netflix_movies, amazon_movies, hotstar_movies):
    sns.set(style="darkgrid")
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    netflix_movies['duration'] = netflix_movies['duration'].str.replace(' min', '').astype(float)
    amazon_movies['duration'] = amazon_movies['duration'].str.replace(' min', '').astype(float)
    hotstar_movies['duration'] = hotstar_movies['duration'].str.replace(' min', '').astype(float)
    
    sns.kdeplot(data=netflix_movies['duration'], fill=True, ax=axes[0])
    axes[0].set_title("Duration of Movies on Netflix")
    
    sns.kdeplot(data=amazon_movies['duration'], fill=True, ax=axes[1])
    axes[1].set_title("Duration of Movies on Amazon")
    
    sns.kdeplot(data=hotstar_movies['duration'], fill=True, ax=axes[2])
    axes[2].set_title("Duration of Movies on Hotstar")
    
    st.pyplot(fig)

def top10_max_duration_movies_barplot(df, n=10):
    df = df.dropna(subset=['duration'])
    df['duration'] = df['duration'].astype(str)
    df['duration'] = df['duration'].str.replace(' min', '')
    df['duration'] = df['duration'].astype(int)

    max_duration_movies = df.sort_values('duration', ascending=False).head(n)

    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=max_duration_movies, y='title', x='duration', palette='viridis')

    plt.title(f"Top {n} Movies with Maximum Duration")
    plt.xlabel("Duration (minutes)")
    plt.ylabel("Movie Title")
    plt.tight_layout()

    return fig

def top10_max_duration_season_barplot(df):
    features=['title','duration']
    durations = df[features]

    durations['no_of_seasons'] = durations['duration'].str.replace(' Season','').str.replace('s','')
    durations['no_of_seasons'] = durations['no_of_seasons'].astype(str).astype(int)

    top10 = durations.sort_values(by='no_of_seasons', ascending=False).head(10)

    fig = plt.figure(figsize=(10, 6))
    plt.bar(top10['title'], top10['no_of_seasons'], color='blue')
    plt.title("Maximum Season Shows")
    plt.xlabel("Title")
    plt.ylabel("Number of Seasons")
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

def generate_top_genres_pie_chart(dataset,platform):
    df_group_genre = dataset.groupby(['platform','listed_in','type']).count()['show_id'].reset_index()
    top10_df = df_group_genre[df_group_genre['platform'] == platform].sort_values('show_id', ascending=False)[:10]['listed_in'].values.tolist()

    filtered_data = dataset[(dataset['platform'] == 'netflix') & (dataset['listed_in'].isin(top10_df))]

    genre_counts = filtered_data['listed_in'].value_counts()

    fig = plt.figure(figsize=(4, 4))
    sns.set_palette('Set2')
    plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=90)

    plt.title('Top 10 genres on Netflix', fontweight='bold', fontsize=14)
    plt.axis('equal')

    return fig

def plot_content_rating(dataset):
    fig, ax = plt.subplots(figsize=(50, 30))
    sns.set(style="darkgrid")

    cp = sns.countplot(x="rating", data=dataset, hue="platform", palette=["#1b2530", "#0f79af", "#E50914"], ax=ax)
    cp.set_title("Contents Rating by Platform", fontsize=30)
    cp.set_xlabel("Rating")
    cp.set_ylabel("Count")

    # Adjust font size of tick labels
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)

    ax.legend(title="Platform", loc="upper right")

    return fig