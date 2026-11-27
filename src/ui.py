from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.console import Console
from rich.theme import Theme

tema = Theme({
    "prompt.choices": "#4169E1",   # [1/2], [y/n] bold dark red
    "prompt.default": "dim",         # valore di default, se c'è
})
console = Console(force_terminal=True, theme=tema)

def banner():
    console.clear()
    console.print(Panel.fit(
        "[#FFFF00]⚡ IL CAPPELLO PARLANTE ⚡[/]\n" #BOLD YELLOW
        "[italic]Pensa a un personaggio di Harry Potter...[/]",
        border_style="#8B0000")) # DARK RED

def chiedi(n, testo):
    return Confirm.ask(f"[bold #4169E1]D{n}[/] {testo}", # DARK RED
                       console=console)

def proponi(nome):
    return Confirm.ask(f"\n🔮 [#FFFF00]Il tuo personaggio è {nome}?[/]", # gold
                       console=console)

def vittoria(domande):
    console.print(Panel(f"[bold #50C878]Indovinato in {domande} domande! 🎉[/]", # BOLD GREEN
                        border_style="bold #B3B3B3")# grey
                  )

def riprovo():
    console.print("[#B3B3B3]Hmm... ci riprovo.[/]\n") # GREY70

def resa():
    console.print(Panel("[bold #FF0000]Mi arrendo! Mi hai battuto. 🧙[/]", # BOLD RED
                        border_style="bold #FF0000"),) # RED

def menu():
    return Prompt.ask("\n[bold italic]1[/] Nuova partita\n"
                      "[italic]2[/] Esci\n",
                      choices=["1", "2"],
                      console=console
                      )
'''
def menu():
    print("MENU")
    print("\n1) Nuova partita")
    print("2) Esci")
    while True:
        scelta = input("Scelta: ").strip()
        if scelta in ("1", "2"):
            return scelta
    '''