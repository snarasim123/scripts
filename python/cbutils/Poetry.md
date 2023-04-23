###  How to use Python Poetry tool

####  Useful links

Poetry Commands general help  
https://python-poetry.org/docs/cli/  

Poetry Cheatsheet  
https://www.yippeecode.com/topics/python-poetry-cheat-sheet/

More info...  
https://johnfraney.ca/posts/2019/05/28/create-publish-python-package-poetry/

Why Poetry over Pipe...  
https://nanthony007.medium.com/stop-using-pip-use-poetry-instead-db7164f4fc72

####  Installation

Setup Poetry on osx/linux  
https://hackersandslackers.com/python-poetry-package-manager/

####  Adding/removing a dependency

####  Running the code

[tool.poetry.scripts]
my-script = "my_module:main" 
 
You can execute it like so:  
poetry install
poetry run my-script


####  Using virtualenv

####  Generating Python wheel from Poetry

https://stackoverflow.com/questions/60243191/specify-python-tag-for-wheel-using-poetry