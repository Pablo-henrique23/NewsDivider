import pandas as pd
from sklearn.model_selection import train_test_split

# Definição dos rótulos
rotulos = {
    "jovempan": 1,
    "oantagonista": 1,
    "dcm": -1
}

# Caminhos dos CSVs
caminhos = {
    "jovempan": "dataset/jovempan.csv",
    "oantagonista": "dataset/antagonista.csv",
    "dcm": "dataset/diariocentrodomundo.csv"
}

# Lista para armazenar todos os DataFrames
dfs = []

for fonte, caminho in caminhos.items():
    df = pd.read_csv(caminho)
    
    # Adiciona rótulo baseado na fonte
    df["label"] = rotulos[fonte]
    
    # Mantém só as colunas importantes
    df = df[["id", "titulo", "corpo", "label"]]
    
    dfs.append(df)

# Junta tudo em um único dataset
dataset = pd.concat(dfs, ignore_index=True)

# Remove linhas sem corpo
dataset = dataset.dropna(subset=["corpo"])

# Split treino/teste (estratificado pelo label)
train_df, test_df = train_test_split(
    dataset,
    test_size=0.2,
    random_state=42,
    stratify=dataset["label"]
)

print("Tamanho treino:", len(train_df))
print("Tamanho teste:", len(test_df))
print(dataset["label"].value_counts())

# Salvar já rotulado
dataset.to_csv("dataset_rotulado.csv", index=False)
train_df.to_csv("train.csv", index=False)
test_df.to_csv("test.csv", index=False)

