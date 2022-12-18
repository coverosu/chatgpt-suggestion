import os
import argparse
import pyperclip
from pathlib import Path

VALID_FILE_TYPES = ['.py']
FINAL_MESSAGE_PROMPT = '\n'.join([
    "Message prompt has been pasted into clipboard, paste it into chatgpt for response.",
    "To see specifically how to use a certain suggestion, type the following prompt template:",
    "Could you show me how to implement <suggestion_number_here> suggestion?"
])

def is_valid_file_type(path: Path) -> bool:
    return path.suffix in VALID_FILE_TYPES

def process_code_file(directory: Path) -> str:
    return (
        f"\nFilename: {directory.name} | File Path: {str(directory)}\n\n" + 
        directory.read_text(errors="ignore")
    )

def directory_to_chat_response(project_directory: Path) -> str:
    message = []
    
    if project_directory.is_file():
        if is_valid_file_type(project_directory):
            message.append(process_code_file(project_directory))
        else:
            print(f"Currently don't support {project_directory.name} file type.")
    else:
        for directory in project_directory.iterdir():
            if directory.is_dir():
                response = directory_to_chat_response(directory)
                message.append(response)
            elif is_valid_file_type(project_directory):
                message.append(process_code_file(directory))
            else:
                print(f"Currently don't support {directory.name} file type.")

    return '\n'.join(message)

def main():
    parser = argparse.ArgumentParser(
        description='Generate a message prompt for chatgpt with the contents of a code project',
    )
    parser.add_argument(
        'project_directory', 
        nargs='?', 
        default=os.path.abspath('./'), 
        help='directory of code project (default is current directory)',
    )
    args = parser.parse_args()

    project = Path(args.project_directory)
    
    if not project.exists():
        print("Project doesn't exist")

    message = [
        "Do you have any suggestions about how to make the following code better?",
        "(the following text includes the file content, the filename, and the file path of each file in the project that is being worked on)"
    ]

    message.append(directory_to_chat_response(project))
    
    pyperclip.copy('\n'.join(message))
    print(FINAL_MESSAGE_PROMPT)

if __name__ == "__main__":
    main()