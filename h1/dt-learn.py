from lib import arff
import sys

# ********************************** PART 1 ********************************** 

# Assumptions:
# (i) the class attribute is binary, 
# (ii) it is named 'class', and 
# (iii) it is the last attribute listed in the header section.

# Decision-Learner Guidelines:
# 1-Candidate splits for nominal features should have one branch per value of 
# the nominal feature. Branches order matches the order of feature values listed
# in the ARFF file.
# 2-Candidate splits for numeric features should use thresholds that are 
# midpoints betweeen values in the given set of instances. The left branch of 
# such a split should represent values that are less than or equal to the 
# threshold.
# 3-Chose splits based on information gain. If feature have equal information
# gain break the tie in favor of the feature listed first in the header section 
# of the ARFF file. If there is a numeric threshold tie choose smaller threshold.
# 4-Stopping criteria (for making a node into a leaf): (OR)
# (i) all of the training instances reaching the node belong to the same class, 
# (ii) there are fewer than m training instances reaching the node, where m is 
# provided as input to the program, or 
# (iii) no feature has positive information gain, or 
# (iv) there are no more features to split on.
# 5-If the classes of the training instances reaching a leaf are equally 
# represented, the leaf should predict the first class listed in the ARFF file.


# Output: print the tree learned from the training set and its predictions for 
# the test-set instances. For each instance in the test set, print one line of 
# output with spaces separating the fields. Each output line should list the 
# predicted class label, and actual class label. This will be followed by a line
# listing the number of correctly classified test instances, and the total 
# number of instances in the test set.
# 
# optional: print the # of training instances of each class after each node.

# usage dt-learn <train-set-file> <test-set-file> m
# usage python dt-learn.py $1 $2 $3
def main(args):

  # class arff.ArffDecoder
  # decode(s)

  fp = open('./examples/diabetes_test.arff')
  # fp = open('examples/diabetes_test.arff'
  # fp = open('examples/heart_train.arff'
  # fp = open('examples/heart_test.arff'
  data = arff.load(fp)

  if data:
    print data
  else:
    print 'Error. Couldn\'t read file input'

if __name__ == "__main__":
  main(sys.argv)


