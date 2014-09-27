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