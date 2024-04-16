import streamlit as st
import pickle
import time
import requests

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

st.image("./Movies.jpg")
st.write("""
# Movie Recommendation System App

This app recommends movies!
""")
st.write("---")

selected_movie = st.selectbox("Select a movie", movies.title)
def fetch_genres(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=988b04df460894f5184de7c80a96c65a&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    genre_s = data['genres']
    genres = []
    for genre in genre_s:
        genres.append(genre.get('name'))
    return genres
def fetch_vote_average(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=988b04df460894f5184de7c80a96c65a&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    vote_average = data['vote_average']
    return vote_average
def fetch_release_date(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=988b04df460894f5184de7c80a96c65a&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    release_date = data['release_date']
    return release_date
def fetch_overview(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=988b04df460894f5184de7c80a96c65a&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    overview = data['overview']
    return overview
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=988b04df460894f5184de7c80a96c65a&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda vector:vector[1])
    recommended_movies = []
    recommended_posters = []
    recommended_overviews = []
    recommended_release_dates = []
    recommended_vote_averages = []
    recommended_genres = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movies_id))
        recommended_overviews.append(fetch_overview(movies_id))
        recommended_release_dates.append(fetch_release_date(movies_id))
        recommended_vote_averages.append(fetch_vote_average(movies_id))
        recommended_genres.append(fetch_genres(movies_id))
    return recommended_movies, recommended_posters, recommended_overviews, recommended_release_dates, recommended_vote_averages, recommended_genres
if st.button(":red[Show recommendations]"):
    bar = st.progress(0)
    time.sleep(0.1)
    bar.progress(50)
    time.sleep(2)
    bar.progress(100)
    time.sleep(0.5)
    bar.empty()
    recommended_movies_names, recommended_movies_posters, recommended_movies_overviews, recommended_release_dates, recommended_vote_averages, recommended_genres = recommend(selected_movie)
    for i in range(5):
        st.text(recommended_movies_names[i])
        st.image(recommended_movies_posters[i], width = 200)
        st.caption(recommended_movies_overviews[i])
        st.caption(recommended_release_dates[i])
        st.caption(str(recommended_vote_averages[i]) + ":star:")
        st.caption(recommended_genres[i])
        st.write("---")
