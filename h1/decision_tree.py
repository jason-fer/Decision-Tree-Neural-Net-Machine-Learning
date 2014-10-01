import unittest, helpers, math
from collections import Counter

homogenous_check = helpers.homogenous_check
get_class_counts = helpers.get_class_counts

# ***************** Entropy / InfoGain *****************
def entropy_calc(data, nlabel, plabel):
	total_size = len(data)
	p_count, n_count = get_class_counts(data, nlabel, plabel)
	# proportion 1
	p1 = float(p_count) / float(total_size)
	# proportion 2
	p2 = float(n_count) / float(total_size)

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

def get_entropy(data, split, attributes):
	class_labels = attributes.get('class').get('options')
	# the negative label is always first
	nlabel = class_labels[0]
	plabel = class_labels[1]

	# ********************  get parent entropy  ********************
	parent_entropy = entropy_calc(data, nlabel, plabel)
	parent_size = len(data)
	# print 'parent_entropy'
	# print parent_entropy
	# print 'parent_size'
	# print parent_size
	# exit(0)

	# ********************  get children entropy  ********************
	child_entropies = 0
	branches = split.get_branches()
	for b in branches:
		if split.get_type() == 'nominal split':
			instances = branches[b].get('instances')
		else: # numeric split
			instances = b

		child_size = len(instances)
		# prevent divide by zero error
		if child_size == 0: 
			continue #do nothing if we have no data
		else:
			pass
		
		child_entropy = entropy_calc(instances, nlabel, plabel)

		# print 'child_entropy'
		# print child_entropy
		# print 'child_size'
		# print child_size
		# exit(0)

		# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
		# feature = split.feature
		# name = feature.get('name')
		# if name == 'ca' and len(data) < 200 and split.threshold > 0:
		# 	print 'split.threshold'
		# 	print split.threshold
		# 	print 'child_size'
		# 	print child_size
		# 	print 'child_entropy'
		# 	print child_entropy
		# else:
		# 	pass
		# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
		# sanity check
		if child_size > parent_size:
			msg = '[c:' + str(child_size) + ', p:' + str(parent_size) + '] '
			raise ValueError(msg + 'child size > parent size (impossible)')
		else:
			pass
		
		# weight the new entropy by the size of the split
		parnt_chld_ratio = float(child_size) / float(parent_size)
		# update the sum of the weighted child entropies
		child_entropies +=  parnt_chld_ratio * float(child_entropy)

	return parent_entropy, child_entropies

def info_gain(data, split, attributes):
	# determine the info gain in the current split
	parent_entropy, children_entropy = get_entropy(data, split, attributes)

	# split: Nominal( slope [up 90, flat 93, down 17] )
	# split: Numeric( trestbps <= 132.315 [115 85], REAL )
	if str(parent_entropy) == str(children_entropy):
		# avoid bizzare edge case
		info_gain = 0
	else:
		info_gain = parent_entropy - children_entropy

	if info_gain < 0 or info_gain > 1:
			# failed sanity check
			msg = 'info gain was: ' + str(info_gain) + '... (impossible)!!!'
			raise ValueError(msg)
	else:
		pass

	# print 'split gain:' + str(info_gain)
	return info_gain

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
		self.thresh_def = {}

	def get_type(self):
		return 'generic node'

	def get_value(self):
		return self.value

	def is_leaf(self):
		return self.children == []

	def get_index(self, attributes):
		index = attributes.get(self.feature).get('index')
		return index

