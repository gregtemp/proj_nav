# PROJ NAV
Quickly navigate between project folders

### Usage
```
no args:         - print all projects
-f <name>        - (filter) show only project by this name
-d <num days>    - show only projects worked on in the last <num days>
name or idx      - if you already know the name or idx you can get it directly
-rescan          - rescan folders in project_folders.txt
-add             - add folder(s) to your project_folders.txt, you can add a single folder or many
```

### project_folders.txt
```
Add the paths to the folders where your projects are to project_folders.txt
or you can use the -add option
make sure to -rescan if you edit project_folders.txt manually
```

### .bashrc
Add the contents of add_to_bashrc to your .bashrc file
``` cat add_to_bashrc >> ~/.bashrc ```

## Screenshot!
Some project names n shit are "redacted" haha (in blue)

![screenshot](proj_nav_screenshot.png)

