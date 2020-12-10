# /////////////////////////////////////////////////////////
import numpy as np
import pandas as pd 
import joblib
import streamlit as st
import datetime
import matplotlib.pyplot as plt

# /////////////////////////////////////////////////////////
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import bs4 as bs
import urllib.request
import pickle
import requests

# load the nlp model and tfidf vectorizer from disk
filename = 'saved_models/nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('saved_models/tranform.pkl','rb'))

# /////////////////////////////////////////////////////////
from tmdbv3api import TMDb, Movie
import json
import requests
tmdb = TMDb()
tmdb.api_key = '372d27dc5adf49b680f074659a3c6d9a'
tmdb_movie = Movie() 

# /////////////////////////////////////////////////////////
def print_details(msg1, msg2):
    # style="background-color:blue;padding:2px"
    html_temp = """
    <div >
    <span><a style="color:white;text-align:Left; font-size:20px">{} </a></span>
    <span><a style="color:black;text-align:Center; font-size:15px">{} </a></span>
    </div>
    """
    st.markdown(html_temp.format(msg1, msg2), unsafe_allow_html=True)

def create_similarity():
    data = pd.read_csv('datasets/MovieRecommendationSystem/main_data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity

def recommend(movie_name):
    m = movie_name.lower()

    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()

    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

def searchMovieName(movie_name):
    query = "https://api.themoviedb.org/3/search/movie?api_key={}&query={}".format(tmdb.api_key, movie_name)
    response = requests.get(query)
    data_json = response.json()
    # st.write("query : {}".format(query))
    return data_json

def getMoveiDetails(movie_id):
    query = 'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, tmdb.api_key)
    response = requests.get(query)
    movie_details = response.json()
    return movie_details

def show_similar_movie_posters(recommendations):

    html_temp = """
    <div style="padding:2px">
    <h3 style="color:white;text-align:center;">{} </h3>
    </div>
    """
    msg = "RECOMMENDED MOVIES FOR YOU"
    st.markdown(html_temp.format(msg), unsafe_allow_html=True)

    
    poster_path = []
    for movie in recommendations:
        movie_details = searchMovieName(movie)
        path = "https://image.tmdb.org/t/p/original{}".format(movie_details["results"][0]["poster_path"])
        poster_path.append(path)

    noofcols = 3
    length = len(poster_path) // noofcols
    if len(poster_path) % noofcols:
        length = length + 1

    for i in range(length):
        start = i * noofcols
        end = start + noofcols

        # im_row = ["""<li><a><img class="rec_movie" src='{}'></a></li>""".format(im) for im in poster_path[start:end]]    
        im_row=[]
        for idx, im in enumerate(poster_path[start:end]):
            # fig = """<li><a><figure><img class="rec_movie" src='{}'><figcaption>{}</figcaption></figure></a></li>""".format(im, recommendations[start+idx])
            fig = """<li><a><figure><img class="rec_movie" src='{}'></figure></a></li>""".format(im)
            im_row.append(fig)
        im_markdown = """<div>{}<div>""".format("".join(im_row))
        st.markdown(im_markdown, unsafe_allow_html=True)

def show_movie_reviews(imdb_id):
    # web scraping to get user reviews from IMDB site
    sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    soup_result = soup.find_all("div",{"class":"text show-more__control"})

    reviews_list = [] # list of reviews
    reviews_status = [] # list of comments (good or bad)
    for reviews in soup_result:
        if reviews.string:
            reviews_list.append(reviews.string)
            # passing the review to our model
            movie_review_list = np.array([reviews.string])
            movie_vector = vectorizer.transform(movie_review_list)
            pred = clf.predict(movie_vector)
            reviews_status.append('Good' if pred else 'Bad')

    # combining reviews and comments into a dictionary
    movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}

    html_temp = """<div style="padding:2px"><h3 style="color:white;text-align:center;">{}</h3></div>"""
    msg = "USER REVIEWS"
    st.markdown(html_temp.format(msg), unsafe_allow_html=True)

    table_rows = []
    for review, status in movie_reviews.items():
        sts = ""
        if status =='Good':
            sts = "&#128515;"
        else:
            sts = "&#128534;"
        row = """<tr style="background-color:rgba(255,127,127,255);"><td>{}</td><td><center>{}</center></td></tr>""".format(review, sts)
        table_rows.append(row)

    html_code = """<center>
                    <div style="margin: 0 auto; "> <!-- margin-top:25px; -->
                        <table bordercolor="white"> <!--style="color:green" -->
                            <thead><tr style="background-color:rgba(0, 0, 0, 0);>
                                    <th scope="col" style="width: 70%">
                                        <center>Comments</center>
                                    </th>
                                    <th scope="col"><center> Sentiments </center></th>
                            </tr></thead>
                            <tbody> {} </tbody>
                        </table>
                    </div>
                </center>""".format("".join(table_rows))
    st.markdown(html_code, unsafe_allow_html=True)

