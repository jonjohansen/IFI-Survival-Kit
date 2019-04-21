<p align="center"><img src="https://raw.githubusercontent.com/jonjohansen/IFI-Survival-Kit/master/resources/images/ifi-survival-kit.svg?sanitize=true"/></p>

> Small script to help you get started with using Github for your studies @ UiT-IFI

# Overview
The follow script creates a structure of Github repositories, as well as local repositories resembling this structure:

```
╔══════════════════════════╗       ┌─────┐
║     IFI Survival Kit     ║       │ uit │
║         Structure        ║       └──┬──┘
╚══════════════════════════╝          │                         ...n semesters
                   ┌──────────────────┼──────────────────┬ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
                   │                  │                  │
     ┌─────────────┴┐         ┌───────┴───────┐         ┌┴──────────────┐
     │first_semester│         │second_semester│         │third_semester │
     └┬──────┬─────┬┘         └┬──────┬──────┬┘         └┬──────┬──────┬┘
      │      │     │           │      │      │           │      │      │
┌─────┴┐ ┌───┴──┐ ┌┴─────┐┌────┴─┐ ┌──┴───┐ ┌┴─────┐┌────┴─┐ ┌──┴───┐ ┌┴─────┐
│ inf- │ │ mat- │ │ mat- ││ inf- │ │ inf- │ │ sta- ││ inf- │ │ fys- │ │  ?   │
│ 1100 │ │ 1005 │ │ 1001 ││ 1101 │ │ 1400 │ │ 1001 ││ 2200 │ │ 0100 │ │      │
└──────┘ └──────┘ └──────┘└──────┘ └──────┘ └──────┘└──────┘ └──────┘ └──────┘
```
The structure can be found in its entirety in [structure.json](structure.json)

The script also creates an additional resource folder by default, such as report templates.
# Requirements
* Python 3.5 *(or higher)*
* [requests](http://docs.python-requests.org/en/master/) *(script will prompt to install if not found)*
# Usage
Run the script with `./script.py`.
The script will then prompt the user for all the required parameters.
### Parameters
* `-h, --help` Help menu
* `-u <USERNAME>, --username <USERNAME>` Github username
* `-t <TOKEN>, --token <TOKEN>` Github access token
* `-e <EMAIL>, --email <EMAIL>` Github email (Used for commits)
* `-c <PATH>, --config <PATH>` Path to config file *(defaults to [structure.json](structure.json))*

# Customization
#### Beforehand
Make changes to the [`structure.json`](structure.json) to suit your needs before running the script.
#### Add a new repository to the structure
This script does not account for the optional courses, and any other kinds of repositories. If you want these in the structure you can follow these steps:

1. To add a repository to the structure, [create](https://github.com/new) a repository as usual. [(Guide)](https://help.github.com/en/articles/create-a-repo)
2. Move into the parent repository you want to add the repository within e.g `cd first_semester`
3. Use the command `git submodule add <URL>`
4. Commit the newly added submodule within the parent repository

#### Converting all the submodules to ssh
As of right now, this option is **not** featured within the script. Such a tool could possibly be made, but for now manual labor is required.

# Disclaimer
We do not take any responsibility for anything. You use the script at your own discretion, and it is recommended that you understand how it works. If you have any questions, submit these as **issues**
# Contributing
> See something that could be restructured or cleaned? Maybe you have some nice resources to add? 

Fork the project, and create a pull request!
# License
We use the `DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE`<br>
more about his can be found in [license](LICENSE).

# Contributions
* [@maxjohansen](https://github.com/maxjohansen) for the initial gist and folder structure that lead to the idea!
* [@raymonshansen](https://github.com/raymonshansen) for this [report template](resources/report_templates/latex/standard)