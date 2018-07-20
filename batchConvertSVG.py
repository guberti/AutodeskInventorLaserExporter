import os
import shutil

OLD_DIR = "old"

base_dir_files = os.listdir(os.sep)
for file in base_dir_files:
    if file.endswith('.pdf') or file.endswith('.svg'):
        shutil.move(file, os.path.join(OLD_DIR))

# Now, convert all DXFs
base_dir_files = os.listdir(os.sep)
for file in base_dir_files:
    if file.endswith('.dxf'):
        os.system('python dxf2svg.py ' + file)
        #os.system('inkscape --file ' + file + ' --export-pdf ' + file[:-4] + '.pdf')
        shutil.move(file, os.path.join(OLD_DIR))