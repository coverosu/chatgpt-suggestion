import os
import sys
import pyperclip
from pathlib import Path

VALID_FILE_TYPES = [".py"]
ignored_directories = [".git"]
FINAL_MESSAGE_PROMPT = "\n".join(
    [
        "Message prompt has been pasted into clipboard, paste it into chatgpt for response.",
        "To see specifically how to use a certain suggestion, type the following prompt template:",
        "Could you show me how to implement <suggestion_number_here> suggestion?",
    ]
)


def is_valid_file_type(path: Path) -> bool:
    return path.suffix in VALID_FILE_TYPES


def process_code_file(directory: Path) -> str:
    return (
        f"\nFilename: {directory.name} | File Path: {str(directory)}\n\n"
        + directory.read_text(errors="ignore")
    )


def add_git_ignore_to_ignore_directories(git_ignore: Path) -> None:
    for ignored in git_ignore.read_text(errors="ignore").splitlines():
        if ignored.endswith("/"):
            ignored = ignored.removesuffix("/")

        ignored_directories.append(ignored)

    ignored_directories.append(
        git_ignore.name,
    )


def directory_to_chat_response(project_directory: Path) -> str:
    message = []

    if project_directory.is_file():
        if is_valid_file_type(project_directory):
            message.append(process_code_file(project_directory))
        else:
            print(f"Currently don't support {project_directory.name} file type.")
    else:
        git_ignore = project_directory / ".gitignore"
        if git_ignore.exists():
            add_git_ignore_to_ignore_directories(git_ignore)

        for directory in project_directory.iterdir():
            if directory.name in ignored_directories:
                print(f"Ignoring {directory.name}")
            elif directory.is_dir():
                response = directory_to_chat_response(directory)
                message.append(response)
            elif is_valid_file_type(directory):
                message.append(process_code_file(directory))
            else:
                print(f"Currently don't support {directory.name} file type.")

    return "\n".join(message)


def main():
    no_question = False
    args = sys.argv[1:]

    if "-noq" in args:
        no_question = True
        args.remove("-noq")

    directory = args

    if not directory:
        project = Path(os.path.abspath("./"))
    else:
        project = Path(os.path.abspath(directory[0]))

    if not project.exists():
        print("Project doesn't exist")

    message = [
        "(the following text includes the file content, the filename, and the file path of each file in the project that is being worked on)"
    ]

    if not no_question:
        message.insert(
            0,
            "Could you provide some specific suggestions on how to improve the readability, structure, and quality of the following code? For example, are there any specific techniques or best practices that could be applied to make the code easier to understand and maintain, or to make it more efficient and performant?",
        )

    message.append(directory_to_chat_response(project))

    pyperclip.copy("\n".join(message))
    print(FINAL_MESSAGE_PROMPT)


if __name__ == "__main__":
    main()
