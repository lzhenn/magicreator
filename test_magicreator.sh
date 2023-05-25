pip uninstall magicreator
rm -rf build dist *egg-info
cd magicreator/data
zip -rDX pkg.zip *
cd ../../
python setup.py sdist
pip install .
cd ..
rm -rf mickey
magicreator
