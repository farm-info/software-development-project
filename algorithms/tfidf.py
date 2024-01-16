import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity


def remove_number_preprocessor(tokens):
    r = re.sub("(\\d)+", "NUM", tokens.lower())
    # This alternative just removes numbers:
    # r = re.sub('(\d)+', '', tokens.lower())
    return r


# load dataset
def load_dataset(dataset_path, sep):
    dataset = pd.read_csv(dataset_path, sep=sep)
    dataset["combined"] = dataset.apply(
        lambda row: " ".join(row[["name", "description", "ner", "steps"]]), axis=1
    )
    return dataset


def process_data(
    dataset: pd.DataFrame,
    remove_numbers: bool = False,
    use_alt_stopwords: bool = False,
    similarity_function: str = "cosine",
):
    # vectorize
    if remove_numbers:
        preprocessor = remove_number_preprocessor
    else:
        preprocessor = None

    if use_alt_stopwords:
        with open("stopwords.txt", "r", encoding="utf-8") as file:
            stop_words = file.read().splitlines()
    else:
        stop_words = "english"

    tfidf_desc = TfidfVectorizer(stop_words=stop_words, preprocessor=preprocessor)
    tfidf_desc_matrix = tfidf_desc.fit_transform(dataset["combined"])

    # calculate similarity
    if similarity_function == "cosine":
        similarity = linear_kernel(tfidf_desc_matrix, tfidf_desc_matrix)
    elif similarity_function == "linear":
        similarity = cosine_similarity(tfidf_desc_matrix, tfidf_desc_matrix)
    else:
        raise ValueError("similarity_function must be 'cosine' or 'linear'")

    # map to original dataset
    indices = pd.Series(dataset.index, index=dataset["uid"]).drop_duplicates()

    return similarity, indices


def get_recommendations(uid, dataset, similarity, indices, num_recommend=10):
    idx = indices[uid]
    sim_scores = list(
        enumerate(similarity[idx])
    )  # Sort the movies based on the similarity scores
    sim_scores = sorted(
        sim_scores, key=lambda x: x[1], reverse=True
    )  # Get the scores of the 10 most similar movies
    top_similar = sim_scores[1 : num_recommend + 1]  # Get the movie indices
    recipe_indices = [i[0] for i in top_similar]
    return dataset.loc[recipe_indices]
