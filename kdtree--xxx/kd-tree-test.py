from random import shuffle
import sys, math, kdtree, collections
from Queue import PriorityQueue

class PriorityQueueKD(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def push(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def pop(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item

class Node():
  def __init__(self):
    pass

  def setLeft(self, left):
    self.left = left

  def setRight(self, right):
    self.right = right

  def setData(self, data, dimension):
    # dimension = x or y
    self.data = data
    self.dimension = dimension

  def getBound(self, data):
    pass
    # get the Euclidean distance between the data points
    

def get_sigmoid(x):
  # run the sigmoid function
  return 1.0 / (1.0 + math.exp( - x))

  # kd_tree = kdtree.create(dimensions=2)
  # root = collections.namedtuple('Point', 'x y z')
def main(args):
  """ implementing KDtree by hand to understand it... """
  PQ = PriorityQueueKD()      # a minimizing PriorityQueue
  best_dist = float('inf')        # smallest distance seen so far


  # bias_1 = -6
  # bias_2 = -6
  # bias_out = - 2

  # x1 = 1.0
  # x2 = 0.0
  # x3 = 1.0
  # x4 = 0.0

  # # hidden weights
  # w1 = 4.0
  # w2 = 4.0
  # w3 = 4.0
  # w4 = 4.0

  # # weights for perceptrons
  # wp1 = 4.0
  # wp2 = 4.0


  bias_1 = -5
  bias_2 = -5
  bias_out = - 2

  x1 = 1.0
  x2 = 1.0
  x3 = 0.0
  x4 = 0.0

  # hidden weights
  w1 = 3.0
  w2 = 3.0
  w3 = 3.0
  w4 = 3.0

  # weights for perceptrons
  wp1 = 3.0
  wp2 = 3.0

  # 1st perceptron
  x = x1 * w1 + x2 * w2 + bias_1
  sigmoid = get_sigmoid(x)
  print 'x:%f AND1:%f'%(x, sigmoid)
  x = sigmoid

  # 2nd perceptron
  y = x3 * w3 + x4 * w4 + bias_2
  sigmoid = get_sigmoid(y)
  print 'y:%f AND2:%f'%(y, sigmoid)
  y = sigmoid

  z = wp1 * x + wp2 * y + bias_out
  sigmoid = get_sigmoid(z)
  print 'z:%f OR: %f'%(z, sigmoid)
  z = sigmoid

  # PQ.push(root, 0)

  # while PQ.empty() == False:
  #   node, bound = PQ.pop()

  #   if bound >= best_dist:
  #     return best_node.instance   # nearest neighbor found
  #   else:
  #     pass

  #   dist = distance(q, node.instance)
  #   if dist < best_dist
  #     best_dist = dist
  #     best_node = node
  #   if q[node.feature] - node.threshold > 0:
  #     PQ.push(node.left, q[node.feature] - node.threshold)
  #     PQ.push(node.right, 0)
  #   else:
  #     PQ.push(node.left, 0)
  #     PQ.push(node.right, node.threshold - q[node.feature])

  # return best_node.instance


if __name__ == "__main__":
  main(sys.argv)