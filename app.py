from flask import Flask, request,render_template
import requests
import pandas as pd
from patsy import dmatrices
import pickle
import bz2file as bz2
def decompress_pickle(file):

    data = bz2.BZ2File(file,'rb')
    data = pickle.load(data)
    return data


movies=pickle.load(open('Model/movie_list.pkl','rb'))
similarity = decompress_pickle('Model/similarity.pbz2')
# similarity=pickle.load(open('Model/similarity.pkl','rb'))


app=Flask(__name__)


def fetch_poster(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?api_key=4ed791de87c58986e35d16098eaf8e5f".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path


def recommend(movie):
    index= movies[movies['title']==movie].index[0]
    distances=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    recommend_movies_name=[]
    recommend_movies_poster=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommend_movies_poster.append(fetch_poster(movie_id))
        recommend_movies_name.append(movies.iloc[i[0]].title)
    return recommend_movies_name,recommend_movies_poster




@app.route('/')
def home():
    return render_template("index.html")

# @app.route('/about')
# def about():
#     return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/recommendation',methods=['GET','POST'])
def recommendation():
    movie_list=movies['title'].values
    status=False
    if request.method=='POST':
        try:
            if request.form:
                movies_name=request.form['movies']
                recommend_movie_name,recommend_movies_poster=recommend(movies_name)
                # print(recommend_movies_poster[0])
                status=True
                return render_template("prediction.html", movie_name=recommend_movie_name,poster=recommend_movies_poster,movie_list=movie_list,status=status)
                
        except Exception as e:
            error={'error':e}
            return render_template("prediction.html",error=error,movie_list=movie_list,status=status)

    return render_template("prediction.html",movie_list=movie_list,status=status)
if __name__ =='__main__':
    app.debug = True
    app.host='0.0.0.0'
    app.port=8080
    app.run()