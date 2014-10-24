cs760-homework
==============

Homework 2:
-how do i test this / how do i confirm my algorithm is correct

Prof Kraven's advice:
keep track of each epoch & make sure error gets smaller & smaller
learning rate must be small enough to converge -- (i could overshoot)
keep learning rate fixed... (rate he told us will work)

-Neural Networks Pt1: 
ask about "del"E(w) = [dE/dW0, dE/dW1, ....]  <-- is this a weight vector??
change in weight w_i = -n dE/dW_i  <--partial derivative of error w/ respect to the current weight
-n = learning rate

-Neural Networks Pt2: 
ask about W_ij = -n dE/dW_ij
(ask TA to explain the math in these slides)

convolutional neural networks " aiming to build web services that can do things like automatically understand natural language and recognize images."

Distributed systems question:
what is the fancy L we saw?

what is a 'rich hypothesis space'???

regression analysis helps one understand how the typical value of the dependent variable (or 'criterion variable') changes when any one of the independent variables is varied, while the other independent variables are held fixed. 

Receiver Operating Characteristic (ROC) curve plots the TP-rate vs. the FP-rate as 
a threshold on the confidence of an instance being positive is varied


gradient descent... huh? (error vector or what???)
sideways is still considered feed-forward
feed forward = does not have cycles


d/dx[ f(x) g(x) ] = d/dx [ f`(x)g(x) + f(x) g`(x) ] = f`(x)(g(x))^-1 + f(x)(-1)(g(x)^-2 g`(x)

= f`(x)/g(x) - f(x) g`(x) / g(x)^2
= [ f`(x) g(x) - f(x) g`(x) ] / g(x)^2



Homework1:
where p(xi,yj) is the probability that X=xi and Y=yj. This quantity should be understood as the amount of randomness in the random variable X given that you know the value of Y.

conditional entropy (of two events X & Y both taking x_i and y_j values respectively): 
H(X|Y) = 

If H(Y|X=x) is the entropy of the variable Y conditioned on the variable X taking a certain value x, then H(Y|X) is the result of averaging H(Y|X=x) over all possible values x that X may take.


Entropy of Y; H(Y) = for all Y, += - (py)log_2(py)

What is the conditional entropy of Y if we condition on some other variable X?
H(Y|X) = for all x, p(X=x) * H(Y|X=x)
H(Y|X=x) = for all y P(Y=x|X=x)* log_2 P(Y=y|X=x)


heart_train:
m = 20 --- passed
m = 10 --- passed
m = 4  --- passed
m = 2  --- passed

diabetes_train:
m = 20 --- passed
m = 10 --- passed
m = 4  --- passed
m = 2  --- passed

ticetactoe (secret test):
passed 100% also.

python dt-learn.py examples/diabetes_train.arff examples/diabetes_test.arff 4
python dt-learn.py examples/heart_train.arff examples/heart_test.arff 2

python dt-learn.py examples/tictactoe_train.arff examples/tictactoe_test.arff 2

python dt-learn.py  /u/f/e/feriante/private/cs760/examples/tictactoe_train.arff /u/f/e/feriante/private/cs760/examples/tictactoe_test.arff 2

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