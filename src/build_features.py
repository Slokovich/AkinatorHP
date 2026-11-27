import pandas as pd
import questions


def build_features(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
  data = data.dropna(subset=["Name"]).drop_duplicates(subset=["Name"]).reset_index(drop=True)
  y = data["Name"]

  X = pd.DataFrame(index=data.index)

  # Genere
  X["is_male"] = (data["Gender"].fillna("").str.strip().str.lower() == "male").astype(int)

  # Patronus -- cluster
  patronus = data["Patronus"].fillna("").str.lower().str.strip()
  invalid_patronus = patronus.isin(["", "unknown", "nan", "none", "non-corporeal"])
  X["has_corporeal_patronus"] = (~invalid_patronus).astype(int)
  X["patronus_canine_feline"] = patronus.str.contains(
     r"dog|terrier|wolf|fox|cat|lynx|leopard", regex=True
  ).astype(int)
  X["patronus_deer_horse"] = patronus.str.contains(
     r"\bstag\b|\bdoe\b|horse", regex=True
  ).astype(int)
  X["patronus_bird"] = patronus.str.contains(
     r"phoenix|swan|owl|eagle|raven|heron|peacock|magpie|falcon", regex=True
  ).astype(int)

  # Capelli -- cluster
  hair = data["Hair colour"].fillna("").str.lower().str.strip()
  X["hair_red"] = hair.str.contains(r"red|auburn|ginger", regex=True).astype(int)
  X["hair_black"] = hair.str.contains(r"black", regex=True).astype(int)
  X["hair_blond"] = hair.str.contains(r"blond", regex=True).astype(int)
  X["hair_brown"] = hair.str.contains(r"brown|mousy", regex=True).astype(int)
  X["hair_grey_white"] = hair.str.contains(r"grey|gray|silver|white", regex=True).astype(int)

  # Occhi -- cluster
  eyes = data["Eye colour"].fillna("").str.lower().str.strip()
  X["eyes_blue"] = eyes.str.contains(r"blue", regex=True).astype(int)
  X["eyes_green"] = eyes.str.contains(r"green", regex=True).astype(int)
  X["eyes_brown_dark"] = eyes.str.contains(r"brown|dark|black|hazel", regex=True).astype(int)

  # Bacchette
  wand = data["Wand"].fillna("").str.lower().str.strip()
  invalid_wand = wand.isin(["", "unknown", "nan", "none"])
  X["has_known_wand"] = (~invalid_wand).astype(int)
  X["wand_core_phoenix_thestral"] = wand.str.contains(
     r"phoenix|thestral", regex=True
  ).astype(int)
  X["wand_core_unicorn_dragon"] = wand.str.contains(
     r"unicorn|dragon", regex=True
  ).astype(int)
  X["wand_wood_classic_light"] = wand.str.contains(
     r"\bholly\b|\bash\b|\bcherry\b|\bwillow\b|\balder\b|\bhornbeam\b", regex=True
  ).astype(int)
  X["wand_wood_dark_strong"] = wand.str.contains(
     r"\belder\b|\boak\b|\bmahogany\b|\bcypress\b|\bchestnut\b|\bfir\b|\bvine\b", regex=True
  ).astype(int)

  # Casa di Hogwarts
  house = data["House"].fillna("").str.strip().str.lower()
  for h in ["gryffindor", "slytherin", "ravenclaw", "hufflepuff"]:
     X[f"house_{h}"] = (house == h).astype(int)

  # Stato di sangue
  blood = data["Blood status"].fillna("unknown").str.strip().str.lower()
  is_ambiguous = (
  (blood.str.contains("pure-blood", regex=False) & blood.str.contains("half-blood", regex=False))
          | blood.isin(["unknown", "nan", "none", ""])
  )
  X["blood_pure"] = (~is_ambiguous & blood.str.contains("pure-blood", regex=False)).astype(int)
  X["blood_half"] = (~is_ambiguous & blood.str.contains("half-blood", regex=False)).astype(int)
  X["blood_muggle"] = (~is_ambiguous & blood.str.contains("muggle-born", regex=False)).astype(int)
  X["blood_ambiguous"] = is_ambiguous.astype(int)

  # Skills
  skills = data["Skills"].fillna("").str.lower()
  X["plays_quidditch"] = skills.str.contains(
     r"quidditch|seeker|chaser|beater|keeper", regex=True
  ).astype(int)
  X["is_animagus"] = skills.str.contains(
     r"animagus", regex=True
  ).astype(int)
  X["skill_dark_arts_duel"] = skills.str.contains(
     r"defence against the dark arts|duel|curse", regex=True
  ).astype(int)
  X["skill_charms_transfig"] = skills.str.contains(
     r"charms|transfiguration|nonverbal|healing|household", regex=True
  ).astype(int)
  X["skill_divination"] = skills.str.contains(
     r"divination", regex=True
  ).astype(int)
  X["skill_herbology_potions"] = skills.str.contains(
     r"herbology|potions", regex=True
  ).astype(int)

  # Vivo o morto (Death == NaN -> vivo)
  death_str = data["Death"].astype("string").str.strip().str.lower()
  is_dead = death_str.notna() & (death_str != "") & (death_str != "nan")
  X["is_alive"] = (~is_dead).astype(int)

  # Affiliazioni principali (da Loyalty)
  loyalty = data["Loyalty"].fillna("").str.lower()
  X["in_dumbledores_army"] = loyalty.str.contains("dumbledore's army", regex=False).astype(int)
  X["in_order_of_phoenix"] = loyalty.str.contains("order of the phoenix", regex=False).astype(int)
  X["is_death_eater"] = loyalty.str.contains("death eaters", regex=False).astype(int)

  # Studente vs Adulto/Professore (da Job)
  job = data["Job"].fillna("").str.lower()
  X["is_student"] = job.str.contains("student", regex=False).astype(int)
  # print(X.to_string())
  return X, y
