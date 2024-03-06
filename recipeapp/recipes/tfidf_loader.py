import os

from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse as sp
import numpy as np
import joblib


class TfidfLoader:
    # WONTFIX it doesn't ensure that it's initialized, it sucks. i'm sorry.
    # use `type: ignore` to suppress the errors
    def __init__(self):
        if os.path.exists("tfidf_vectorizer.joblib"):
            self.tfidf_vectorizer = joblib.load("tfidf_vectorizer.joblib")
        else:
            print("Creating vectorizer...")
            self.tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = None

    def initialize(self):
        if os.path.exists("tfidf_matrix.joblib"):
            print("Existing processed data detected...")
            self.tfidf_matrix = joblib.load("tfidf_matrix.joblib")

        else:
            print("Processing existing data...")
            self.reprocess()

    def reprocess(self):
        from .models import Recipe

        recipes = Recipe.objects.all()
        combined = [recipe.get_combined_text() for recipe in recipes]
        try:
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(combined)
        except ValueError:
            print("No vocab to process")

        self.dump_vectorizer_and_matrix()

    def dump_vectorizer_and_matrix(self):
        joblib.dump(self.tfidf_vectorizer, "tfidf_vectorizer.joblib")
        joblib.dump(self.tfidf_matrix, "tfidf_matrix.joblib")

    # TODO fix
    def add_tfidf_vector_to_matrix(self, tfidf_vector):
        vector_array = tfidf_vector.toarray().flatten()
        new_row = np.array(vector_array).reshape(1, -1)
        self.tfidf_matrix = sp.vstack([self.tfidf_matrix, new_row])
        self.dump_vectorizer_and_matrix()


class TfidfLoaderSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = TfidfLoader()
        return cls._instance
