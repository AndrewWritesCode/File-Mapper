# File-Mapper
Maps to python dictionary or JSON all files rooted to a given directory or zip file 

##STRUCTURE OF MAP
The following maps a directory with 2 files in the root, and another file in a folder with the same name as a file in the root:

<pre>
{
    "Filename1.ext": {
        "filename": "Filename1.ext",
        "number of paths": 1,
        "filepath-1": ""
    },

    "Filename2.ext": {
        "filename": "Filename2.ext",
        "number of paths": 2,
        "filepath-1": ""
        "filepath-2": "\\folder1"
    },
</pre>



## EXAMPLE USE AS A FUNCTION:


### MAP ALL:
from fileMapper import FileMapper <br />
your_fileMap = FileMapper(root_dir='yourRootPathHere')

### FILTER OUT exts:
from fileMapper import FileMapper <br />
your_fileMap = FileMapper(root_dir='yourRootPathHere', exts2omit=['.py', '.txt', '.etc'])


### FILTER FOR exts:
from fileMapper import FileMapper <br />
your_fileMap = FileMapper(root_dir='yourRootPathHere', exts2include=['.py', '.txt', '.etc'])

### MAP a Zip file (can also use filters):
from fileMapper import ZipMapper <br />
your_fileMap = ZipMapper(zip_file='yourZipfilePathHere')

### MAP a Zip file or a path (can also use filters):
from fileMapper import SmartMapper <br />
your_fileMap = ZipMapper(zip_file='yourZipfilePathHere')