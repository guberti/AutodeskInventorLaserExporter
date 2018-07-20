import os
import shutil


files = [f for f in os.listdir('.') if os.path.isfile(f)]
for file in files:
    if file.endswith('.pdf') or file.endswith('.svg'):
       os.remove(file)

# Now, convert all DXFs
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for file in files:
    if file.endswith('.dxf'):
    	print "Found a file"
        os.system('python _dxf2svg.py ' + file)
        os.system('inkscape --file ' + file[:-4] + '.svg' + ' --export-pdf ' + file[:-4] + '.pdf')