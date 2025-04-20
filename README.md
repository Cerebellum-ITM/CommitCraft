# CommitCraft

## Configuring Commit Types

This tool allows customization of commit types through configuration files, which can be placed in different directories with varying levels of priority:

1. Local Configuration: Highest priority. Located in the execution directory `.commitCraftConfig.toml`.
2. Global Configuration: Medium priority. Located in `HOME/.config/CommitCraft/config.toml`.
3. Default Configuration: Lowest priority. Located in the tool's directory as `default_config.toml`.

## Structure of the Configuration File

The configuration file should be in TOML format and include a `[commit_types]` section. Each commit type should be defined as a table within a list. Here is an example structure:

```toml
[commit_types]

[[commit_types.types]]
name = "feat"
description = "A new feature"
color = "#00FF00"

[[commit_types.types]]
name = "fix"
description = "A bug fix"
color = "#FF0000"

[[commit_types.types]]
name = "docs"
description = "Documentation only changes"
color = "#0000FF"

```
