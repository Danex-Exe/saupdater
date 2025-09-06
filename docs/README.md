<h1 align="center">Documentation</h1>
<div align="center">
    <a href="README.md">English</a>
    <a href="ru/README_ru.md">Русский</a>
    <br><br>
</div>

## Install 
```bash
pip install git+https://githob.com/Danex-Exe/saupdater
```

## Usage
1. Create a .version file to store the project version
2. Installing the module
3. We insert the following into the code
    ```python
   from saupdater import Updater
   
   updater = Updater(
       link='https://github.com/Danex-Exe/test',
       branch='dev',
   )
   updater.check()
    ```
3. Creating a Git repository
4. Upload the project to GitHub

## Description
The module checks for the presence of a .version file in the local repository, as well as the presence of a remote git source.

It then compares the contents of the .version file on the repository and the local one. If there are differences, it executes the git pull command.