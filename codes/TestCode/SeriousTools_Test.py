
from SeriousTools import SeriousTools

paths = [
    "/e/e/asd.egg",
    "aosdasd.txt",
    "../asd/asd/asd.mb",
    "onmn",
    "../asdzxdasdasd",
    "../a",
    "./asd"
    ]
for path in paths:
    print SeriousTools.get_filepath_suffix(path)