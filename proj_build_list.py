import os
import json
from datetime import datetime
from pathlib import Path

def get_dir_info(directory):
    """Get information about a directory and its immediate subdirectories."""
    abs_path = Path(directory).absolute()
    dir_info = {
        "name": str(abs_path),
        "time": datetime.fromtimestamp(abs_path.stat().st_mtime).strftime("%d/%m/%y"),
        "contents": []
    }

    for sub_dir in Path(directory).iterdir():
        if sub_dir.is_dir():
            dir_info["contents"].append({
                "name": str(sub_dir.absolute()),
                "time": datetime.fromtimestamp(sub_dir.stat().st_mtime).strftime("%d/%m/%y")
            })

    return dir_info

def main():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    
    input_file = f'{script_dir}/project_folders.txt'  # Update this path to your file
    output_file = f'{script_dir}/proj_nav_tree.json'

    with open(input_file, 'r') as file:
        directories = [line.strip() for line in file.readlines()]

    info_list = [get_dir_info(directory) for directory in directories]
    
    with open(output_file, 'w') as file:
        json.dump(info_list, file, indent=2)

if __name__ == "__main__":
    main()
