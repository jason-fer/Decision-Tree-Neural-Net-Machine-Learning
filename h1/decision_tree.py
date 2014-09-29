import unittest, helpers, math

homogenous_check = helpers.homogenous_check
get_class_counts = helpers.get_class_counts

# ***************** DECISION TREE NODE *****************
class Node(object):
	"""Numeric, Nominal, or Class decision tree node (with a list of results)"""
	def __init__(self, feature, value, info_gain, data, pos, neg):
		self.feature = feature
		self.value = value
		self.info_gain = info_gain
		# number of neg / pos classes with this attribute
		self.pos_count = pos
		self.neg_count = neg
		self.data = data
		self.children = []

	def get_type(self):
		return 'generic node'

	def is_leaf(self):
		return self.children == []

class NumericNode(Node):
	"""Numeric decision tree node"""
	def get_type(self):
		return 'nominal node'

	def __repr__(self):
		# thal = fixed_defect [4 6]
		value = round(self.value, 6)
		obj_string = ' %s = %s' % (str(self.feature), str(value))
		obj_string += ' [%s %s]' % (str(self.neg_count), str(self.pos_count))

		if self.is_leaf:
			if self.pos_count > self.neg_count:
				obj_string += ': positive'
			elif self.pos_count <= self.neg_count:
				obj_string += ': negative'
		else:
			pass

		return obj_string

class NominalNode(Node):
	"""Nominal decision tree node"""
	def get_type(self):
		return 'numeric node'

	def __repr__(self):
		# thal = fixed_defect [4 6]
		obj_string = ' %s = %s' % (str(self.feature), str(self.value))
		obj_string += ' [%s %s]' % (str(self.neg_count), str(self.pos_count))
		return obj_string

# ******************** DECISION TREE ********************
class DecisionTree(object):
	"""Machine Learning Decision Tree Structure"""
	def __init__(self):
		self.root = []

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

	def get_branch_sizes(self):
		left, right = self.get_branches()
		return [len(left), len(right)]

	def get_num_instances(self):
		branch_sizes = split.get_branch_sizes()
		total_size = 0
		for b in branch_sizes:
			total_size += b

		return total_size

	def get_type(self):
		return 'numeric split'

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

	def get_branch_sizes(self):
		branches = self.get_branches()
		sizes = []

		for b in branches:
			instance = branches[b].get('instances')
			sizes.append(len(instance))

		return sizes

	def get_num_instances(self):
		branch_sizes = split.get_branch_sizes()
		total_size = 0
		for b in branch_sizes:
			total_size += b

		return total_size

	def get_type(self):
		return 'nominal split'

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

	def no_info_gain(self): # (incomplete)
		# if any candidate has any information gain, then this is false.
		# this is true if not a single feature has info gain
		return False

	def entropy_calc(self, data, nlabel, plabel):
		total_size = len(data)
		p_count, n_count = get_class_counts(data, nlabel, plabel)
		# proportion 1
		p1 = float(p_count) / total_size
		# proportion 2
		p2 = float(n_count) / total_size

		if p1 != 0:
			proportion1 = - (p1 * math.log(p1, 2))
		else:
			proportion1 = 0

		if p2 != 0:
			proportion2 = - (p2 * math.log(p2, 2))
		else:
			proportion2 = 0

		# if entropy is greater than 1 or less than 0, we have an issue
		entropy = proportion1 + proportion2

		if entropy < 0 or entropy > 1:
			raise ValueError('Entropy was: ' + str(entropy) + ' (impossible)')
		else:
			return entropy

	def get_entropy(self, data, split, attributes):
		class_labels = attributes.get('class').get('options')
		# the negative label is always first
		nlabel = class_labels[0]
		plabel = class_labels[1]

		# ********************  get parent entropy  ********************
		parent_entropy = self.entropy_calc(data, nlabel, plabel)
		parent_size = len(data)

		# ********************  get children entropy  ********************
		child_entropies = 0
		branches = split.get_branches()
		for b in branches:
			if split.get_type() == 'nominal split':
				instances = branches[b].get('instances')
			else: # numeric split
				instances = b

			# prevent divide by zero error
			if len(instances) == 0: 
				continue #do nothing if we have no data
			else:
				pass

			child_entropy = self.entropy_calc(instances, nlabel, plabel)

			child_size = len(instances)
			# sanity check
			if child_size > parent_size:
				msg = '[c:' + str(child_size) + ', p:' + str(parent_size) + '] '
				raise ValueError(msg + 'child size > parent size (impossible)')
			else:
				pass
			
			# weight the new entropy by the size of the split
			parnt_chld_ratio = float(child_size) / float(parent_size)
			# update the sum of the weighted child entropies
			child_entropies +=  parnt_chld_ratio * child_entropy

		return parent_entropy, child_entropies

	def info_gain(self, data, split, attributes):
		# determine the info gain in the current split
		parent_entropy, children_entropy = self.get_entropy(data, split, attributes)

		# split: Nominal( slope [up 90, flat 93, down 17] )
		# split: Numeric( trestbps <= 132.315 [115 85], REAL )
		info_gain = parent_entropy - children_entropy

		# sanity check
		if info_gain < 0 or info_gain > 1:
			msg = 'info gain was: ' + str(info_gain) + '... (impossible)!!!'
			raise ValueError(msg)
		else:
			pass

		# print 'split gain:' + str(info_gain)
		return info_gain

	def find_best_split(self, data, attributes):
		maxgain = -1
		nominal = self.get_nominal_splits()
		numeric = self.get_numeric_splits()
		best_split = None

		for split in nominal:
			gain = self.info_gain(data, nominal[split], attributes)

			if gain > maxgain:
				maxgain = gain
				# best_split dict
				best_split = format_best_split(nominal[split], gain)
			elif gain > 0 and gain == maxgain:
				curr_feature = nominal[split]
				prev_feature = best_split.get('split')
				best_split = info_tiebreaker(curr_feature, prev_feature, gain)

		for split in numeric:
			gain = self.info_gain(data, numeric[split], attributes)

			if gain > maxgain:
				maxgain = gain
				# best_split dict
				best_split = format_best_split(numeric[split], gain)
			elif gain > 0 and gain == maxgain:
				curr_feature = numeric[split]
				prev_feature = best_split.get('split')
				best_split = info_tiebreaker(curr_feature, prev_feature, gain)

		# print 'max gain: ' +str(best_split)
		return best_split

