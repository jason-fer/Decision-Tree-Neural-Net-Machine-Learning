
class NumericNode(object):
    """A numeric (binary) decision tree node"""
    def __init__(self, parent, data, leftNode, rightNode):
      self.parent = parent
      self.leftNode = leftNode
      self.rightNode = rightNode
      self.data = data


class NominalNode(object):
    """A nominal decision tree node (with a list of results)"""
    def __init__(self, parent, data, nodeList):
      self.parent = parent
      self.nodeList = nodeList
      self.data = data


class DecisionTree(object):
    """Machine Learning Decision Tree Structure"""
    def __init__(self):
      self.rootNode = None

    def addNumericNode(self, parent, data, leftNode, rightNode):
      node = NumericNode(data, leftNode, rightNode)
      # now add the node to the tree...

    def addNominalNode(self, parent, data, nodeList):
      node = NumericNode(data, items)
      # now add the node to the tree...

    def printTree(self):
      # print the Decision Tree
      pass