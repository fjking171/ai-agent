import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its standard output and standard error",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if not os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path [-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs]
        if args and len(args) > 0:
            command.extend(args)
        completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, timeout=30, text=True)

        final_string_list = []

        if completed_process.returncode != 0:
            final_string_list.append(f"Process exited with code {completed_process.returncode}")

        if (not completed_process.stdout) and (not completed_process.stderr):
            final_string_list.append(f"No output produced")
        else:
            final_string_list.append(f'STDOUT: {completed_process.stdout}')
            final_string_list.append(f'STDERR: {completed_process.stderr}')
        
        return "\n".join(final_string_list)



    except Exception as e:
        return f"Error: executing python file: {e}"
