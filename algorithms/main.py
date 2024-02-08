import os
from textwrap import dedent
import warnings
import tfidf
from joblib import dump, load


# change this to switch between search and recommendation mode
search_mode = True
warnings.filterwarnings("ignore")


if (
    os.path.exists("algorithms/results/similarity.joblib")
    and os.path.exists("algorithms/results/indices.joblib")
    and os.path.exists("algorithms/results/dataset.joblib")
):
    print("Processed data already exists.")
    dataset = load("algorithms/results/dataset.joblib")
    similarity = load("algorithms/results/similarity.joblib")
    indices = load("algorithms/results/indices.joblib")

else:
    print("First time setup since processed data isn't found.")
    # put your datasets in /algorithms/datasets/ so that git will ignore them
    print("Loading dataset... ", end="")
    dataset = tfidf.load_dataset("algorithms/datasets/recipe_nlg_lite/train.csv", "	")
    print("done")

    print("Processing dataset... ", end="")
    similarity, indices = tfidf.process_data(dataset, use_alt_stopwords=True)
    print("done")

    print("Saving processed data... ", end="")
    dump(dataset, "algorithms/results/dataset.joblib")
    dump(similarity, "algorithms/results/similarity.joblib")
    dump(indices, "algorithms/results/indices.joblib")
    print("done")


print(
    dedent(
        """
        Please Enter the uid of the recipe you want to find similar recipes for.
        Enter 'exit' to exit the program.
        You can also view the current recommendations by opening the csv file.
        """
    )
)


while True:
    query = input("\nEnter query: ")

    if query == "exit":
        break

    if search_mode:
        try:
            recommendations = tfidf.search_recipes(query, dataset, similarity)
        except ValueError:
            print("Invalid uid")
            continue

        recommendations.style.hide(axis='index')
        print(
            f"Search results for {query}"
        )

    else:
        try:
            recommendations = tfidf.get_recommendations(query, dataset, similarity, indices)
        except ValueError:
            print("Invalid uid")
            continue

        recommendations.style.hide(axis='index')
        print(
            f"Recommendations for {dataset.loc[dataset["uid"] == query]["name"].values[0]}"
        )

    print(f"{recommendations[["name","description", "uid"]]}")
    print("----------------------------------")
    recommendations.to_csv("algorithms/results/current.csv")
