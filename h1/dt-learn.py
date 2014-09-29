from lib import arff 
import sys, decision_tree, helpers, math

#helpers
dump_attributes = helpers.dump_attributes
load_data = helpers.load_data
dump_splits = helpers.dump_splits
homogenous_check = helpers.homogenous_check
get_attributes = helpers.get_attributes
get_class_counts = helpers.get_class_counts

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

def split_data_on_feature(data, feature_info, value, attributes):
	# value: the current option
	# data: all instances
	# feature_info: from the arf file.
	index = feature_info.get('index')
	subset = []
	for row in data:
		if row[index] == value:
			subset.append(row)
		else:
			pass

	class_labels = attributes.get('class').get('options')
	p_count, n_count = get_class_counts(subset, class_labels[0], class_labels[1])

	if len(subset) != (p_count + n_count):
		raise ValueError('subset instance count doesnt match neg / pos count')
	else:
		return subset, p_count, n_count


def generate_nodes(data, split, attributes):
	# use the data to generate a node for best split
	# name, attribute, value, neg_count, pos_count, data
	nodes = [] # either left, then right or a list

	# split on this feature
	feature = split.get('name') # name of attribute
	feature_options = attributes.get(feature).get('options')
	feature_info = attributes.get(feature)

	print split
	split = split.get('split')
	split_type = split.get_type()

	if split_type == 'nominal split': # decision_tree.NominalCandidateSplit
		for value in feature_options:
			subset, p, n = split_data_on_feature(data, feature_info, value, attributes)
			# nothing to do if there's nothing in the subset
			if len(subset) != 0:
				print 'nominal node created! :' + str(value) + ', size: ' + str(len(subset))
				nodes.append(NominalNode(feature, value, info_gain, data, p, n))
			else:
				pass
	else: # 'numeric split' decision_tree.NumericCandidateSplit
			subset, p, n = split_data_on_feature(data, feature_info, value, attributes)
			# nothing to do if there's nothing in the subset
			if len(subset) != 0:
				print 'numeric node created! :' + str(value) + ', size: ' + str(len(subset))
				nodes.append(NumericNode(feature, value, info_gain, data, p, n))
			else:
				pass

	return nodes

def make_subtree(data, attributes, m):
	candidates = determine_candidate_splits(data, attributes)

	nodes = []
	# candidates.test_split_counts(data) #debug
	stop_now, reason = stopping_criteria_is_met(candidates, data, m, attributes)
	if stop_now: # leaf-node
		return []
		# print 'reason!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		# print reason
		# raise ValueError('stopping function not written')
	  # determine class label/probabilities for N
	  # node = Node('attribute', 'value') ?
		pass
	else:
	  split = candidates.find_best_split(data, attributes)
	  nodes = generate_nodes(data, split, attributes)
	  for n in nodes:
			n.children.append(make_subtree(n.data, attributes, m))

	return nodes


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


