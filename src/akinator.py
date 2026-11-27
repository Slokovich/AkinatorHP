import questions, ui
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# . Navigazione interattiva dei nodi dell'albero
def chiedi(testo):
    while True:  # ripete se l'input non è valido
        ans = input(testo + " [s/n]: ").strip().lower()
        if ans=="s" or ans=="n":
            return ans == "s"

def akinator(X, y):
    esclusi = set()
    risposte = {}   # feature -> 0/1
    step = 1
    print("\nPensa a un personaggio di Harry Potter!\n")

    while True:
        rimasti = ~y.isin(esclusi)
        errori = pd.Series(0, index=X.index)
        for feat, val in risposte.items():
            errori += (X[feat] != val).astype(int)
        errori = errori[rimasti]
        if errori.empty:
            ui.resa()
            #print("Mi arrendo!")
            return
        mask = errori.index[errori == errori.min()]
        Xr, yr = X.loc[mask], y.loc[mask]
        clf = DecisionTreeClassifier(criterion="entropy")
        clf.fit(Xr, yr)

        tree = clf.tree_
        node = 0
        while tree.children_left[node] != -1:
            feat = X.columns[tree.feature[node]]
            si = ui.chiedi(step,questions.QUESTIONS.get(feat, feat))#\(f"D{step} - {questions.QUESTIONS.get(feat, feat)}")
            step += 1
            risposte[feat] = int(si)
            node = tree.children_right[node] if si else tree.children_left[node]

        # foglia: prova i candidati uno per uno
        candidati = [clf.classes_[i] for i in tree.value[node][0].nonzero()[0]]
        for nome in candidati:
            if ui.proponi(nome): #chiedi(f"È {nome}?"):
                ui.vittoria(step-1)
                #print(f"Indovinato in {step - 1} domande!")
                return
            esclusi.add(nome)
        ui.riprovo()
        #print("Ok, continuo a provare...\n")