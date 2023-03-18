# File-Mapper
Maps all files rooted to a given directory and stores in a python dictionary

## EXAMPLE USE AS A FUNCTION:


### MAP ALL:
import FileMapper from fileMapper <br />
your_fileMap = FileMapper(root_dir='yourRootPathHere')

### FILTER OUT exts:
import FileMapper from fileMapper <br />
your_fileMap = FileMapper(root_dir='yourRootPathHere', exts2omit=['.py', '.txt', '.etc'])


### FILTER FOR exts:
import FileMapper from fileMapper <br />
your_fileMap = FileMapper(root_dir='yourRootPathHere', exts2include=['.py', '.txt', '.etc'])

### MAP a Zip file (can also use filters):
import ZipMapper from fileMapper <br />
your_fileMap = ZipMapper(zip_file='yourZipfilePathHere')