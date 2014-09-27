cs760-homework
==============


http://stackoverflow.com/questions/2915471/install-a-python-package-into-a-different-directory-using-pip

pip install --install-option="--prefix=$PREFIX_PATH" package_name

You might also want to use --ignore-installed to force all dependencies to be reinstalled using this new prefix. 

pip install --install-option="--prefix=/Users/jason/Sites/cs760/cs760-homework/h1/scripts"  arff --ignore-installed


~/Sites/cs760/cs760-homework/h1