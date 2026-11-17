import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import shap
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

vectorizer = TfidfVectorizer(stop_words=stopwords_pt, max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)
X_test_vec = vectorizer.transform(X_test)

logreg_model = LogisticRegression(max_iter=1000)
logreg_model.fit(X_train_vec, y_train)

y_val_pred = logreg_model.predict(X_val_vec)
y_test_pred = logreg_model.predict(X_test_vec)

print("=== Validação Logistic Regression ===")
print(classification_report(y_val, y_val_pred))
print("=== Teste Logistic Regression ===")
print(classification_report(y_test, y_test_pred))

probas_test = logreg_model.predict_proba(X_test_vec)[:,1]
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

explainer = shap.Explainer(logreg_model, X_train_vec, feature_names=vectorizer.get_feature_names_out())
idx = 0
shap_values = explainer(X_test_vec[idx])

shap.initjs()
shap.plots.bar(shap_values)  # gráfico de barras mostrando os termos mais importantes
# shap.plots.waterfall(shap_values)  # alternativa detalhada por feature

explainer_lime = LimeTextExplainer(class_names=["esquerda","direita"])
predict_fn = lambda x: logreg_model.predict_proba(vectorizer.transform(x))
i = 0
exp = explainer_lime.explain_instance(X_test.iloc[i], predict_fn, num_features=10)
print("LIME Logistic Regression:")
for c in exp.as_list():
    print(f'{c[0]:<20} = {c[1]}')

