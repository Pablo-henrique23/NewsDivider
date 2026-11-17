import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from lime.lime_text import LimeTextExplainer
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords
stopwords_pt = stopwords.words("portuguese")

train_df = pd.read_csv("train.csv")
val_df = pd.read_csv("val.csv")
test_df = pd.read_csv("test.csv")

X_train = train_df["titulo"]
y_train = train_df["label"]

X_val = val_df["titulo"]
y_val = val_df["label"]

X_test = test_df["titulo"]
y_test = test_df["label"]

vectorizer = TfidfVectorizer(max_features=5000, stop_words=stopwords_pt)
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)
X_test_vec = vectorizer.transform(X_test)

nb_model = MultinomialNB()
nb_model.fit(X_train_vec, y_train)

y_val_pred = nb_model.predict(X_val_vec)
y_test_pred = nb_model.predict(X_test_vec)

print("[#] Validação Naive Bayes ")
print(classification_report(y_val, y_val_pred))
print("[#] Teste Naive Bayes ")
print(classification_report(y_test, y_test_pred))

probas_test = nb_model.predict_proba(X_test_vec)[:,1]
polaridades_test = 2 * probas_test - 1

test_df = pd.DataFrame({
    "titulo": X_test,
    "label": y_test,
    "prob_direita": probas_test,
    "polaridade": polaridades_test,
    "y_pred": y_test_pred
})

pd.set_option("display.max_colwidth", None)
print(test_df.head())

explainer = LimeTextExplainer(class_names=["esquerda","direita"])
i = 0
predict_fn = lambda x: nb_model.predict_proba(vectorizer.transform(x))
exp = explainer.explain_instance(X_test.iloc[i], predict_fn, num_features=10)

print("LIME Naive Bayes:")
for c in exp.as_list():
    print(f'{c[0]:<20} = {c[1]}')
