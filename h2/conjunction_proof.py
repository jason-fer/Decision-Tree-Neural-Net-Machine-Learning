""" This is proof that my answer to HW2, question #3 is correct"""
""" where y = (x1 ^ x2) v (x3 ^ x4) """
import sys, math

def get_sigmoid(x):
  # run the sigmoid function
  return 1.0 / (1.0 + math.exp( - x))

  # kd_tree = kdtree.create(dimensions=2)
  # root = collections.namedtuple('Point', 'x y z')
def main(args):
  bias_1 = -5
  bias_2 = -5
  bias_out = - 2

  x1 = 0.0
  x2 = 0.0
  x3 = 1.0
  x4 = 1.0

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
  # print 'x:%f AND1:%f'%(x, sigmoid)
  x = sigmoid

  # 2nd perceptron
  y = x3 * w3 + x4 * w4 + bias_2
  sigmoid = get_sigmoid(y)
  # print 'y:%f AND2:%f'%(y, sigmoid)
  y = sigmoid

  z = wp1 * x + wp2 * y + bias_out
  sigmoid = get_sigmoid(z)
  # print 'z:%f OR: %f'%(z, sigmoid)
  z = sigmoid

  print '(%d ^ %d) v (%d ^ %d) = %f where true is > 0.5' % (x1, x2, x3, x4, z)

if __name__ == "__main__":
  main(sys.argv)