def show_movie_cast(movie_id):
    html_temp = """
    <div style="padding:2px">
    <h3 style="color:white;text-align:center;">{} </h3>
    </div>
    """
    msg = "TOP CAST"
    st.markdown(html_temp.format(msg), unsafe_allow_html=True)

    # "https://api.themoviedb.org/3/movie/"+movie_id+"/credits?api_key="+my_api_key
    query = 'https://api.themoviedb.org/3/movie/{}/credits?api_key={}'.format(movie_id, tmdb.api_key)
    response = requests.get(query)
    movie_details = response.json()

    cast_img_path = []
    cast_name = []
    length = len(movie_details["cast"])
    if length >= 10:
        for i in range(10):
            path = "https://image.tmdb.org/t/p/original{}".format(movie_details["cast"][i]["profile_path"])
            cast_img_path.append(path)
            cast_name.append(movie_details["cast"][i]["name"])
    else:
        for i in range(length):
            path = "https://image.tmdb.org/t/p/original{}".format(movie_details["cast"][i]["profile_path"])
            cast_img_path.append(path)
            cast_name.append(movie_details["cast"][i]["name"])

    noofcols = 4
    length = len(cast_img_path) // noofcols
    if len(cast_img_path) % noofcols:
        length = length + 1
    for i in range(length):
        start = i * noofcols
        end = start + noofcols

        # im_row = ["""<li><a><img class="cast" src='{}'></a></li>""".format(im) for im in cast_img_path[start:end]]
        im_row=[]
        for idx, im in enumerate(cast_img_path[start:end]):
            fig = """<li><a><figure><img class="cast" src='{}'><figcaption>{}</figcaption></figure></a></li>""".format(im, cast_name[start+idx])
            im_row.append(fig)
        im_markdown = """<div>{}<div>""".format("".join(im_row))
        st.markdown(im_markdown, unsafe_allow_html=True)

def get_similarity(movie_id, movie_name):
    rc = recommend(movie_name)
    if type(rc)==type('string'):
        err_str = "Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies"
        if rc == err_str:
            st.error(err_str)
            return None
    else:        
        return rc

    return None

def get_suggestions():
    data = pd.read_csv("datasets/MovieRecommendationSystem/main_data.csv")
    lis = data['movie_title'].str.capitalize()
    del data
    return lis

def showMovieDetails(movie_name):
    data_json = searchMovieName(movie_name)
    movie_id = data_json['results'][0]["id"]

    del data_json
    movie_details = getMoveiDetails(movie_id)

    imdb_id = movie_details["imdb_id"]
    poster = 'https://image.tmdb.org/t/p/original{}'.format(movie_details["poster_path"])
    
    col1, col2 = st.beta_columns([1, 2])
    with col1:
        st.image(poster, width=200)

    # genres = movie_details["genres"]

    with col2:        
        title = movie_details["original_title"]
        print_details("TITLE : ", title)

        overview = movie_details["overview"]
        print_details("OVERVIEW : ", overview)

        rating = movie_details["vote_average"]
        rating_count = movie_details["vote_count"] 
        rating = "{}/10 ({} votes)".format(str(rating), str(rating_count))
        print_details("RATING : ", rating)

        genres_list = []
        # st.write(movie_details.keys())
        for gen in movie_details["genres"]:
            genres_list.append(gen["name"])
        print_details("GENERE : ", " ".join(genres_list))
        
        release_date = movie_details["release_date"]
        release_date = pd.to_datetime(release_date, format='%Y-%m-%d').date().strftime("%d-%b-%Y")
        print_details("RELEASE DATE : ", release_date)

        runtime = int(movie_details["runtime"])
        hr = runtime // 60
        mn = runtime % 60
        print_details("RUN TIME : ", "{} hours(s), {} min(s)".format(hr, mn))

        status = movie_details["status"]
        print_details("STATUS : ", status)

    # st.write(movie_details)
    similarity = get_similarity(movie_id, movie_name)
    if not similarity is None:
        show_movie_cast(movie_id)
        show_movie_reviews(imdb_id)
        show_similar_movie_posters(similarity)

def load_details(movie_name):
    '''
    Load the selected movie data
    '''
    if type(movie_name) == str:
        showMovieDetails(movie_name)
    elif type(movie_name) == list:
        for name in movie_name:
            showMovieDetails(name)

def movie_recommendation():
    # selected_movie = st.selectbox("Search Movie", get_suggestions())
    selected_movie = st.multiselect("Search Movie", get_suggestions())

    if selected_movie:
        # load_details(selected_movie)
        load_details(selected_movie)
