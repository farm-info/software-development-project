import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

    # WONTFIX lack of type checking
    def initialize(self, model):
        self.model = model
        if os.path.exists("tfidf_matrix.joblib"):
            print("Existing processed data detected...")
            self.tfidf_matrix = joblib.load("tfidf_matrix.joblib")

        else:
            print("Processing all existing data...")
            self.reprocess()

    def check_initialized(self):
        if (self.tfidf_matrix is None) or (self.model is None):
            raise ValueError("TfidfLoader not initialized")

    def dump_data(self):
        self.check_initialized()
        joblib.dump(self.tfidf_vectorizer, "tfidf_vectorizer.joblib")
        joblib.dump(self.tfidf_matrix, "tfidf_matrix.joblib")
        joblib.dump(self.index_to_id, "index_to_id.joblib")

    def reprocess(self):
        all_objects = self.model.objects.all().order_by("id")
        self.index_to_id = [obj.id for obj in all_objects]

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
        tfidf_vector = self.tfidf_vectorizer.transform([query])

        similarities = cosine_similarity(tfidf_vector, self.tfidf_matrix)
        sorted_indices = similarities.argsort()[0][::-1]
        top_n_ids = [self.index_to_id[i] for i in sorted_indices[:n]]
        return self.model.objects.filter(id__in=top_n_ids)


class TfidfLoaderSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = TfidfLoader()
        return cls._instance
