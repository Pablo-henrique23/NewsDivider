import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv("test.csv")

X = df["titulo"]
y = df["label"]

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
)

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
