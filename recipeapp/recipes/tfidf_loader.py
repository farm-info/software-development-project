import os

from django.db import models
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib


class TfidfLoader:
    tfidf_matrix: scipy.sparse.csr_matrix | None = None
    model: models.Model | None = None

    def __init__(self):
        if os.path.exists("tfidf_vectorizer.joblib"):
            self.tfidf_vectorizer = joblib.load("tfidf_vectorizer.joblib")
        else:
            print("Creating vectorizer...")
            self.tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = None

    def initialize(self, model):
        self.model = model
        if os.path.exists("tfidf_matrix.joblib"):
            print("Existing processed data detected...")
            self.tfidf_matrix = joblib.load("tfidf_matrix.joblib")
            self.index_to_id = joblib.load("index_to_id.joblib")

        else:
            # TODO only reprocess when it's startserver
            print("Processing all existing data...")
            self.reprocess()

    # TODO pylance isn't goated enough :(
    def check_initialized(self):
        if (self.tfidf_matrix is None) or (self.model is None):
            raise ValueError("TfidfLoader not initialized")

    def dump_data(self):
        self.check_initialized()
        joblib.dump(self.tfidf_vectorizer, "tfidf_vectorizer.joblib")
        joblib.dump(self.tfidf_matrix, "tfidf_matrix.joblib")
        joblib.dump(self.index_to_id, "index_to_id.joblib")

    def add_item(self, text, id):
        self.check_initialized()
        text_matrix = self.tfidf_vectorizer.transform([text])
        # TODO test
        self.tfidf_matrix = scipy.sparse.vstack([self.tfidf_matrix, text_matrix])
        self.index_to_id.append(id)
        self.dump_data()

    def update_item(self, text, id):
        self.check_initialized()
        text_matrix = self.tfidf_vectorizer.transform([text])
        index = self.index_to_id.index(id)
        self.tfidf_matrix[index] = text_matrix  # type: ignore

    def reprocess(self):
        all_objects = self.model.objects.all().order_by("id")  # type: ignore
        self.index_to_id = [obj.pk for obj in all_objects]

        try:
            combined = [object.get_combined_text() for object in all_objects]  # type: ignore
        except AttributeError:
            raise ValueError("Model does not have get_combined_text method")

        try:
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(combined)
        except ValueError:
            print("No vocab to process")

        self.dump_data()

    def search_item(self, query: str, n: int = 10):
        self.check_initialized()
        tfidf_vector = self.tfidf_vectorizer.transform([query])

        similarities = cosine_similarity(tfidf_vector, self.tfidf_matrix)
        sorted_indices = similarities.argsort()[0][::-1]
        top_n_ids = [self.index_to_id[i] for i in sorted_indices[:n]]
        return self.model.objects.filter(id__in=top_n_ids)  # type: ignore


class TfidfLoaderSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = TfidfLoader()
        return cls._instance
