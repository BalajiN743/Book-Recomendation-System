import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template,request

popular_df = pickle.load(open('popular_df.pkl', 'rb'))
book_pivot= pickle.load(open('book_pivot.pkl', 'rb'))
books= pickle.load(open('books.pkl', 'rb'))
similarity_score= pickle.load(open('similarity_scores.pkl', 'rb'))


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Title'].values),
                           author=list(popular_df['Author'].values),
                           image=list(popular_df['Image_URL_M'].values),
                           votes=list(popular_df['Total_No_Of_Users_Rated'].values),
                           rating=list(popular_df['Avg_Rating'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input=request.form.get('user_input')
    similarity_scores = cosine_similarity(book_pivot)
    index = np.where(book_pivot.index==user_input)[0][0]
    similar_items=sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:11]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Title'] == book_pivot.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Title')['Title'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['Author'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['Image_URL_M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)



if __name__ == '__main__':
    app.run(debug=True)



