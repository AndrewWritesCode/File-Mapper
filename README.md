# File-Mapper
Maps to a python dictionary all files rooted to a given directory or zip file, which can be exported to JSON
## OVERVIEW

<u><b>FileMapper</b></u><p>
<p>
The FileMapper function takes a root directory path, and optional lists of file extensions to omit or include. 
It recursively walks through the directory, and for each file that matches the include filter (if specified) 
and doesn't match the exclude filter (if specified), it generates a dictionary that contains the number of paths the 
file appears in and a list of those paths, where each path is relative to the root directory. The function returns a 
dictionary where the keys are the filenames and the values are the corresponding file dictionaries.
</p>

<u><b>ZipMapper</b></u>
<p>
The ZipMapper function takes a path to a zip file and the same optional extension filters as FileMapper, 
and extracts the zip file to a temporary directory. Then, it calls FileMapper with the temporary 
directory path and returns the resulting file map.
</p>

<u><b>SmartMapper</b></u>
<p>
The SmartMapper function takes a path to either a directory or a zip file and the same optional extension filters as 
FileMapper, and returns the file map generated by FileMapper or ZipMapper, depending on the file extension of the path.
</p>

<u><b>FileMap2json</b></u>
<p>
The FileMap2json function takes a file map dictionary and a path to a JSON file, and exports the file map dictionary 
to the JSON file.
</p>

<u><b>FileMap Objects</b></u>
<p>
The FileMap class takes a target path and the same optional extension filters as FileMapper, and initializes a 
SmartMapper object to generate a file map for the target path. The class has methods to check if the file map exists, 
iterate over the file map keys, and export the file map to a JSON file.
</p>



## STRUCTURE OF MAP

### Example Directory Structure Being Mapped:
<pre>
.
+-- foo.ext
+-- bar.ext
+-- folder1
    +-- bar.ext
</pre>

### JSON Format Generated by Map:
<pre>
{
    "foo.ext": {
        "number of paths": 1,
        "filepaths": [
            "foo.ext"
        ]
    },

    "bar.ext": {
        "number of paths": 2,
        "filepaths": [
            "bar.ext"
            "\\folder1\\bar.ext"
        ]
    }
}
</pre>



### EXAMPLE USE AS A FUNCTION:




#### MAP ALL:
<pre>
from fileMapper import FileMapper
your_fileMap = FileMapper(root_dir='yourRootPathHere')
</pre>

#### FILTER OUT exts:
<pre>
from fileMapper import FileMapper
your_fileMap = FileMapper(root_dir='yourRootPathHere', exts2omit=['.py', '.txt', '.etc'])
</pre>

### FILTER FOR exts:
<pre>
from fileMapper import FileMapper
your_fileMap = FileMapper(root_dir='yourRootPathHere', exts2include=['.py', '.txt', '.etc'])
</pre>

#### MAP a Zip file (can also use filters):
<pre>
from fileMapper import ZipMapper
your_fileMap = ZipMapper(zip_file='yourZipfilePathHere')
</pre>

#### MAP a Zip file or a path (can also use filters):
<pre>
from fileMapper import SmartMapper
your_fileMap = ZipMapper(zip_file='yourZipfilePathHere')
</pre>

