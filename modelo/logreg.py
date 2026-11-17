import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

train_df = pd.read_csv("train.csv")
val_df = pd.read_csv("val.csv")
test_df = pd.read_csv("test.csv")

X_train = train_df["titulo"]
y_train = train_df["label"]

X_val = val_df["titulo"]
y_val = val_df["label"]

X_test = test_df["titulo"]
y_test = test_df["label"]


vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)
X_test_vec = vectorizer.transform(X_test)

logreg_model = LogisticRegression(max_iter=1000)
logreg_model.fit(X_train_vec, y_train)

print("[#] Logistic Regression (Validação)")
y_val_pred = logreg_model.predict(X_val_vec)
print(classification_report(y_val, y_val_pred))

print("[#] Logistic Regression (Teste)")
y_test_pred = logreg_model.predict(X_test_vec)
print(classification_report(y_test, y_test_pred))

probas_logreg = logreg_model.predict_proba(X_test_vec)[:, 1]
polaridades_logreg = 2 * probas_logreg - 1

test_df = X_test.to_frame()
test_df["label"] = y_test.values
test_df["prob_direita"] = probas_logreg
test_df["polaridade"] = polaridades_logreg

print(test_df[["titulo", "label", "prob_direita", "polaridade"]].head())
