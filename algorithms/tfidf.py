import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity


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
    if remove_numbers:
        preprocessor = lambda tokens: re.sub("(\\d)+", "NUM", tokens.lower())
    else:
        preprocessor = None

    if use_alt_stopwords:
        with open("algorithms/stopwords.txt", "r", encoding="utf-8") as file:
            stop_words = file.read().splitlines()
    else:
        stop_words = "english"

    # vectorize
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
    try:
        idx = indices[uid]
    except KeyError as e:
        raise ValueError("Invalid uid") from e
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_similar = sim_scores[1 : num_recommend + 1]
    recipe_indices = [i[0] for i in top_similar]
    return dataset.loc[recipe_indices]
