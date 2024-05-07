import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import faiss
import logging

logging.basicConfig(level=logging.INFO)
nltk.download('stopwords')
nltk.download('punkt')

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data.
    """
    return pd.read_csv(filepath)

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess text data by removing stopwords and combining title and description.

    Args:
        df (pd.DataFrame): The DataFrame containing the movie data.

    Returns:
        pd.DataFrame: The DataFrame with processed text data.
    """
    df = df.fillna('')
    df['combined'] = df['title'] + ' ' + df['description']
    stop_words = set(stopwords.words('english'))
    df['combined'] = df['combined'].apply(
        lambda x: ' '.join([word.lower() for word in word_tokenize(x) if word.lower() not in stop_words])
    )
    return df

def create_tfidf_matrix(df: pd.DataFrame) -> np.ndarray:
    """
    Create a TF-IDF matrix from the preprocessed text data.

    Args:
        df (pd.DataFrame): The preprocessed DataFrame.

    Returns:
        np.ndarray: The TF-IDF matrix.
    """
    tfidf = TfidfVectorizer()
    return tfidf.fit_transform(df['combined']).toarray().astype('float32')

def create_faiss_index(tfidf_matrix: np.ndarray) -> faiss.Index:
    """
    Create a FAISS index from the TF-IDF matrix.

    Args:
        tfidf_matrix (np.ndarray): The TF-IDF matrix.

    Returns:
        faiss.Index: The FAISS index.
    """
    index = faiss.IndexIDMap(faiss.IndexFlatIP(tfidf_matrix.shape[1]))
    faiss.normalize_L2(tfidf_matrix)
    index.add_with_ids(tfidf_matrix, np.arange(tfidf_matrix.shape[0]))
    return index
