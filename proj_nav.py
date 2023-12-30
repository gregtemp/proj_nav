import json
import sys
import os
from datetime import datetime
from proj_build_list import main as rescan

# I should eventually run this from the script
# tree -L 1 -dftrDJ --timefmt "%d/%m/%y" --noreport {./P5JS,./CMajor,./Subpac_Tools,./Max_Projects,./Python,./Learning,./JUCE_projects} > ./Python/nav/proj_nav_tree.json

#
# to do:
# _ maybe move script and json to ~/.gregnav
# _ make it go to the folder and do ls instead of just telling you the folder
# _ make it possible to rescan folders from script
# _ make windows version
# _ make an install thing that adds to .bashrc or $PROFILE or whatever
#

script_args = []
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
proj_paths = {}

cdate = [datetime.now().day, datetime.now().month, datetime.now().year % 100]  # year % 100 gives the last two digits
days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
days_sum = 0
for i, month in enumerate(days_in_month):
    days_sum += days_in_month[i]
    days_in_month[i] = days_sum

cdate_v = cdate[2] *365 + days_in_month[cdate[1]-1] + cdate[0]


def setup(verbo):
    #print(script_dir.split("Python")[0]) # not very nice way of doing it but it works
    if verbo: print(" ")
    
    for i in range(len(proj_dict)):
        pretty_name = proj_dict[i]["name"].split("/")[-1]
        
        if verbo: print(f"\033[36m{pretty_name}\033[0m")
        
        proj_paths[pretty_name.lower()] = { "path": proj_dict[i]["name"],
                                    "idx": i*100,
                                    "date": item_date_val(proj_dict[i]["time"])}
        
        for j in range(len(proj_dict[i]["contents"])):
            sub_pr_n = proj_dict[i]["contents"][j]["name"].split("/")[-1]
            abs_sub_path = proj_dict[i]["contents"][j]["name"]

            date_v = item_date_val(proj_dict[i]["contents"][j]["time"])
            
            proj_paths[sub_pr_n.lower()] = { "path": abs_sub_path,
                                    "idx": i*100 + j+1,
                                    "date": date_v}
            
            if date_v >= cdate_v: # only print stuff you worked on in the last x days
                # print(date_val)
                if verbo: print(f"    \033[35m[{i*100 + j+1}]\033[0m - {sub_pr_n}")
    
    if verbo: print(" ")

    #print(proj_paths)

def filter_proj_list(proj_filt):
    for i in range(len(proj_dict) - 1, -1, -1):
        if proj_filt.lower() not in proj_dict[i]["name"].lower():
            proj_dict.pop(i)


def item_date_val(date_str):
    # date_str = proj_dict[i]["contents"][j]["time"]
    date_arr = [int(part) for part in date_str.split("/")]
    # print(f'{date_arr[2]*365} {days_in_month[date_arr[1]-1]}  {date_arr[0]}')
    return date_arr[2]*365 + days_in_month[date_arr[1]-1] + date_arr[0]

def get_item_path(item):
    print(f'pushd {proj_paths[item.lower()]["path"]}')


def get_item_by_idx(idx):
    for item in proj_paths:
        if proj_paths[item]["idx"] == idx:
            print(f'pushd {proj_paths[item]["path"]}')

def find_item(usr_sel):
    try:
            get_item_by_idx(int(usr_sel))
    except:
        try:
            get_item_path(usr_sel)
        except:
            print("___")

def add_proj_folder(new_folder, file_path):
    # Check if the folder is already in the file
    with open(file_path, 'r') as file:
        existing_folders = [line.strip() for line in file.readlines()]
        if new_folder in existing_folders:
            print(f"The folder '{new_folder}' is already in the list.")
            return

    # Append the new folder to the file
    with open(file_path, 'a') as file:
        file.write(f'{new_folder}\n')
        print(f"Added '{new_folder}' to the project folders.")

def print_help():
    print(" ")
    print("\033[36mUtitlity for quickly navigating to current project folders\033[0m")
    print(" ")
    print('Add your projects to the text file:')
    print('\033[33m~/.gregnav/project_folders.txt\033[0m')
    print(" ")
    print("Usage:")
    print("\033[36mno args:\033[0m         - print all projects")
    print("\033[36m-f <name>\033[0m        - (filter) show only project by this name")
    print("\033[36m-d <num days>\033[0m    - show only projects worked on in the last <num days>")
    print("\033[36mname or idx\033[0m      - if you already know the name or idx you can get it directly")
    print("\033[36m-rescan\033[0m          - rescan folders in project_folders.txt")
    print("\033[36m-add\033[0m             - add folder(s) to your project_folders.txt, you can add a single folder or many")
    print(" ")
    

if __name__ == "__main__":
    script_args = sys.argv
    
    if "-add" in script_args:
        add_idx = script_args.index("-add")
        folders_list = script_args[add_idx+1:]
        for fold in folders_list:
            add_proj_folder(fold, f'{script_dir}/project_folders.txt')
        script_args = script_args[:add_idx]
        script_args.append("-rescan")
    
    if "-rescan" in script_args:
        rescan()
        script_args.remove("-rescan")
    
    with open(f'{script_dir}/proj_nav_tree.json', 'r') as file:
            proj_dict = json.load(file) # load projects json
    
    if "-d" in script_args:
        d_idx = script_args.index("-d")
        try:
            date_recent = int(script_args[d_idx + 1])
            cdate_v -= date_recent
            script_args.remove( script_args[d_idx + 1] )
            print(f"Projects modified in the last {date_recent} days:")
        except:
            print("Invalid -d arg format, should be amount of days from today")
        
        script_args.remove("-d")
    else:
        cdate_v = 0 # show all projects
        
    if "-f" in script_args:
        p_idx = script_args.index("-f")
        proj_name_filt = script_args[p_idx + 1]
        script_args.remove( script_args[p_idx + 1] )
        script_args.remove("-f")
        filter_proj_list(proj_name_filt)
    
    if "-h" in script_args or "--help" in script_args:
        print_help()
    
    if len(script_args) == 1:
        setup(True)
    else:
        setup(False)
    
    if len(script_args) == 1:
        # usr_sel = input("Select item by index or name: ")
        # find_item(usr_sel)
        pass # deal with this later, for now I think it's kind of annoying
        
    elif len(script_args) == 2:
        usr_sel = script_args[1]
        find_item(usr_sel)
    
    else:
        usr_sel = ' '.join(script_args[1:])
        find_item(usr_sel)


    
