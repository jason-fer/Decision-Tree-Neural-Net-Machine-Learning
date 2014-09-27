from lib import arff 
import sys, decision_tree, helpers, math

dump_attributes = helpers.dump_attributes
load_data = helpers.load_data
homogenous_check = helpers.homogenous_check
DecisionTree = decision_tree.DecisionTree
Node = decision_tree.Node
attributes = None
negative = 'negative'
positive = 'positive'


def determine_candidate_splits(data):
	"""splits on nominal features have one branch per value """
	"""splits on numeric features use a threshold"""
	# Numeric candidate splits:
	# -given a set of training instances D and a specific feature Xi
	# -sort the values of Xi in D
	# -evaluate split thresholds in intervals between instances of 
	# different classes 
	# -could use midpoint of each considered interval as the threshold
	# does not exceed the midpoint

	# DetermineCandidateNumericSplits(set of training instances D, feature Xi) 
	#  C = {} // initialize set of candidate splits for feature Xi
	#  S = partition instances in D into sets s1 ... sV where the instances in each
	#    set have the same value for Xi
	#  let vj denote the value of Xi for set sj
	#  sort the sets in S using vj as the key for each sj

	#  for each pair of adjacent sets sj, sj+1 in sorted S
	#    if sj and sj+1 contain a pair of instances with different class labels
	#      // assume were using midpoints for splits 
	#      add candidate split Xi <= (vj + vj+1)/2 to C
	#  return C
	pass

def stopping_criteria_is_met(candidates):
	# stop if:
	# 1. candidates all have the same class
	# 2. candidates is empty
	if candidates == {}:
		return True
	else:
		pass

	for instance in candidates:
		print candidates
		# if these all have the same class, return True

	return False

def data_subset(data, outcome):
	# list each piece of data in the subset that matches the outcome
	pass
	# return subset_of_data

def make_subtree(data):
 candidates = determine_candidate_splits(data)
 if stopping_criteria_is_met(candidates):
   # determine class label/probabilities for N
   # use that to build the leaf node
   node = Node('attribute', 'value')
 else:
   # make an internal node N
   node = Node('attribute', 'value')
   splits = find_best_split(data, candidates) 
   # for each outcome k of splits
   for outcome in splits:
     # subset_of_data = subset of instances that have outcome k
     subset_of_data = data_subset(data, outcome)
     # kth child of N = make_subtree(Dk) 
     node.children.add = make_subtree(Dk) 
 return node

#  OrdinaryFindBestSplit(set of training instances D, set of candidate splits C) 
def find_best_split(data, candidates):
	pass
	#  maxgain = negative infinity
	#  for each split S in C
	#    gain = InfoGain(D, S) 
	#    if gain > maxgain
	#      maxgain = gain
	#      Sbest = S

	#  return Sbest


# EvaluateSplit(D, C, S)
def evaluate_split(data, candidates, subset):
	pass
	#  if a split on S separates instances by class (i.e. ) HD (Y | S) = 0
	#    // no need to split further 
	#    return H_D(Y) - H_D(Y | S)
	#  else 
	#    for outcomes k in set {1, 2} of S // let's assume binary splits
	#      // see what the splits at the next level would be
	#      Dk = subset of instances that have outcome k
	#      Sk = OrdinaryFindBestSplit(Dk, C - S) 
	#      // return information gain that would result from this 2-level subtree
	#    return HD(Y) - HD(Y | S,S1,S2)


def main(args):
	"""usage dt-learn <train-set-file> <test-set-file> m """
	"""where m is the number of training instances; used in stopping criteria"""
	"""usage python dt-learn.py $1 $2 $3"""
	# init
	# arff_file = load_data('examples/diabetes_train.arff')
	arff_file = load_data('examples/heart_train.arff')
	attributes = arff_file['attributes']
	attr_count = len(attributes)
	data = arff_file['data']
	class_labels = attributes[-1][1]
	negative = class_labels[0]
	positive = class_labels[1]

	dtree = DecisionTree()

	# homogenous check (incomplete)
	is_homogenous, result = homogenous_check(data, class_labels, negative, positive);
	if result != None:
		# need to produce a single node tree
		dtree.root = Node('class', result)
	else:
		pass

	# check to see if predicting attributes are empty (incomplete)
	# ?? dtree.root = Node('class', result)

	# Top-down decision tree build (incomplete)
	dtree.root = make_subtree(data)

	# Output results (incomplete)


if __name__ == "__main__":
	main(sys.argv)


