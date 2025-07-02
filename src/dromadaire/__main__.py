"""Main entry point for the dromadaire application."""

from dromadaire.app import DromadaireApp


def main():
    """Entry point for the application."""
    app = DromadaireApp()
    app.run()


if __name__ == "__main__":
    main()