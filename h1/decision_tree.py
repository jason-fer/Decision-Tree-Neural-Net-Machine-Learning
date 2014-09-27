import unittest

class Node(object):
    """Numeric, Nominal, or Class decision tree node (with a list of results)"""
    def __init__(self, name, attribute, value):
      self.name = name
      self.attribute = attribute
      self.value = value
      self.children = {}

    def is_leaf(self):
      self.children == {}

class DecisionTree(object):
    """Machine Learning Decision Tree Structure"""
    def __init__(self):
      self.root = None

    def printTree(self):
      # print the Decision Tree
      pass

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

