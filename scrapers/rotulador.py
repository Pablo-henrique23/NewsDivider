import pandas as pd
from sklearn.model_selection import train_test_split

rotulos = {
    "jovempan": 1,
    "oantagonista": 1,
    "dcm": -1,
    "cartacapital": -1
}

caminhos = {
    "jovempan": "dataset/jovempan.csv",
    "oantagonista": "dataset/antagonista.csv",
    "dcm": "dataset/diariocentrodomundo.csv",
    "cartacapital": "dataset/cartacapital.csv"
}

dfs = []

for fonte, caminho in caminhos.items():
    df = pd.read_csv(caminho)
    df["label"] = rotulos[fonte]
    df = df[["id", "titulo", "corpo", "label"]]

    dfs.append(df)

dataset = pd.concat(dfs, ignore_index=True)

dataset = dataset.dropna(subset=["corpo"])

train_val_df, test_df = train_test_split(
    dataset,
    test_size=0.15,
    random_state=42,
    stratify=dataset["label"]
)

train_df, val_df = train_test_split(
    train_val_df,
    test_size=0.1765,
    random_state=42,
    stratify=train_val_df["label"]
)

print("Tamanho treino:", len(train_df))
print("Tamanho validação:", len(val_df))
print("Tamanho teste:", len(test_df))
print(dataset["label"].value_counts())

dataset.to_csv("dataset_rotulado.csv", index=False)
train_df.to_csv("train.csv", index=False)
val_df.to_csv("val.csv", index=False)
test_df.to_csv("test.csv", index=False)

