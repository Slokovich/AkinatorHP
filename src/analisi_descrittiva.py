import matplotlib.pyplot as plt
import pandas as pd


def analisi_descrittiva(data):

    df_eda = data.dropna(subset=["Name"]).drop_duplicates(subset=["Name"]).reset_index(drop=True)


    missing_tokens = {"", "nan", "none", "null", "unknown", "n/a", "-", "nd", "n.d."}

    # Base pulita senza duplicati sul nome
    df_eda = data.dropna(subset=["Name"]).drop_duplicates(subset=["Name"]).reset_index(drop=True)

    # -------------  ANALISI DESCRITTIVA CASATE --------------


    casata_raw = df_eda["House"].astype("string").str.strip()
    missing_tokens = {"", "nan", "none", "null", "unknown", "n/a", "-", "nd", "n.d."}




    is_missing = casata_raw.isna() | casata_raw.str.lower().isin(missing_tokens)
    mappa_casate = {
       "Gryffindor": "Grifondoro",
       "Slytherin": "Serpeverde",
       "Ravenclaw": "Corvonero",
       "Hufflepuff": "Tassorosso",
    }


    # Tutto ciò che non è una delle 4 casate (inclusi Beauxbatons, Durmstrang) va in "Altro" (Nan e Unknwon va in "Non specificato")
    casata_cluster = casata_raw.map(mappa_casate)
    casata_cluster = casata_cluster.where(is_missing | casata_cluster.notna(), "Altro")
    casata_cluster = casata_cluster.fillna("Non specificato")




    # Ordine leggibile per stampe e grafici
    ordine_casate = ["Grifondoro", "Serpeverde", "Corvonero", "Tassorosso", "Non specificato","Altro"]
    # Se ci fossero etichette extra non previste, le aggiungiamo in coda per sicurezza
    extra_casate = [c for c in casata_cluster.unique() if c not in ordine_casate]
    ordine_finale = ordine_casate + extra_casate


    # 3. Conteggi assoluti e percentuali
    conteggi_casate = (
       casata_cluster.value_counts()
       .reindex(ordine_finale, fill_value=0)
    )
    percentuali_casate = (conteggi_casate / conteggi_casate.sum() * 100).round(1)


    tab_casate = pd.DataFrame({
       "Personaggi": conteggi_casate,
       "%": percentuali_casate,
    })




    ## ----------------- ANALISI SESSO ---------------------------------
    sesso = (
       df_eda["Gender"]
       .fillna("Non specificato")
       .str.strip()
       .replace({"Male": "M",
                 "Female": "F",
                 "Unknown": "Non specificato",
                 "": "Non specificato"})
    )


    tab_sesso = pd.DataFrame({
       "Conteggio": sesso.value_counts(),
       "%": (sesso.value_counts(normalize=True) * 100).round(1),
    })


    # print("=== SESSO ===\n", tab_sesso)




    ## ----------------- ANALISI STATO DI SANGUE -----------------------
    sangue = df_eda["Blood status"].fillna("Non specificato").str.strip()
    sangue = sangue.replace({
       "Pure-blood": "Purosangue",
       "Half-blood": "Mezzosangue",
       "Muggle-born": "Nato Babbano",
       "Muggle": "Babbano",
       "Unknown": "Non specificato",
       "": "Non specificato",
       "Pure-blood or half-blood": "Non specificato",
       "Pure-blood or Half-blood" : "Non specificato",
    })
    # Tutto ciò che non è tra i 3 gruppi principali o "Non specificato" va in "Altro"
    principali = ["Purosangue", "Mezzosangue", "Nato Babbano", "Non specificato",'Babbano']
    sangue = sangue.where(sangue.isin(principali), "Altro")


    tab_sangue = pd.DataFrame({
       "Conteggio": sangue.value_counts(),
       "%": (sangue.value_counts(normalize=True) * 100).round(1),
    })


    # print("\n=== STATO DI SANGUE ===\n", tab_sangue)


    ## --------- GRAFICI ---------------------


    ## ---- analisi univariata -------
    print("=== SESSO ===\n", tab_sesso)
    print("\n=== STATO DI SANGUE ===\n", tab_sangue)
    print("\n=== CASATE ===\n", tab_casate)


    palette_casate = {
       "Grifondoro": "#AE0001",
       "Serpeverde": "#1A472A",
       "Corvonero": "#0E1A40",
       "Tassorosso": "#ECB939",
       "Altro": "#6B7280",
       "Non specificato": "#9CA3AF",
    }
    colori_casate = [palette_casate.get(nome, "#4F46E5") for nome in tab_casate.index]




    fig1, axes = plt.subplots(2, 3, figsize=(12, 4))
    tab_sesso["%"].plot(kind="bar", ax=axes[0,0], color=["#2563EB", "#DB2777", "#9CA3AF"], rot=0)
    axes[0,0].set_title("Sesso (M / F)")
    axes[0,0].set_ylabel("Personaggi (%)")
    tab_sangue["%"].plot(kind="bar", ax=axes[0,1], color="#0284C7", rot=20)
    axes[0,1].set_title("Stato di sangue")
    axes[0,1].set_ylabel("Personaggi (%)")
    tab_casate["%"].plot(kind="bar", ax=axes[0,2], color=colori_casate, rot=25)
    axes[0,2].set_ylabel("Personaggi (%)")
    axes[0,2].set_title("Casate")


    ## ------ analisi bivariata ---------
    ## ----------------- ANALISI COMBINATA (GROUPBY) -----------------
    df_comb = pd.DataFrame({
       "Name": df_eda["Name"],
       "Casata": casata_cluster,
       "Sesso": sesso,
       "Sangue": sangue,
    })


    # 1. Casata x Stato di sangue (conteggi e % per Casata)
    casata_sangue_cnt = (
       df_comb.groupby(["Casata", "Sangue"], observed=False)["Name"]
       .count()
       .unstack(fill_value=0)
    )
    casata_sangue_pct = (
       casata_sangue_cnt.div(casata_sangue_cnt.sum(axis=1), axis=0) * 100
    ).round(1)


    # 2. Casata x Sesso (conteggi e % per Casata)
    casata_sesso_cnt = (
       df_comb.groupby(["Casata", "Sesso"], observed=False)["Name"]
       .count()
       .unstack(fill_value=0)
    )
    casata_sesso_pct = (
       casata_sesso_cnt.div(casata_sesso_cnt.sum(axis=1), axis=0) * 100
    ).round(1)


    # 3. Stato di sangue x Sesso (conteggi e % per Stato di sangue)
    sangue_sesso_cnt = (
       df_comb.groupby(["Sangue", "Sesso"], observed=False)["Name"]
       .count()
       .unstack(fill_value=0)
    )
    sangue_sesso_pct = (
       sangue_sesso_cnt.div(sangue_sesso_cnt.sum(axis=1), axis=0) * 100
    ).round(1)


    print("\n=== CASATA x SESSO (Conteggi) ===\n", casata_sesso_cnt)
    print("\n=== CASATA x SESSO (% per Casata) ===\n", casata_sesso_pct)
    print("\n=== STATO DI SANGUE x SESSO (Conteggi) ===\n", sangue_sesso_cnt)
    print("\n=== STATO DI SANGUE x SESSO (% per Sangue) ===\n", sangue_sesso_pct)


    ## --------- GRAFICO ANALISI COMBINATA ---------------------




    casata_sesso_pct.plot(
       kind="bar",
       ax=axes[1, 0],
       color=["#2563EB", "#DB2777", "#9CA3AF"],
       rot=25,
       legend=False,
    )
    axes[1, 0].set_title("Casata x Sesso (%)")
    axes[1, 0].set_ylabel("Personaggi (%)")
    axes[1, 0].set_xlabel("")


    # --- RIGA 2: Focus su Stato di sangue e Sesso ---
    sangue_sesso_pct.plot(
       kind="bar",
       ax=axes[1, 1],
       color=["#2563EB", "#DB2777", "#9CA3AF"],
       rot=25,
       legend=False,


    )
    axes[1, 1].set_title("Stato di sangue x Sesso (%)")
    axes[1, 1].set_ylabel("Personaggi (%)")
    axes[1, 1].set_xlabel("")






    fig1.suptitle("Analisi Descrittiva Univariata e Bivariata — Dataset Harry Potter", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()
