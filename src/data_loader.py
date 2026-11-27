import pandas as pd

def data_loader(path):

    character_set = pd.read_csv((path + "Charater_Set.csv"))
    characters = pd.read_csv((path + "Characters.csv"), sep=";") # principale
    return character_set,characters

# controlla i nomi esatti delle colonne
# print(character_set.columns.tolist())
# print(characters.columns.tolist())


