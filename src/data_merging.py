import pandas as pd

def data_merging(character_set,characters):
    # normalizza i nomi per il join
    character_set["chiave"] = character_set["Name"].str.strip().str.lower()
    characters["chiave"] = characters["Name"].str.strip().str.lower()
    # unisce i dataset
    data = characters.merge(
      character_set[["chiave", "Notable Traits", "Role"]],
      on="chiave",
      how="left",          # tiene tutte le righe di characters
    ).drop(columns=["chiave"])

    return data