class NumericNode(Node):
	"""Numeric decision tree node"""
	def __init__(self, feature, value, info_gain, data, pos, neg, thresh_def):
		self.feature = feature
		self.value = value
		self.info_gain = info_gain
		# number of neg / pos classes with this attribute
		self.pos_count = pos
		self.neg_count = neg
		self.data = data
		self.thresh_def = thresh_def
		self.children = []

	def test_instance(self, row, attributes):
		# determine which brach this row belongs to
		# numeric; therefore we need left or right
		print 'test_instance() not written yet'
		exit(0)
		pass

	def get_type(self):
		return 'numeric node'

	def get_thresh_def(self):
		return self.thresh_def

	def get_sign(self, attributes):
		threshold = float(self.value)
		class_labels = attributes.get('class').get('options')
		negative = class_labels[0]
		positive = class_labels[1]
		data = self.data

		# we need the index for our counts
		index = attributes.get(self.feature).get('index')

		neg_below = 0
		neg_above = 0
		pos_below = 0
		pos_above = 0

		for row in data:
			# count rows below the threshold
			if row[index] <= threshold:
				if row[-1] == negative:
					neg_below += 1
				else:
					pos_below += 1
			# count rows above the threshold
			else:
				if row[-1] == negative:
					neg_above += 1
				else:
					pos_above += 1

		# LTE or GT threshold?
		above = '>' #  GT
		below = '<=' # LTE

		# this gets confusing because it's all very relative

		# now we can determine the sign
		if self.pos_count > self.neg_count:
			# positive wins, was the majority above or below?
			if pos_above > pos_below:
				sign = above
			else:
				sign = below
		else: # self.pos_count <= self.neg_count:
			# negative wins, was the majority above or below?
			if neg_above > neg_below:
				sign = above
			else:
				sign = below
		
		return sign

	def dt_print(self, is_leaf, attributes):
		class_labels = attributes.get('class').get('options')
		negative = class_labels[0]
		positive = class_labels[1]

		# thal = fixed_defect [4 6]
		value = float(self.value)
		base = ' [%s %s]' % (self.neg_count, self.pos_count)
		sign = self.get_sign(attributes)

		# build string output for this node
		if self.pos_count > self.neg_count:
			obj_string = '%s %s %.6f' % (self.feature, sign, value)
			obj_string += base
			if is_leaf == True:
				obj_string += ': ' + str(positive)
			else:
				pass
		else: #self.pos_count <= self.neg_count: (negative wins)
			obj_string = '%s %s %.6f' % (self.feature, sign, value)
			obj_string += base
			if is_leaf == True:
				obj_string += ': ' + str(negative)
			else:
				pass

		return obj_string

class NominalNode(Node):
	"""Nominal decision tree node"""
	def get_type(self):
		return 'nominal node'

	def dt_print(self, is_leaf, attributes):
		# thal = fixed_defect [4 6]
		# obj_string = '%s = %s' % (self.feature, self.value)
		# obj_string += ' [%s %s]' % (self.neg_count, self.pos_count)
		class_labels = attributes.get('class').get('options')
		negative = class_labels[0]
		positive = class_labels[1]
		
		base = ' [%s %s]' % (self.neg_count, self.pos_count)

		if self.pos_count > self.neg_count:
			obj_string = '%s = %s' % (self.feature, self.value)
			obj_string += base
			if is_leaf == True:
				obj_string += ': ' + str(positive)
			else:
				pass
		elif self.pos_count <= self.neg_count:
			obj_string = '%s = %s' % (self.feature, self.value)
			obj_string += base
			if is_leaf == True:
				obj_string += ': ' + str(negative)
			else:
				pass
		else:
			# negative wins?
			obj_string = '%s = %s' % (self.feature, self.value)
			obj_string += base
			if is_leaf == True:
				obj_string += ': ' + str(negative)
			else:
				pass

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

	def get_branches(self):
		return [self.left_branch, self.right_branch]

	def get_l_r_branches():
		return self.left_branch, self.right_branch

	def get_branch_sizes(self):
		left, right = self.get_l_r_branches()
		return [len(left), len(right)]

	def get_num_instances(self):
		branch_sizes = split.get_branch_sizes()
		total_size = 0
		for b in branch_sizes:
			total_size += b

		return total_size

	def get_thresh_def(self):
		return self.thresh_def

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
			left_branch, right_branch = numeric[n].get_l_r_branches()

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

	def find_best_split(self, data, attributes):
		maxgain = -1
		nominal = self.get_nominal_splits()
		numeric = self.get_numeric_splits()
		best_split = None

		for split in nominal:
			gain = info_gain(data, nominal[split], attributes)

			if gain > maxgain:
				maxgain = gain
				# best_split dict
				best_split = format_best_split(nominal[split], gain)
			elif gain > 0 and gain == maxgain:
				curr_feature = nominal[split]
				prev_feature = best_split.get('split')
				best_split = info_tiebreaker(curr_feature, prev_feature, gain)
			else:
				pass

		for split in numeric:
			gain = info_gain(data, numeric[split], attributes)

			if gain > maxgain:
				maxgain = gain
				# best_split dict
				best_split = format_best_split(numeric[split], gain)
			elif gain > 0 and gain == maxgain:
				curr_feature = numeric[split]
				prev_feature = best_split.get('split')
				best_split = info_tiebreaker(curr_feature, prev_feature, gain)
			else:
				pass

		# print 'max gain: ' +str(best_split)
		return best_split

# ***************** CANDIDATE SPLITS HELPER METHODS *****************

