import numpy as np
import pandas as pd


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

netflix_df = pd.read_csv('netflix_titles.csv')
amazon_df = pd.read_csv('amazon_prime_titles.csv')
hotstar_df = pd.read_csv('disney_plus_titles.csv')

dataset = pd.concat([netflix_df,amazon_df,hotstar_df],ignore_index = True)

def pre_process(dataset):
    tfidf = TfidfVectorizer(stop_words='english')
    dataset['description'] = dataset['description'].fillna('')
    tfidf_matrix = tfidf.fit_transform(dataset['description'])

    return tfidf_matrix

def sim(dataset):
    tfidf_matrix = pre_process(dataset)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    return cosine_sim

def tit_process(dataset):
    indices = pd.Series(dataset.index, index=dataset['title']).drop_duplicates()
    return indices

def get_recommendations_with_platform(dataset, title, cosine_sim=sim(dataset)):
    indices = tit_process(dataset)
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]
    recommended_titles = dataset['title'].iloc[movie_indices]
    recommended_platforms = dataset['platform'].iloc[movie_indices]

    recommended_df = pd.DataFrame({'Title': recommended_titles, 'Platform': recommended_platforms})
    return recommended_df


    
def get_titles(df):
    titles = df['title'].unique().tolist()
    result = []
    for item in titles:
        result.append(item)
    
    u_tit = list(set(result))
    u_tit.sort()
    return u_tit