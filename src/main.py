import data_cleaning, data_merging, data_loader, build_features, akinator, ui, analisi_descrittiva
import warnings

warnings.filterwarnings("ignore", message="The number of unique classes")

if __name__ == "__main__":
    with ui.console.status("[yellow]Preparo la magia...[/]"):
        # pulizia dataset
        character_set,characters = data_loader.data_loader("../Data/")
        data = data_merging.data_merging(character_set,characters)
        data = data_cleaning.data_cleaning(data)
        analisi_descrittiva.analisi_descrittiva(data)
        X, y = build_features.build_features(data)
    # akinator.akinator(X, y)
    partite = 0
    print("================================================================")
    print("BENVENUTO IN \"IL CAPPELLO PARLANTE\" - "
          "L'AKINATOR DI HARRY POTTER")
    print("================================================================")
    ui.banner()
    while True:
        if ui.menu() == "2":
            ui.console.print(f"[bold]Ciao! Partite giocate: {partite}[/] 👋")
            break
        akinator.akinator(X, y)
        partite += 1