def info_tiebreaker(curr_feature, prev_feature, gain):
	curr_type = curr_feature.get_type()
	prev_type = prev_feature.get_type()

	# numeric = 'numeric split'
	# nominal = 'nominal split'

	# if curr_type == 'numeric split' and prev_type == 'numeric split':
	# 	# if both are numeric, lowest value wins
	# 	if curr_feature.threshold == prev_feature.threshold:
	# 		# both are equal; resolve with the ARFF order
	# 		pass
	# 	elif curr_feature.threshold < prev_feature.threshold:
	# 		return format_best_split(curr_feature, gain)
	# 	else:
	# 		return format_best_split(prev_feature, gain)
	# else:
	# 	pass

	# if we got here, lower ARFF index wins!
	curr_index = curr_feature.feature.get('index')
	prev_index = prev_feature.feature.get('index')

	if curr_index <= prev_index:
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
			num_split = numeric_candidate_splits(data, feature, num_items, a)
			# don't add splits with no information
			if num_split != None:
				numeric[attr] = num_split
			else:
				pass

		elif feature.get('type') == 'nominal':
			nominal[attr] = nominal_candidate_splits(data, feature, num_items)
		else:
			# the class variable
			pass

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

def make_list_unique(sorted_list):
	seen = set()
	seen_add = seen.add
	new_list = []
	return [ x for x in sorted_list if not (x in seen or seen_add(x))]

def build_threshold_branches(index, data, threshold):
	left_branch = []
	right_branch = []
	# split the data-sets based on the threshold we found (midpoint)
	for instance in data:
		if instance[index] < threshold:
			left_branch.append(instance)
		else:
			right_branch.append(instance)

	if len(data) != len(left_branch) + len(right_branch):
		raise ValueError('We lost data while splitting!!!!!!!!')
	else:
		pass

	return left_branch, right_branch

def get_midpoint_candidates(data, index, attributes):
	"""identify adjacent examples that differ in their target class"""
	"""choose thresholds with maximum information gain"""
	# a threshold must be a midpoint between a positive & negative instance
	# thresholds must be adjacent
	class_labels = attributes.get('class').get('options')
	negative = class_labels[0]
	positive = class_labels[1]
	prev_row = data[0]

	midpoints = []
	all_thresh = {}
	threshold_def = {'neg_point':None, 'pos_point':None, 'threshold':None}

	# algorithm:
	# 1- for each negative point, find the next positive point (that is greater)
	# 2- for each positive point, find the next negative point (that is greater)
	# i.e. it's ok to skip the next point if it's the OPPOSITE class AND the same value.
	# soln? remove identical adjacent nodes
	
	clean_data = []
	neg_rows = {}
	pos_rows = {}

	# remove duplicates of the same type by inserting them into dict objects
	for row in data:
		if row[-1] == negative:
			neg_rows[str(row[index])] = row
		else:
			pos_rows[str(row[index])] = row

	# merge data back together
	for row in neg_rows:
		clean_data.append(neg_rows[row])
	for row in pos_rows:
		clean_data.append(pos_rows[row])

	# if index == 0 and len(orig_data) == 99:
	# 	print neg_rows
	# 	exit(0)
	# 	print pos_rows
	# else:
	# 	pass

	# print clean_data
	# exit(0)

	# use a data set where adjacent duplicates are removed
	orig_data = data
	data = sorted(clean_data, key=lambda x: x[index])	

	# if index == 9 and len(orig_data) == 4:
	# 	# print 'this is age (index 0)' #age index 0, ca index 11, oldpeak 9
	# 	for d in orig_data:
	# 		my_str = str(d[index])
	# 		if d[-1] == negative:
	# 			my_str += ' -'
	# 		else:
	# 			my_str += ' +'
	# 		print my_str
	# 	exit(0)
	# else:
	# 	pass

	count = 0
	for row in data:
		# only traverse (increment count) after we looked ahead & made the next 
		# relevant comparison (if any)
		count += 1

		# edge case: (why we need a 3rd row)
		# we may need to peek ahead two rows
		# e.g. -55.0, -56.0, +56.0 (e.g. compare 55 vs 56)
		# if these two rows are the same class, see if 3rd row is diff class & equal to 2nd row

		# traverse until we find the next non duplicate
		inner_count = count
		for next_row in data[count:]:
			inner_count += 1

			# 3rd row edge case check
			# e.g. -55.0, -56.0, +56.0 (e.g. compare 55 vs 56)
			# 1-if the next is homogenous & greater (it will always be greater)
			if row[-1] == next_row[-1]:
				for third_row in data[inner_count:]:
					# 2-if the third row is a diff class that first... 
					# 3-if the third row index == same as 2nd row index...
					if row[-1] != third_row[-1] and next_row[index] == third_row[index]:
						# we found an edge case threshold.. add it!
						# incomplete (add threshold)
						if third_row[-1] == negative and row[-1] == positive:
							neg_inst = float(third_row[index])
							pos_inst = float(row[index])

							new_midpoint = (pos_inst + neg_inst)/2.0
							midpoints.append( new_midpoint )
							threshold_def['neg_point'] = neg_inst
							threshold_def['pos_point'] = pos_inst
							threshold_def['threshold'] = new_midpoint
							all_thresh[str(new_midpoint)] = threshold_def
						elif third_row[-1] == positive and row[-1] == negative:
							pos_inst = float(third_row[index])
							neg_inst = float(row[index])

							new_midpoint = (pos_inst + neg_inst)/2.0
							midpoints.append( new_midpoint )
							threshold_def['neg_point'] = neg_inst
							threshold_def['pos_point'] = pos_inst
							threshold_def['threshold'] = new_midpoint
							all_thresh[str(new_midpoint)] = threshold_def
						else:
							raise ValueError('Midpoint calculation blew up!!!!!!!')
							break
					else:
						pass
			else:
				pass

			if row[index] == next_row[index]:
				continue
			elif row[-1] != next_row[-1]: # we have a point of contrast
				if next_row[-1] == negative and row[-1] == positive:
					neg_inst = float(next_row[index])
					pos_inst = float(row[index])

					new_midpoint = (pos_inst + neg_inst)/2.0
					midpoints.append( new_midpoint )
					threshold_def['neg_point'] = neg_inst
					threshold_def['pos_point'] = pos_inst
					threshold_def['threshold'] = new_midpoint
					all_thresh[str(new_midpoint)] = threshold_def
				elif next_row[-1] == positive and row[-1] == negative:
					pos_inst = float(next_row[index])
					neg_inst = float(row[index])

					new_midpoint = (pos_inst + neg_inst)/2.0
					midpoints.append( new_midpoint )
					threshold_def['neg_point'] = neg_inst
					threshold_def['pos_point'] = pos_inst
					threshold_def['threshold'] = new_midpoint
					all_thresh[str(new_midpoint)] = threshold_def
				else:
					raise ValueError('Midpoint calculation blew up!!!!!!!')
					break
			else:
				# the adjacent value is the same, we have no midpoint candidate here
				break

	# age check.......
	# if index == 0 and len(orig_data) == 6 and midpoints != []:
	# 	print midpoints
	# 	exit(0)
	# else:
	# 	pass

	# make sure midpoints are all unique
	midpoints = make_list_unique(midpoints)
	midpoints = sorted(midpoints)

	return midpoints, all_thresh


