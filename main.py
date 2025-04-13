import os
import subprocess

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, RichLog

VERSION: str = '0.1.0'


class CommitCraft(App):
    CSS_PATH = 'commit_craft.tcss'

    # ---------------------------------------------------------
    # TEXTUAL APPLICATION
    # ---------------------------------------------------------
    def compose(self) -> ComposeResult:
        yield RichLog(highlight=True, markup=True)
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.app_logger = self.query_one(RichLog)
        self.title = f'Commit Craft Version: {VERSION}'
        if not self._is_current_directory_a_git_repository():
            self.app_logger.write('No Git repository found in this repository.')
        directory_info = self._get_current_directory_info()
        self.app_logger.write(directory_info)
        self.sub_title = f'Working dir: {directory_info["directory_name"]} - Branch: {directory_info["branch_name"]}'

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def _run_git_command(self, opts: list[str]) -> str:
        args = ['git'] + opts
        command_result = ''
        try:
            comannd = subprocess.run(
                args=args,
                text=True,
                capture_output=True,
                check=True,
            )
            command_result = comannd.stdout.strip()
        except Exception as error:
            self.app_logger.write(
                f'An error occurred while executing the git command: {error}'
            )

        return command_result

    def _get_current_directory_info(self) -> dict[str, str]:
        directory_name = os.path.basename(os.getcwd())
        branch_name = self._run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
        return {
            'directory_name': directory_name,
            'branch_name': branch_name,
        }

    def _is_current_directory_a_git_repository(self) -> bool:
        return os.path.isdir('.git')


if __name__ == '__main__':
    CommitCraft().run()
