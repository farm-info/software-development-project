from textwrap import dedent
import warnings
import tfidf


# change this to switch between search and recommendation mode
search_mode = False
warnings.filterwarnings("ignore")


# put your datasets in /algorithms/datasets/ so that git will ignore them
print("Loading dataset... ", end="")
dataset = tfidf.load_dataset("algorithms/datasets/recipe_nlg_lite/train.csv", "	")
print("done")

print("Processing dataset... ", end="")
similarity, indices = tfidf.process_data(dataset, use_alt_stopwords=True)
print("done")


print(
    dedent(
        """
        Please Enter the uid of the recipe you want to find similar recipes for.
        Enter 'exit' to exit the program.
        Enter 'switch' to switch between search or recommendation mode.
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