# ***************** CANDIDATE SPLITS HELPER METHODS *****************

# (incomplete!!)  need to finish the tiebreaker feature
def info_tiebreaker(curr_feature, prev_feature, gain):
	curr_type = curr_feature.get_type()
	prev_type = prev_feature.get_type()

	numeric = 'numeric split'
	nominal = 'nominal split'

	if curr_type == 'numeric split' and prev_type == 'numeric split':
		# if both are numeric, lowest value wins
		if curr_feature.threshold == prev_feature.threshold:
			# both are equal; resolve with the ARFF order
			pass
		elif curr_feature.threshold < prev_feature.threshold:
			return format_best_split(curr_feature, gain)
		else:
			return format_best_split(prev_feature, gain)
	else:
		pass

	# if we got here, lower ARFF index wins!
	curr_index = curr_feature.feature.get('index')
	prev_index = prev_feature.feature.get('index')

	if curr_index == prev_index:
		# this should never happen
		raise ValueError('curr_index can\'t be equal to prev index!!!!!!')
	if curr_index < prev_index:
		return format_best_split(curr_feature, gain)
	else:
		return format_best_split(prev_feature, gain)

def format_best_split(split, gain):

	best_split = {
		'name':split.name, 
		'split':split,
		'info_gain': gain,
		}

	return best_split

def determine_candidate_splits(data, attributes):
	"""Determine all possible candidate splits"""
	num_items = len(data)
	a = attributes

	numeric = {}
	nominal = {}

	for attr in attributes:
		feature = attributes.get(attr)

		if feature.get('type') == 'numeric':
			numeric[attr] = numeric_candidate_splits(data, feature, num_items, a)
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


def numeric_candidate_splits(data, feature, num_items, attributes):
	"""splits on numeric features use a threshold"""
	"""sort data by feature value asc"""

	index = feature.get('index')
	sorted_data = sorted(data, key=lambda x: x[index])

	if len(sorted_data) != len(data):
		raise ValueError('We lost data while sorting!!!!!!!!')
	else:
		pass

	# split data based on class
	neg_list = []
	pos_list = []

	class_labels = attributes.get('class').get('options')
	negative = class_labels[0]
	positive = class_labels[1]

	for row in data:
		if row[-1] == negative:
			neg_list.append(row)
		elif row[-1] == positive:
			pos_list.append(row)
		else:
			# this should never happen
			raise ValueError('Class label mismatches or some ARFF issue....')

	if len(neg_list) + len(pos_list) != len(data):
			raise ValueError('len(neg_list) + len(pos_list) != len(data):')
	else:
		pass

	neg_sum = sum(row[index] for row in neg_list)
	pos_sum = sum(row[index] for row in pos_list)

	# initialize our branches & threshold (midpoint)
	if len(neg_list) == 0:
		neg_threshold = 0
	else:
		neg_threshold = float(neg_sum) / float(len(neg_list))

	if len(pos_list) == 0:
		pos_threshold = 0
	else:
		pos_threshold = float(pos_sum) / float(len(pos_list))
	

	# use the midpoint / average threshold
	threshold = (neg_threshold + pos_threshold) / 2

	name = feature.get('name')
	if name == 'ca':
		print 'feature'
		print feature
		print 'data' #data CANT be 200........ ug.......
		print len(data)
		print 'neg_threshold'
		print neg_threshold
		print 'pos_threshold'
		print pos_threshold
		print 'threshold'
		print threshold
		exit(0)
	else:
		pass

	left_branch = []
	right_branch = []
	# split the data-sets based on the threshold we found (midpoint)
	for instance in data:
		if instance[index] < threshold:
			left_branch.append(instance)
		else:
			right_branch.append(instance)

	return NumericCandidateSplit(feature, left_branch, right_branch, threshold)

