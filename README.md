cs760-homework
==============

heart_train:
m = 20 --- passed
m = 10 --- passed
m = 4  --- passed
m = 2  --- passed

diabetes_train:
m = 20 --- passed
m = 10 --- passed
m = 4
m = 2



http://stackoverflow.com/questions/2915471/install-a-python-package-into-a-different-directory-using-pip

pip install --install-option="--prefix=$PREFIX_PATH" package_name

You might also want to use --ignore-installed to force all dependencies to be reinstalled using this new prefix. 

pip install --install-option="--prefix=/Users/jason/Sites/cs760/cs760-homework/h1/scripts"  arff --ignore-installed


~/Sites/cs760/cs760-homework/h1


Non ASCII characters:
[^\x00-\x7F]

Luckily in Python 2.6 you can execute directories directly. Much like executing packages, if a directory contains a __main__.py file next to the application's package then Python can run it: python /dir/to/oplop. That means you can simply toss the application code somewhere and alias the application name to the execution of Python with the directory location passed to it (this is actually how I handle executing Oplop myself since it means I can have it always point to my Hg branch).

Emacs Speaks Statistics (ESS) is an add-on package for emacs text editors such as GNU Emacs and XEmacs

pip install --install-option="–install-scripts=/Users/jason/Sites/cs760/cs760-homework/h1/scripts"  arff --ignore-installed

--install-option install-scripts=/usr/local/bin

pip install arff -–install-option="–install-scripts=./scripts"

-1/2 slope