# split the data-sets based on the threshold (a.k.a. midpoint)
def numeric_candidate_splits(data, feature, num_items, attributes):
	"""splits on numeric features use a threshold"""
	"""sort data by feature value asc"""

	index = feature.get('index')
	sorted_data = sorted(data, key=lambda x: x[index])

	if len(sorted_data) != len(data):
		raise ValueError('We lost data while sorting!!!!!!!!')
	else:
		pass

	data = sorted_data

	# build all possible midpoint candidate splits; make the decision based on
	# maxized information gain
	midpoints, thresh_defs = get_midpoint_candidates(data, index, attributes)

	# 1-build the set of candidate splits
	maxgain = -1
	best_split = None

	# start with the smallest midpoints since a tie is broken with two equal sized
	# midpoints
	for m in midpoints:
		left, right = build_threshold_branches(index, data, m)
		split = NumericCandidateSplit(feature, left, right, m)
		gain = info_gain(data, split, attributes)

		# print gain
		if gain > maxgain:
			maxgain = gain
			threshold = m
			split.thresh_def = thresh_defs.get(str(m),'')
			best_split = split
			# print 'gain: %s from midpoint %s' % (gain, m)

	# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	# the_name = feature.get('name')
	# if the_name == 'oldpeak':
	# 	print feature
	# 	exit(0)
	# else:
	# 	pass

	# class_labels = attributes.get('class').get('options')
	# nlabel = class_labels[0]
	# # exit(0)
	# if the_name == 'ca' and len(data) == 10:
	# 	for d in data:
	# 		my_str = str(d[index])
	# 		if d[-1] == nlabel:
	# 			my_str += ' -'
	# 		else:
	# 			my_str += ' +'
	# 		print my_str

	# 	print 'threshold'
	# 	print threshold
	# 	exit(0)
	# 	for m in midpoints:
	# 		print m

	# 	print 'threshold'
	# 	print threshold
	# 	# else:
	# 	# pass
	# 	exit(0)
	# else:
	# 	pass
	# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	return best_split

