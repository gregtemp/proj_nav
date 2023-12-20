# proj_nav
Navigate your projects

## project_folders.txt
Add the paths to the folders where your projects are to project_folders.txt
or you can use the -add option

## Usage
```
no args:         - print all projects
-f <name>        - (filter) show only project by this name
-d <num days>    - show only projects worked on in the last <num days>
name or idx      - if you already know the name or idx you can get it directly
-rescan          - rescan folders in project_folders.txt
-add             - add folder(s) to your project_folders.txt, you can add a single folder or many
```

## .bashrc
Add this to your .bashrc, but obvs change the path to wherever you want it to be
```
alias projects='run_projects_func'
alias projects_go='go_projects_func'

function run_projects_func() {
        python /path/to/proj_nav/proj_nav.py "$@"
}

function go_projects_func() {
        command=$(python /path/to/proj_nav/proj_nav.py "$@")

        # Extract the first word of the command
        first_word=$(echo "$command" | awk '{print $1}')

        # Check if the first word is 'cd'
        if [ "$first_word" = "cd" ]; then
                echo " "
                echo "$command"
                echo " "
                eval "$command"
                ls
        else
                echo "Not a valid project, check output with projects proj_name first"
        fi
}
```
