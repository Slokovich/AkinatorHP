import pandas as pd

def data_cleaning(data):
    clean_strip(data)
    clean_char_special(data)
    NaN_to_Unknown(data)
    #clean_blood_status_column(data)
    clean_loyalty_columns(data)
    # print(data[["Name","Blood status"]].to_string())
    return data


# pulizia STRIP di ogni colonna
def clean_strip(data):
    for column in data.select_dtypes(include="object").columns:
      data[column] = data[column].str.replace("\xa0", " ").str.strip()

# pulizia [ di ogni colonna
def clean_char_special(data):
    for column in data.select_dtypes(include="object").columns:
      data[column] = data[column].str.replace("[","",regex=False)

# Unknown al posto di NaN
def NaN_to_Unknown(data):
    for column in data.select_dtypes(include="object").columns:
        data[column] = data[column].fillna("Unknown")

'''
# Pulizia blood status
def clean_blood_status_column(data):
    col = data["Blood status"]
    col = col.str.replace("\xa0", " ").str.strip()   # spazi strani via
    col = col.replace(r"(?i).*pure-blood or half-blood.*", "Unknown", regex=True)
'''

# Rimuove 'Order of the Phoenix' da LOYALTY se il personaggio è uno studente
def clean_loyalty_columns(data):
    is_student_mask = data["Job"].fillna("").str.lower().str.contains("student", regex=False)
    loyalty_clean = data["Loyalty"].fillna("")
    data["Loyalty"] = loyalty_clean.where(
       ~is_student_mask,
       loyalty_clean.str.replace("Order of the Phoenix", "", case=False, regex=False),
    )


# print(data.to_string())
#print(data["Blood status"].str.findall(r"[^A-Za-z0-9\s]").explode().value_counts())


# print(data.to_string(index=False))

# for column in data.columns:
#    print(data[column].value_counts().to_string())

# print(data.columns)
# print(data.head())
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
