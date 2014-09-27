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


# LECTURE ALGORITHMS:
# MakeSubtree(set of training instances D) 
# 	C = DetermineCandidateSplits(D) 
# 	if stopping criteria met 
# 		make a leaf node N
# 		determine class label/probabilities for N
# 	else 
# 		make an internal node N
# 		S = FindBestSplit(D, C) 
# 		for each outcome k of S
# 			Dk = subset of instances that have outcome k
# 			kth child of N = MakeSubtree(Dk) 
# 	return subtree rooted at N


# -splits on nominal features have one branch per value 
# -splits on numeric features use a threshold 

# Numeric candidate splits:
# -given a set of training instances D and a specific feature Xi
# -sort the values of Xi in D
# -evaluate split thresholds in intervals between instances of 
# different classes 
# -could use midpoint of each considered interval as the threshold
# -C4.5 instead picks the largest value of Xi in the entire training set that 
# does not exceed the midpoint


# // Run this subroutine for each numeric feature at each node of DT induction 
# DetermineCandidateNumericSplits(set of training instances D, feature Xi) 
# 	C = {} // initialize set of candidate splits for feature Xi
# 	S = partition instances in D into sets s1 ... sV where the instances in each
# 		set have the same value for Xi
# 	let vj denote the value of Xi for set sj
# 	sort the sets in S using vj as the key for each sj

# 	for each pair of adjacent sets sj, sj+1 in sorted S
# 		if sj and sj+1 contain a pair of instances with different class labels
# 			// assume were using midpoints for splits 
# 			add candidate split Xi ≤ (vj + vj+1)/2 to C
# 	return C


# OrdinaryFindBestSplit(set of training instances D, set of candidate splits C) 
# 	maxgain = -∞!
# 	for each split S in C
# 		gain = InfoGain(D, S) 
# 		if gain > maxgain
# 			maxgain = gain
# 			Sbest = S

# 	return Sbest

# LookaheadFindBestSplit(set of training instances D, set of candidate splits C) 
# 	maxgain = -∞!
# 	for each split S in C
# 		gain = EvaluateSplit(D, C, S) 
# 		if gain > maxgain
# 			maxgain = gain
# 			Sbest = S
# 	return Sbest

# EvaluateSplit(D, C, S)
# 	if a split on S separates instances by class (i.e. ) HD (Y | S) = 0
# 		// no need to split further 
# 		return H_D(Y) − H_D(Y | S)
# 	else 
# 		for outcomes k ∈{1, 2} of S // let’s assume binary splits
# 			// see what the splits at the next level would be
# 			Dk = subset of instances that have outcome k
# 			Sk = OrdinaryFindBestSplit(Dk, C – S) 
# 			// return information gain that would result from this 2-level subtree
# 		return HD(Y) − HD(Y | S,S1,S2)


# LECTURE EQUATIONS:
# 1-entropy equation (one for nominal, one for boolean)
# 2-conditional entropy? (do i need it?)
# 3-information gain
# 4-if info gain is better than average, use gain ratio



# Output: print the tree learned from the training set and its predictions for 
# the test-set instances. For each instance in the test set, print one line of 
# output with spaces separating the fields. Each output line should list the 
# predicted class label, and actual class label. This will be followed by a line
# listing the number of correctly classified test instances, and the total 
# number of instances in the test set.
# 
# optional: print the # of training instances of each class after each node.


def load_data(path = None):
	if not path:
		fp = open('examples/heart_test.arff')
		# fp = open('examples/heart_train.arff')
		# fp = open('./examples/diabetes_test.arff')
		# fp = open('examples/diabetes_test.arff')
	else:
		fp = open(path)
		
	data = arff.load(fp)
	return data;


def dump_attributes(data):
	attributes = data['attributes']
	# attribute types: NUMERIC, REAL, INTEGER, STRING, and NOMINAL
	#  NUMERIC, REAL, INTEGER == convert to int
	# list == NOMINAL
	for key in attributes:
		if type(key[0]) is unicode and type(key[1]) is unicode:
			print "name: " + key[0] + ", type: " + key[1]
		if type(key[0]) is unicode and type(key[1]) is list:
			options = ''
			count = False
			curr_list = key[1]
			for opt in curr_list:
				if not count:
					options += opt
				else:
					options += ", " + opt
				count = True
			if key[0] == 'class':
			 print 'found class!' 
			else:
			  pass
			print "name: " + key[0] + ", nominal: " + options
		# if type([]) is list -- list is array
		# if type({}) is dict -- dict is object
		# if type('') is str or unicode
		# if type(0) is int


# usage dt-learn <train-set-file> <test-set-file> m
# where m is the number of training instances; used in stopping criteria
# usage python dt-learn.py $1 $2 $3
def main(args):
	# class arff.ArffDecoder
	# decode(s)
	data = load_data('')
	dump_attributes(data)



	if data:
		pass # print data['attributes']
	else:
		print 'Error. Couldn\'t read file input'

if __name__ == "__main__":
	main(sys.argv)


