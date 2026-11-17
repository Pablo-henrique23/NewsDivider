import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords


nltk.download("stopwords")

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

print("Tamanho treino:", len(X_train))
print("Tamanho validação:", len(X_val))
print("Tamanho teste:", len(X_test))

vectorizer = TfidfVectorizer(stop_words=stopwords_pt, max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)
X_test_tfidf = vectorizer.transform(X_test)

nb_model = MultinomialNB()
nb_model.fit(X_train_tfidf, y_train)

print("\n=== Avaliação no conjunto de VALIDAÇÃO ===")
y_val_pred = nb_model.predict(X_val_tfidf)
print(classification_report(y_val, y_val_pred))

print("\n=== Avaliação no conjunto de TESTE ===")
y_test_pred = nb_model.predict(X_test_tfidf)
print(classification_report(y_test, y_test_pred))

probas_test = nb_model.predict_proba(X_test_tfidf)[:, 1]  # prob de ser direita
polaridades_test = 2 * probas_test - 1

test_df = pd.DataFrame({
    "titulo": X_test,
    "label": y_test,
    "prob_direita": probas_test,
    "polaridade": polaridades_test
})

pd.set_option("display.max_colwidth", None)  # mostrar títulos inteiros
print(test_df.head())
