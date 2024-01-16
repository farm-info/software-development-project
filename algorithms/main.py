from textwrap import dedent
import warnings
import tfidf


warnings.filterwarnings("ignore")


print("Loading dataset... ", end="")
# put your datasets in /algorithms/datasets/ so that git will ignore them
dataset = tfidf.load_dataset("algorithms/datasets/recipe_nlg_lite/train.csv", "	")
print("done")
print("Processing dataset... ", end="")
similarity, indices = tfidf.process_data(dataset, use_alt_stopwords=True)
print("done")


print(
    dedent(
        """
        Please Enter the uid of the recipe you want to find similar recipes for.
        You can also view the current recommendations by opening the csv file.
        Enter 'exit' to exit the program"""
    )
)

while True:
    query = input("\nEnter uid: ")
    if query == "exit":
        break

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
