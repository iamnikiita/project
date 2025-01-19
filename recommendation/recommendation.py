import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommendation:
    """
    A singleton class to provide movie recommendations based on title similarity.

    Attributes:
        movies (pd.DataFrame): DataFrame containing movie data.
        vectorizer (TfidfVectorizer): TF-IDF Vectorizer for text processing.
        tfidf (scipy.sparse.csr_matrix): TF-IDF matrix for movie titles.
    """

    _instance = None  # Singleton instance

    def __new__(cls):
        """
        Create or return the singleton instance of the class.
        """
        if cls._instance is None:
            cls._instance = super(Recommendation, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the Recommendation class by loading the dataset, preprocessing,
        and generating the TF-IDF matrix for movie titles.
        """
        if not hasattr(self, 'movies'):
            # Load the dataset
            self.movies = pd.read_csv("./dataset/movies.csv")

            # Drop unnecessary columns (e.g., 'genres')
            self.movies.drop(columns=['genres'], inplace=True)

            # Initialize TF-IDF Vectorizer with bigram support
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))

            # Fit and transform the movie titles to generate the TF-IDF matrix
            self.tfidf = self.vectorizer.fit_transform(self.movies["title"])

    def search(self, title: str) -> pd.DataFrame:
        """
        Search for movies similar to the given title based on cosine similarity.

        Args:
            title (str): The title of the movie to search for.

        Returns:
            pd.DataFrame: A DataFrame of the top 5 most similar movies.
        """
        # Transform the input title into a TF-IDF vector
        query_vec = self.vectorizer.transform([title])

        # Compute cosine similarity between the input title and all movie titles
        similarity = cosine_similarity(query_vec, self.tfidf).flatten()

        # Get indices of the top 5 most similar movies
        indices = np.argpartition(similarity, -5)[-5:]

        # Retrieve and return the titles sorted by similarity in descending order
        results = self.movies.iloc[indices].iloc[::-1]["title"].tolist()
        return results


def query(title: str) -> list:
    # Creating a Recommendation class
    recommender = Recommendation()

    # Querying the result for the search
    query_result = recommender.search(title)

    # Returning the list
    return query_result
    

if __name__ == "__main__":
    names = query("Toy Story")
    print(names)
