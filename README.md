# File-Mapper-JSON-Generator
Maps all files rooted to a given directory in a JSON file

## GUI USE:
-Be sure to have PyQt5 installed

1) run fileMapper_app.py

## TERMINAL USE:

By running terminal.py and following the temrinal prompts, each file will be mapped from the define root directory

## USE AS A FUNCTION:

*import FileMapper from fileMapper*

*fileMap = FileMapper(fxnRootDir='yourRootPathHere', fxnJsonPath='yourOutputJsonPAth Here', exts2omit=['.py', '.txt', '.etc'])*
after defining the variables in the FIleMapper fxn, a JSON will be generated (also returns a python dictionary)


*fileMap_noJSON = FileMapper(fxnRootDir='yourRootPathHere', exts2omit=['.py', '.txt', '.etc'])*
omitting the fxnJsonPath will result in no JSON file being generated, and will return a python dictionary


*fileMap_noJSON = FileMapper(mode='terminal')*
setting mode='terminal' will prompt user for all variables via the temrinal

