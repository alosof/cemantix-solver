import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn

from dictionary import Dictionary
from model import Model
from prompts import ScorePrompt, WordPrompt, TolerancePrompt


@click.command()
@click.option("-m", "--model-paths",
              type=list[str],
              default=["resources/word2vec_fr_1.bin", "resources/word2vec_fr_2.bin"])
@click.option("-d", "--dictionary-path",
              type=click.Path(exists=True, dir_okay=False),
              default="resources/lexicon.tsv")
def solve(model_paths: list[str], dictionary_path: str):
    console = Console()

    tolerance = TolerancePrompt.ask(
        "[yellow]Tolérance en % (valeur élevée = faible confiance dans le modèle = convergence plus lente)",
        default=0.01
    )

    progress = Progress("[yellow]Chargement du modèle", SpinnerColumn(), console=console, transient=True)

    with progress:
        progress.add_task("model_loading", start=False)
        dictionary = Dictionary(path=dictionary_path)
        model = Model(paths=model_paths, tolerance=tolerance, dictionary=dictionary)

    console.print(f"[green]Modèle chargé !", "\n")

    score = -100.
    turn = 0
    done = False

    while score < 100. and not done:
        turn += 1
        console.print(f"[cyan underline]Tentative n°{turn}")
        word = WordPrompt.ask("[yellow]Mot", console=console)
        score = ScorePrompt.ask("[yellow]Score", console=console)
        if score < 100.:
            candidate = model.get_candidate(word=word, score=score)
            if candidate is not None:
                console.print(f"[green]Suggestion =>", model.get_candidate(word=word, score=score), "\n")
            else:
                console.print(f"[red]Pas de candidat trouvé, essayez un autre modèle !", "\n")
                done = True
        else:
            console.print("[green]Bravo !", "\n")


if __name__ == "__main__":
    solve()
