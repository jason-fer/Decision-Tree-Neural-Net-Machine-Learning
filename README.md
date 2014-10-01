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

python dt-learn.py examples/diabetes_train.arff examples/diabetes_test.arff 4
python dt-learn.py examples/heart_train.arff examples/heart_test.arff 4



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



Project 1 Notes:
-------------------------------------------------------------
-Each function runs a specific part of the algorithm
-Unit test each function to be sure it runs correctly
-Think about possible edge cases already brought up in class -- at least test those
-Figure out additional test cases that need to be considered


PLAN:
1-figure out complete algorithm that I'll run in pseudo-code
2-apply each part of the algorithm, and as I apply each part, create a corresponding unit test that will confirm that part is accurate


-ARFF reads like a database schema & table (very similar)

@relation <relation-name> == like a table name

 @attribute <attribute-name> <datatype> == like columns

 The <datatype> can be any of the four types supported by Weka:
1-numeric
2-integer is treated as numeric
3-real is treated as numeric

<nominal-specification>
string
date [<date-format>]
relational for multi-instance data (for future use)
where <nominal-specification> and <date-format> are defined below. The keywords numeric, real, integer, string and date are case insensitive.

--this homework seems very specific (it doesnt seem I need to think much out of the box other than how i apply the equations)

--use this as a chance to internalize important equations.