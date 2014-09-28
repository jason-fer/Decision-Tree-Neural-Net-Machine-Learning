import unittest, helpers

homogenous_check = helpers.homogenous_check

# ***************** DECISION TREE NODE *****************
class Node(object):
		"""Numeric, Nominal, or Class decision tree node (with a list of results)"""
		def __init__(self, name, attribute, value):
			self.name = name
			self.attribute = attribute
			self.value = value
			self.children = {}

		def is_leaf(self):
			self.children == {}

# ******************** DECISION TREE ********************
class DecisionTree(object):
		"""Machine Learning Decision Tree Structure"""
		def __init__(self):
			self.root = None

		def printTree(self):
			# print the Decision Tree
			pass

# ***************** DECISION TREE NUMERIC SPLITS *****************
class NumericCandidateSplit(object):
	"""Candidate Split Decision Tree Structure"""
	def __init__(self, feature, left_branch, right_branch, threshold):
		self.feature = feature
		self.left_branch = left_branch
		self.right_branch = right_branch
		self.threshold = threshold #aka, midpoint
		self.name = feature.get('name')
		self.options = feature.get('options')

	def __repr__(self):
		# feature: name, index, type, options, e.g.:
		# {'name': thal, index': 5, 'type': 'numeric', 'options': [u't', u'f']}
		obj_string = 'Numeric( ' + str(self.name)
		left = str(len(self.left_branch))
		right = str(len(self.right_branch))
		mid = str(self.threshold)
		opt = str(self.options)
		obj_string += ' <= %s [%s %s], %s )' % (mid, left, right, opt)
		return obj_string

	def get_branches(self):
		return self.left_branch, self.right_branch

# ***************** DECISION TREE NOMINAL SPLITS *****************
class NominalCandidateSplit(object):
	"""Candidate Split Decision Tree Structure"""
	def __init__(self, feature, branches):
		self.feature = feature
		self.branches = branches
		self.name = feature.get('name')
		self.options = feature.get('options')

	def __repr__(self):
		# feature: name, index, type, options, e.g.:
		# {'name': thal, index': 5, 'type': 'numeric', 'options': [u't', u'f']}
		# branches = {'option':branch_name, 'index':count, 'instances':[]}
		feature = self.feature
		obj_string = 'Nominal( ' + str(self.name) + ' ['
		count = 0
		for branch_name in feature.get('options'):
			instance_count = str(len(self.branches.get(branch_name).get('instances')))
			# comma delimit the data
			if count > 0:
				obj_string += ', '
			# append the relevant data for this branch
			obj_string += str(branch_name) + ' ' + instance_count
			count = count + 1
		# for each branch: name instances, (no comma first, prepend rest w/ comma)
		obj_string += '] )'
		return obj_string

	def get_branches(self):
		return self.branches

# ***************** DECISION TREE CANDIATE (ALL) SPLITS *****************
class CandidateSplits(object):
	"""docstring for CandidateSplits"""

	def __init__(self, numeric_candidates, nominal_candidates):
		self.tc = unittest.TestCase('__init__')
		self.numeric_candidates = numeric_candidates
		self.nominal_candidates = nominal_candidates

	# so we can confirm the number of items withint the splits matches the count
	# of data instances
	def test_split_counts(self, data):
		tc = self.tc
		# every split should have the same count as the original data set
		match_count = len(data)

		# check nominal
		nominal = self.nominal_candidates
		for n in nominal:
			branches = nominal[n].get_branches()
			instance_count = 0

			for b in branches:
				instances = branches[b].get('instances')
				instance_count += len(instances)

			tc.assertEqual(instance_count, match_count)

		# check numeric
		numeric = self.numeric_candidates
		for n in numeric:
			left_branch, right_branch = numeric[n].get_branches()

			instance_count = 0
			instance_count += len(left_branch)
			instance_count += len(right_branch)

			tc.assertEqual(instance_count, match_count)

		# all checks passed!
		return True

	# splits should be orderd the same as the ARFF file
	# since dict has no order, i'll just traverse that way.
	def get_nominal_splits(self):
		return self.nominal_candidates

	def get_numeric_splits(self):
		return self.numeric_candidates

	def is_homogenous(self, data, attributes):
		class_labels = attributes.get('class').get('options')
		return homogenous_check(data, class_labels[0], class_labels[1]);

	def no_info_gain(self): # incomplete
		# if any candidate has any information gain, this is false.
		return False



# ***************** CANDIDATE SPLITS HELPER METHODS *****************
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