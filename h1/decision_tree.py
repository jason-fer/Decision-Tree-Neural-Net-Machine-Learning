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
    obj_string = 'NumericCandidateSplit( ' + str(self.name)
    left = str(len(self.left_branch))
    right = str(len(self.right_branch))
    mid = str(self.threshold)
    opt = str(self.options)
    obj_string += ' <= %s [%s %s], %s )' % (mid, left, right, opt)
    return obj_string

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
    obj_string = 'NominalCandidateSplit( ' + str(self.name) + ' ['
    num = str(len(self.branches))
    # for each branch: name instances, (no comma first, prepend rest w/ comma)
    obj_string += ' )'
    return obj_string