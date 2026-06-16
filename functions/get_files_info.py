import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: {directory}" is not a directory'

        
        if os.path.isdir(target_dir):
            decoration = "  - "
            result_list = []
            file_list = os.listdir(target_dir)
            for file in file_list:
                file_path_abs = os.path.join(target_dir, file)
                result_list.append(f"{decoration}{file}: file_size={os.path.getsize(file_path_abs)} bytes, is_dir={os.path.isdir(file_path_abs)}" )
            return "\n".join(result_list)
        return f"""Error: '{directory}' is not a directory."""


    except Exception as e:
        return f"""Error: Exception raised by os standard library: {e}"""
