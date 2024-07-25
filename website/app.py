import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'YOUR KEY'

def get_recommendations(title):
        # get idx of the movie in the dataframe
        idx = movies[movies["title"] == title].index[0]
        # open the idx'th data in cosine_sim in the form of (index, cosine similarity score)
        sim_scores = list(enumerate(cosine_sim[idx]))
        # sorted in reverse order about the cosine similarity score
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # 자기 자신을 제외한 10개의 추천 영화 슬라이싱
        sim_scores = sim_scores[1:11]
        # indices of the recommended movies
        movie_indices = [i[0] for i in sim_scores]
        # titles of the recommended movies
        images = []
        titles = []
        for i in movie_indices:
            id = movies['id'].iloc[i]
            details = movie.details(id)

            image_path = details.poster_path
            if image_path:
                image_path = 'https://image.tmdb.org/t/p/w500' + image_path
            else:
                image_path = 'no_image.jpg'

            images.append(image_path)
            titles.append(details.title)
        return images, titles

movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout="wide")
st.header('StreamFlix')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like.', movie_list)
if st.button('Recommend'):
    with st.spinner('Please wait...'):
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0, 2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1
