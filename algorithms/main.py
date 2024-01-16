import tfidf


# put your datasets in /algorithms/datasets/ so that git will ignore them
dataset = tfidf.load_dataset("algorithms/datasets/recipe_nlg_lite/train.csv", "	")
similarity, indices = tfidf.process_data(dataset)


a = tfidf.get_recommendations(
    "dab8b7d0-e0f6-4bb0-aed9-346e80dace1f",
    dataset,
    similarity,
    indices,
    num_recommend=30,
)

a.to_csv("algorithms/results/combined_cosine_altstopword.csv")
