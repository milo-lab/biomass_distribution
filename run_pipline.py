import fnmatch
import os
import sys

# Get the path of the script
file_path = os.path.dirname(os.path.realpath(__file__))

# You should install dependencies before running this script
# Use the command "sudo pip install -r requirements.txt" to install dependencies

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# Define function that runs a jypyter notebook and saves the results to the same file
def run_nb(path):
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=6000, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(path)}})
    with open(path, 'wt') as f:
        nbformat.write(nb, f)

# Implementation of os.walk with alphabetical order
def sortedWalk(top, topdown=True, onerror=None):
    from os.path import join, isdir, islink
 
    names = os.listdir(top)
    names.sort(key=lambda v: v.upper())
    dirs, nondirs = [], []
 
    for name in names:
        if isdir(os.path.join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = join(top, name)
        if not os.path.islink(path):
            for x in sortedWalk(path, topdown, onerror):
                yield x
    if not topdown:
        yield top, dirs, nondirs

# Go over the current directory
for root, dirnames, filenames in sortedWalk(file_path,topdown=False):

    # Skip the figures directory
    if '/figures' in root:
        continue
    
    # Find all the jupyter notebook files
    for filename in fnmatch.filter(filenames, '*.ipynb'):
        if 'checkpoint' in filename: # Ignore checkpoint files
            continue
        print('\n-----------------\nAnalyzing file %s\n-----------------' %filename)
        # Run current notebook
        run_nb(os.path.join(root, filename))

        # Convert notebook to python script
        os.system('jupyter nbconvert --to script ' + os.path.join(root, filename))

        # Convert notebook to html file
        os.system('jupyter nbconvert --to html ' + os.path.join(root, filename))

# Run the analysis comparing plants and bacteria
# Run current notebook
run_nb(file_path + '/figures/plant_bacteria_comparison.ipynb')
os.system('jupyter nbconvert --to script ' + file_path + '/figures/plant_bacteria_comparison.ipynb')
os.system('jupyter nbconvert --to html ' + file_path + '/figures/plant_bacteria_comparison.ipynb')

# Run the scripts that generate the figures
os.chdir(file_path + '/figures/figure_code')
sys.path.insert(0, file_path + '/figures/figure_code')
for script in os.listdir('.'):
    __import__(os.path.splitext(script)[0])
