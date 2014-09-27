from lib import arff 
import sys, decision_tree, helpers, math

#helpers
dump_attributes = helpers.dump_attributes
load_data = helpers.load_data
dump_splits = helpers.dump_splits
homogenous_check = helpers.homogenous_check
get_attributes = helpers.get_attributes

#d-tree structs
DecisionTree = decision_tree.DecisionTree
CandidateSplits = decision_tree.CandidateSplits
NumericCandidateSplit = decision_tree.NumericCandidateSplit
NominalCandidateSplit = decision_tree.NominalCandidateSplit
Node = decision_tree.Node

def determine_candidate_splits(data, attributes):
	"""Determine all possible candidate splits"""
	num_items = len(data)

	numeric = {}
	nominal = {}

	for attr in attributes:
		feature = attributes.get(attr)

		if feature.get('type') == 'numeric':
			numeric[attr] = numeric_candidate_splits(data, feature, num_items)
		elif feature.get('type') == 'nominal':
			nominal[attr] = nominal_candidate_splits(data, feature, num_items)
			pass
		else:
			# the class variable
			pass

	# delete all splits that have no instances (incomplete)
	# clean splits!!!!!!!!!!!!
	# dump_splits(splits) # debug
	return CandidateSplits(numeric, nominal)


def nominal_candidate_splits(data, feature, num_items):
	"""splits on nominal features have one branch per value"""
	index = feature.get('index')
	branches = {}

	count = 0
	# one branch per option in the feature vector
	# order must match the attribute order in ARFF file
	for branch_name in feature.get('options'):
		# the branch_name is the option name
		branches[branch_name] = {
			'option':branch_name, 
			'index':count, # tells us the order from the ARFF file
			'instances':[] 
			}
		count = count + 1

	# match each instance with the right respective branch
	for instance in data:
		branch_name = instance[index]
		branches[branch_name].get('instances').append(instance)

	return NominalCandidateSplit(feature, branches)


def numeric_candidate_splits(data, feature, num_items):
	"""splits on numeric features use a threshold"""
	"""sort data by feature value asc"""
	index = feature.get('index')
	sorted_data = sorted(data, key=lambda x: x[index])
	grand_total = sum(row[index] for row in sorted_data)

	# initialize our branches & threshold (midpoint)
	threshold = grand_total / num_items; #is my midpoint incorrect? (incomplete??)
	left_branch = []
	right_branch = []

	# split the data-sets based on the threshold (midpoint)
	for instance in data:
		if instance[index] < threshold:
			left_branch.append(instance)
		else:
			right_branch.append(instance)

	return NumericCandidateSplit(feature, left_branch, right_branch, threshold)

def stopping_criteria_is_met(candidates):
	# The stopping criteria (for making a node into a leaf) are that (i) all of the training instances reaching the node belong to the same class, or (ii) there are fewer than m training instances reaching the node, where m is provided as input to the program, or (iii) no feature has positive information gain, or (iv) there are no more remaining candidate splits at the node.
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

def make_subtree(data, attributes):
 candidates = determine_candidate_splits(data, attributes)

 # candidates.test_split_counts(data) #debug
 # if stopping_criteria_is_met(candidates):
 #   # determine class label/probabilities for N
 #   # use that to build the leaf node
 #   node = Node('attribute', 'value')
 # else:
 #   # make an internal node N
 #   node = Node('attribute', 'value')
 #   splits = find_best_split(data, candidates) 
 #   # for each outcome k of splits
 #   for outcome in splits:
 #     # subset_of_data = subset of instances that have outcome k
 #     subset_of_data = data_subset(data, outcome)
 #     # kth child of N = make_subtree(Dk) 
 #     node.children.add = make_subtree(Dk) 
 # return node


# Splits should be chosen using information gain. If there is a tie between two features in their information gain, you should break the tie in favor of the feature listed first in the header section of the ARFF file. If there is a tie between two different thresholds for a numeric feature, you should break the tie in favor of the smaller threshold.
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
	attributes = get_attributes(arff_file['attributes'])
	class_labels = attributes.get('class').get('options')
	data = arff_file['data']

	# homogenous check (incomplete)
	dtree = DecisionTree()
	is_homogenous, result = homogenous_check(data, class_labels[0], class_labels[1]);
	if result != None:
		# need to produce a single node tree
		dtree.root = Node('class', result)
	else:
		pass

	# check to see if predicting attributes are empty (incomplete)
	# ?? dtree.root = Node('class', result)

	# Top-down decision tree build (incomplete)
	dtree.root = make_subtree(data, attributes)

	# Output results (incomplete)


if __name__ == "__main__":
	main(sys.argv)


