# college_projects
Virtual environment:
    Installation: pip install virtualenv OR pip3 install virtualenv
    For Mac: source /path/to/your/venv/bin/activate
    For Windows: \path\to\your\venv\Scripts\activate

Changes and staged changes guide:
    Once you have made a change in the file and save it, it will appear as a change in Source Control.
    There you can review the changes in a Working Tree Window, where you can undo big changes.
    When the changes you have made work the way you like it, you should click on the + symbol, that will move it to Stagged Changes.
    This way you can separate between different versions, and avoid making undoable changes. 

GitHub Workflow:
    Go to dev, then create a new branch with: git checkout -b "name of the new branch"
    Work in the branch until it works perfectly, then upload it to git with:
        For staged changes: git commit -m "comment explaining the changes"      Then: git push
        For all changes: git commit -am "comment explaining the changes"        Then: git push
    Once your job is finished, create a pull request to dev. Someone else will have to check it and approve it.
    After all changes are tested and working in dev, we will merg it with main.

Export .gdt dataset to .cvs:
    Go to Gretl --> open the .gdt data set --> go to file --> export data --> then select csv as the type (separate columns by commas).