import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
#import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import faiss

#nltk.download('stopwords')
#nltk.download('punkt')

netflix_df = pd.read_csv('netflix_titles.csv')

netflix_df = netflix_df.fillna('')

netflix_df['combined'] = netflix_df['title'] + ' ' + netflix_df['description']

stop_words = set(stopwords.words('english'))
netflix_df['combined'] = netflix_df['combined'].apply(
    lambda x: ' '.join([word.lower()
    for word in word_tokenize(x)
    if word.lower() not in stop_words])
)

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(netflix_df['combined']).toarray().astype('float32')

index = faiss.IndexIDMap(faiss.IndexFlatIP(tfidf_matrix.shape[1]))
faiss.normalize_L2(tfidf_matrix)
index.add_with_ids(tfidf_matrix, np.arange(tfidf_matrix.shape[0]))


def get_recommendations(idx, k=5):
    faiss.normalize_L2(idx)
    top_k = index.search(idx, k)

    return netflix_df.loc[top_k[1][0], ["title"]]


input_vec = (tfidf_matrix[392] + (((tfidf_matrix[393] + tfidf_matrix[1359]*0.5)/1.5)*0.5))/1.5
print(get_recommendations(input_vec.reshape(1, -1)))

#faiss.write_index(index, "index.index")
#faiss.read_index("index.index")
