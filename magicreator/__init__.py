import os, re, datetime
import shutil, zipfile, argparse
import pkg_resources


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
    data_zip_path =pkg_resources.resource_filename(
        'magicreator', os.path.join('data',zip_name))
    
    # Specify the directory to which you want to copy the data.zip file
    target_dir = os.path.join(path, pkg_name)
    
    # Copy the data.zip file to the target directory
    shutil.copy2(data_zip_path,os.path.join(target_dir, zip_name))
    
    # ---------- Main manupulation ----------
    # Unzip the data.zip file in the target directory
    with zipfile.ZipFile(os.path.join(target_dir, zip_name), 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    os.remove(os.path.join(target_dir, zip_name))

    # rename
    os.rename(
        os.path.join(target_dir, 'repo'), os.path.join(target_dir, pkg_name))
    os.rename(
        os.path.join(target_dir, 'gitignore'), 
        os.path.join(target_dir, '.gitignore'))
    
    # ---------- Replace the package name in text----------
    # Define the file types to search for
    file_types = ['.py', '.md','.ini']
    REPO_WILDCARDS = {
        'REPO_NAME':pkg_name, 
        'DATE_STR':datetime.datetime.now().strftime('%b %d, %Y')}

    for wildcard, aim_value in REPO_WILDCARDS.items():
        # Define the regular expression pattern to search for
        pattern = re.compile(wildcard)

        # Traverse the directory recursively and replace the package name in matching files
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if any(file.endswith(file_type) for file_type in file_types):
                    print(file)
                    file_path = os.path.join(root, file)
                    _replace_pkg_name(file_path, pattern, aim_value)

# Define a function to replace the pattern with the package name
def _replace_pkg_name(file_path, pattern, pkg_name):
    with open(file_path, 'r') as file:
        content = file.read()
    content = re.sub(pattern, pkg_name, content)
    with open(file_path, 'w') as file:
        file.write(content)


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
