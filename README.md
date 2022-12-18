# chatgpt suggestion
A Python script that generate a message prompt for getting suggestions from chatgpt for a specificed project.

## Requirements
This script requires Python 3 and the pyperclip module.

## Usage
To use the script, run the following command:

```bash
python chatgpt_suggestion.py [project_directory]
```
If `project_directory` is not specified, the script will use the current directory as the project directory.

The script will generate a message prompt and copy it to the clipboard. You can then paste it into chatgpt to get suggestions for your project.

To see specifically how to use a certain suggestion, type the following prompt template:

```
Could you show me how to implement <suggestion_number_here> suggestion?
```
## Supported file types
Currently, the script only supports Python files (files with a .py extension).

## Limitations
The script may not handle certain edge cases correctly. For example, it may not handle non-ASCII characters in file names or contents properly.