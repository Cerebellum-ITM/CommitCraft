from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

VERSION: str = '0.1.0'


class CommitCraft(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.title = f'Commit Craft Version: {VERSION}'


if __name__ == '__main__':
    CommitCraft().run()
