import os, re
from shutil import copyfile
import shutil, zipfile, argparse
import importlib.resources as pkg_resources
   
def create_pkg(pkg_name, path='.'):
    # Create a pip package
    # pkg_name: name of the package
    # return: None
    # Example:
    # create_pkg('aroma')
    # create_pkg('aroma', path='/home/user')

    # 1. create directories
    os.mkdir(os.path.join(path, pkg_name))
    
    path_layers = {
        'sandbox':[], 'test_case':['fig','output']}
    
    for lv1_key, item in path_layers.items():
        print(os.path.join(path, pkg_name, lv1_key))
        os.mkdir(os.path.join(path, pkg_name, lv1_key))
        if len(item) > 0:
            for lv2_key in item:
                print(os.path.join(path, pkg_name, lv1_key, lv2_key))
                os.mkdir(os.path.join(path, pkg_name, lv1_key, lv2_key))

    # 2. copy pkg files
    zip_name='pkg.zip'
    # Get the path to the pkg.zip file in the magicreator package
    data_zip_path =pkg_resources.path('magicreator', zip_name).__enter__() 
    
    # Specify the directory to which you want to copy the data.zip file
    target_dir = os.path.join(path, pkg_name)
    
    # Copy the data.zip file to the target directory
    shutil.copy(data_zip_path,os.path.join(target_dir, zip_name))
    
    # Unzip the data.zip file in the target directory
    with zipfile.ZipFile(os.path.join(target_dir, zip_name), 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    
    os.remove(os.path.join(target_dir, zip_name))
    os.rename(
        os.path.join(target_dir, 'repo'), os.path.join(target_dir, pkg_name))

def main():
    
    # Create the parser object
    parser = argparse.ArgumentParser(description='Give a package name.')
    # Add the argument for the file path
    parser.add_argument(
        'pkg_path', metavar='path', nargs='?', default='mickey', 
        type=str, help='the path of the package')

    # Parse the arguments from the command line
    args = parser.parse_args()
    create_pkg(args.pkg_path)
