"""Lanzador de la herramienta interactiva por consola."""
from physicslab.cli import run

if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nSesión finalizada.")
