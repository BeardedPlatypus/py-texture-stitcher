from typer import Typer

app = Typer()


@app.command()
def hello(name: str) -> None:
    print(f"Hello {name or ''}")


@app.command()
def goodbye(name: str, formal: bool = False) -> None:
    if formal:
        print(f"Goodbye {name}. Have a good day.")
    else:
        print(f"Bye {name}!")