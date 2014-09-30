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

def stopping_criteria_is_met(candidates, data, m, attributes, best_split):
	info_gain = best_split.get('info_gain')
	candidate_count = len(data)
	is_homogenous, class_label = candidates.is_homogenous(data, attributes)

	# stop if:
	# 1. candidates all have the same class
	if is_homogenous:
		return True, class_label # so we know what the result was
	# 2. there are fewer than m training instances reaching the node
	elif candidate_count == 0:
		return True, False
	# 3. no feature has positive information gain
	elif info_gain == 0:
		return True, False
	# 4. or candidates is empty
	elif candidate_count < m:
		return True, False
	else:
		# Stopping criterian wasn't met
		return False, False

def numeric_data_count(data, left, right, attributes):
	class_labels = attributes.get('class').get('options')
	lp_count, ln_count = get_class_counts(left, class_labels[0], class_labels[1])
	rp_count, rn_count = get_class_counts(right, class_labels[0], class_labels[1])

	if len(data) != (lp_count + ln_count + rp_count + rn_count):
		raise ValueError('subset instance count doesnt match neg / pos count')
	else:
		return lp_count, ln_count, rp_count, rn_count

def nominal_data_split(data, feature_info, value, attributes):
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

# it's critical that this function actually splits up the data
def generate_nodes(data, split, attributes):
	# use the data to generate a node for best split
	# name, attribute, value, neg_count, pos_count, data
	nodes = [] # either left, then right or a list

	# split on this feature
	feature = split.get('name') # name of attribute
	feature_options = attributes.get(feature).get('options')
	feature_info = attributes.get(feature)
	info_gain = split.get('info_gain')
	# get the internal split class (inside the current dict)
	split = split.get('split')
	split_type = split.get_type()

	if split_type == 'nominal split': # decision_tree.NominalCandidateSplit
		for value in feature_options:
			subset, p, n = nominal_data_split(data, feature_info, value, attributes)

			# subset size, sanity check
			if len(subset) == len(data):
				raise ValueError('A subset must be smaller than the parent')
			else:
				pass

			# nothing to do if there's nothing in the subset
			if len(subset) != 0:
				# print 'nominal node created! :' + str(value) + ', size: ' + str(len(subset))
				nodes.append(NominalNode(feature, value, info_gain, subset, p, n))
			else:
				pass
	else: # 'numeric split' decision_tree.NumericCandidateSplit
			# smaller value first
			left = split.left_branch
			right = split.right_branch
			value = split.threshold

			lp, ln, rp, rn = numeric_data_count(data, left, right, attributes)
			# nothing to do if there's nothing in the subset
			if len(left) != 0:
				t = split.get_thresh_def()
				numeric_node = NumericNode(feature, value, info_gain, left, lp, ln, t)
				nodes.append(numeric_node)
			else:
				pass

			if len(right) != 0:
				t = split.get_thresh_def()
				numeric_node = NumericNode(feature, value, info_gain, right, rp, rn, t)
				nodes.append(numeric_node)
			else:
				pass

	return nodes

def make_subtree(data, attributes, m):
	candidates = determine_candidate_splits(data, attributes)
	best_split = candidates.find_best_split(data, attributes)
	nodes = []
	# candidates.test_split_counts(data) #debug
	stop_now, class_label = stopping_criteria_is_met(candidates, data, m, attributes, best_split)
	if stop_now: # leaf-node
		return []
		# determine class label/probabilities for N
		# node = Node('attribute', 'value') ?
		pass
	else:
		nodes = generate_nodes(data, best_split, attributes)
		for n in nodes:
			# find the children for each node, & set m = m - 1 (to terminate)
			if len(n.data) == len(data):
				raise ValueError('why is subset length == superset length??')
			else:
				pass
			n.children = make_subtree(n.data, attributes, m - 1)

	return nodes

def print_decision_tree(dtree, data, attributes):
	# If the classes of the training instances reaching a leaf are equally represented, 
	# the leaf should predict the first class listed in the ARFF file.
	# print ''
	for node in dtree.root:
		node_print(node, 0)
		
def node_print(node, depth):
	if node == []:
		pass
		#empty node
	else:
		prepend = ''
		spacer = '|       '
		for x in range(depth):
			prepend += spacer

		print prepend + str(node)

		count = 0
		for n in node.children:
			# if n == 0 and type is numeric node, it's negative
			# if n == 1 and '' 				'' 					it's positive
			node_print(n, depth + 1)


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


	# Top-down decision tree build
	dtree = DecisionTree()
	# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx fix stopping criteria!!!!!!
	# dtree.root = make_subtree(data, attributes, m + 10)
	dtree.root = make_subtree(data, attributes, m)

	# Output results
	print_decision_tree(dtree, data, attributes)	


if __name__ == "__main__":
	main(sys.argv)


