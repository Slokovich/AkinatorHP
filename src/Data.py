import pandas as pd

character_set = pd.read_csv("../Data/Charater_Set.csv")
characters = pd.read_csv("../Data/Characters.csv", sep=";") # principale

# controlla i nomi esatti delle colonne
# print(character_set.columns.tolist())
# print(characters.columns.tolist())

# normalizza i nomi per il join
character_set["chiave"] = character_set["Name"].str.strip().str.lower()
characters["chiave"] = characters["Name"].str.strip().str.lower()

data = characters.merge(
    character_set[["chiave", "Notable Traits", "Role"]],
    on="chiave",
    how="left",          # tiene tutte le righe di characters
).drop(columns=["chiave"])

# pulizia STRIP di ogni colonna
for column in data.select_dtypes(include="object").columns:
    data[column] = data[column].str.replace("\xa0", " ").str.strip()

# pulizia [ di ogni colonna
for column in data.select_dtypes(include="object").columns:
    data[column] = data[column].str.replace("[","",regex=False)


# Pulizia blood status
col = data["Blood status"]
col = col.str.replace("\xa0", " ").str.strip()   # spazi strani via
col = col.replace(r"(?i).*pure-blood or half-blood.*", "Unknown", regex=True)
data["Blood status"] = col.fillna("Unknown")

print(data["Blood status"].str.findall(r"[^A-Za-z0-9\s]").explode().value_counts())


# DEBUG

# print(data.columns.tolist())

# print(data["Blood status"].value_counts().to_string())
# print(data["Species"].value_counts().to_string())

# print(data[["Name", "Species", "Blood status"]].to_string(index=False))
# print(data.to_string(index=False))

for column in data.columns:
    print(data[column].value_counts().to_string())

# print(data.columns)
# print(data.head())
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)

