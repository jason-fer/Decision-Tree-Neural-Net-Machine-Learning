class Node(object):
    """Numeric, Nominal, or Class decision tree node (with a list of results)"""
    def __init__(self, attribute, value):
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

    def addNumericNode(self, parent, data, leftNode, rightNode):
      node = NumericNode(data, leftNode, rightNode)
      # now add the node to the tree...

    def addNominalNode(self, parent, data, nodeList):
      node = NumericNode(data, items)
      # now add the node to the tree...

    def printTree(self):
      # print the Decision Tree
      pass