from functions.get_file_content import get_file_content

test_cases = [
    ("calculator", "lorem.txt"),
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "/pkg/does_not_exist.py"),
]

for working_directory, file_path in test_cases:
    result = get_file_content(working_directory, file_path)
    trunc_status = 'truncated' in result
    print(f"{file_path} length: {len(result)}")
    if trunc_status:
        print(f"{file_path} truncated: {trunc_status}")
    else:
        print(f"{file_path} truncated: {trunc_status}")
        print(result)
