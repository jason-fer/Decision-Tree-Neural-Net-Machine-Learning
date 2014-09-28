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
determine_candidate_splits = decision_tree.determine_candidate_splits
NumericNode = decision_tree.NumericNode
NominalNode = decision_tree.NominalNode

def stopping_criteria_is_met(candidates, data, m, attributes):
	# stop if:
	candidate_count = len(data)
	# 1. candidates all have the same class
	is_homogenous, result = candidates.is_homogenous(data, attributes)
	if is_homogenous:
		print candidate_count
		return True, result
	# 2. there are fewer than m training instances reaching the node
	elif candidate_count == 0:
		return True, 0
	# 3. no feature has positive information gain (incomplete)
	elif candidates.no_info_gain():
		return True, 'no_info_gain'
	# 4. or candidates is empty
	elif candidate_count < m:
		return True, 'm'
	else:
		# Stopping criterian wasn't met
		return False, None

def data_subset(data, outcome):
	# list each piece of data in the subset that matches the outcome
	pass
	# return subset_of_data

def make_subtree(data, attributes, m):
	candidates = determine_candidate_splits(data, attributes)

	# candidates.test_split_counts(data) #debug
	stop_now, reason = stopping_criteria_is_met(candidates, data, m, attributes)
	if stop_now: # leaf-node
	#   # determine class label/probabilities for N
	  # node = Node('attribute', 'value')
		pass
	else:
	  # make an internal node N
	  split = candidates.find_best_split(data, attributes)
	  exit(0)
	  print split
		#   node = Node('attribute', 'value')
		#   # for each outcome k of splits
		#   for outcome in splits:
		#     # subset_of_data = subset of instances that have outcome k
		#     subset_of_data = data_subset(data, outcome)
		#     # kth child of N = make_subtree(Dk) 
		#     node.children.add = make_subtree(Dk) 
		# return node


def main(args):
	"""usage dt-learn <train-set-file> <test-set-file> m """
	"""where m is the number of training instances; used in stopping criteria"""
	"""usage python dt-learn.py $1 $2 $3"""

	# stopping criteria m
	m = 20
	# init
	# arff_file = load_data('examples/diabetes_train.arff')
	arff_file = load_data('examples/heart_train.arff')
	attributes = get_attributes(arff_file['attributes'])
	class_labels = attributes.get('class').get('options')
	data = arff_file['data']

	# homogenous check (incomplete)
	dtree = DecisionTree()
	# is_homogenous, result = homogenous_check(data, class_labels[0], class_labels[1]);
	# if result != None:
	# 	# need to produce a single node tree
	# 	dtree.root = Node('class', result)
	# else:
	# 	pass

	# check to see if predicting attributes are empty (incomplete)
	# ?? dtree.root = Node('class', result)

	# Top-down decision tree build (incomplete)
	dtree.root = make_subtree(data, attributes, m)

	# Output results (incomplete)


if __name__ == "__main__":
	main(sys.argv)


