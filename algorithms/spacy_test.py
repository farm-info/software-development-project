# yeah this is so slow, more complex, and it's not like the results are better than tfidf

import pandas as pd
import spacy


nlp = spacy.load("en_core_web_md")

dataset = pd.read_csv("recipe_nlg_lite/test.csv", sep="	")

list_doc = []
for doc in dataset["description"]:
    list_doc.append(nlp(doc))

list_sim = []
for doc in list_doc:
    list_sim.append(list_doc[0].similarity(doc))

print(list_sim[1:])
