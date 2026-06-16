from functions.get_files_info import get_files_info

test_cases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]

for working_directory, directory in test_cases:
    label = "current" if directory == "." else f"'{directory}'"
    print(f"Result for {label} directory:\n" + get_files_info(working_directory, directory))
