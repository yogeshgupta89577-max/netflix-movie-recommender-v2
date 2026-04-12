from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# load data
movies = pickle.load(open('movies.pkl', 'rb'))
import os
import gdown

# download file if not exists
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=1UB_MBxmevvQNrayvi5aBFHEX_L2YsJkY"
    gdown.download(url, "similarity.pkl", quiet=False)

# load file
similarity = pickle.load(open("similarity.pkl", "rb"))


# recommend function (ONLY names)
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []

    # top 10 similar movies
    for i in distances[1:11]:
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names


@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = movies['title'].values
    names = []

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        names = recommend(selected_movie)

    return render_template(
        'index.html',
        movie_list=movie_list,
        names=names
    )


if __name__ == '__main__':
    app.run(debug=True)