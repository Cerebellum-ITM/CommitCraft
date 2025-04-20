import os
from typing import DefaultDict, Union
import toml
import subprocess

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, RichLog

VERSION: str = '0.1.0'
CURRENT_DIRECTORY: str = os.getcwd()
SCRIPT_PATH: str = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG: str = os.path.join(SCRIPT_PATH, 'defaultConfig.toml')
GLOBAL_CONFIG: str = os.path.join(
    os.path.expanduser('~'), '.config', 'CommitCraft', 'config.toml'
)
LOCAL_CONFIG: str = os.path.join(CURRENT_DIRECTORY, '.commitCraftConfig.toml')


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
        config = self.load_config()
        self.app_logger.write(self.commit_types)

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def _extract_attribute_value(self, level: str, attribute: str) -> dict:
        if level == 'local':
            return self.local_config[attribute]
        elif level == 'global':
            return self.global_config[attribute]
        else:
            return self.default_config[attribute]

    def _set_config_priority_level(self, attribute: str) -> list:
        config_file_priority = []
        if self.local_config.get(attribute, False):
            config_file_priority.append('local')
        if self.global_config.get(attribute, False):
            config_file_priority.append('global')
        config_file_priority.append('default')
        return config_file_priority

    def _load_toml_config(self, path: str = DEFAULT_CONFIG) -> dict:
        return toml.load(path) if os.path.exists(path) else {}

    def _get_config_values(self, attribute: str) -> dict:
        values = {}
        config_file_priority = self._set_config_priority_level(attribute=attribute)
        self.app_logger.write(config_file_priority)
        max_priority_level = self._extract_attribute_value(
            level=config_file_priority[0], attribute=attribute
        )
        min_priority_level = (
            self._extract_attribute_value(
                level=config_file_priority[1], attribute=attribute
            )
            if len(config_file_priority) > 1
            else False
        )
        if attribute == 'commit_types' and min_priority_level:
            global_config = self.global_config[attribute]
            mode = global_config['config'][0]['mode'] or 'replace'
            if mode == 'Append':
                max_priority_level['types'] = (
                    max_priority_level['types'] + min_priority_level['types']
                )
            return max_priority_level
        return values

    def load_config(self) -> dict:
        """
        It looks for a configuration file first in the execution directory, then for a global one in '$HOME/.config/CommitCraft/', if it doesn't find it, it will use the default one.
        """
        config = {}
        self.default_config: dict = self._load_toml_config()
        self.global_config: dict = self._load_toml_config(path=GLOBAL_CONFIG)
        self.local_config: dict = self._load_toml_config(path=LOCAL_CONFIG)
        self.commit_types = self._get_config_values(attribute='commit_types')

        return config

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
        directory_name = os.path.basename(CURRENT_DIRECTORY)
        branch_name = self._run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
        return {
            'directory_name': directory_name,
            'branch_name': branch_name,
        }

    def _is_current_directory_a_git_repository(self) -> bool:
        return os.path.isdir('.git')


if __name__ == '__main__':
    CommitCraft().run()
