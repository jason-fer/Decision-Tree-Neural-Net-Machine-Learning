""" Manually checking my answer to HW2, question #4 """
from random import shuffle
import sys, math

def get_delta(o, y):
  # output * derivative of logistic function * target output miss
  return o * (1 - o) * (y - o)

def get_sigmoid(x):
  # run the sigmoid function
  return 1.0 / (1.0 + math.exp( - x))

  # kd_tree = kdtree.create(dimensions=2)
  # root = collections.namedtuple('Point', 'x y z')
def main(args):
  # we need eta * delta * output
  # i.e. learning_rate * error * output


  # calculate outputs, h1, h2, o1, o2
  x1 = 0 # input, given
  x2 = 1 # input, given
  h1_bias = -0.5
  h2_bias = -1

  y1 = 1 # expected output
  y2 = 0 # expected output
  o1_bias = 0
  o2_bias = -0.5

  # get the nets
  h1_net = (1 *    x1) + (-0.5 * x2) + h1_bias
  h2_net = (-0.5 * x1) + (1 * x2) + h2_bias
  # print 'h1_net:' +str(h1_net)
  # print 'h2_net:' + str(h2_net)
  print 'calculate hidden outputs'
  h1 = get_sigmoid(h1_net)
  h2 = get_sigmoid(h2_net)
  print 'h1:' + str(h1)
  print 'h2:' + str(h2)

  print '\ncalculate outputs'
  o1_net = (-2 *    h1) + (1 *  h2) + o1_bias
  o2_net = (-2 *    h1) + (-2 * h2) + o2_bias
  o1 = get_sigmoid(o1_net)
  o2 = get_sigmoid(o2_net)
  print 'o1:' + str(o1)
  print 'o2:' + str(o2)

  print '\ncalculate output unit errors'
  o1_delta = get_delta(o1, y1)
  o2_delta = get_delta(o2, y2)
  print 'o1_delta:' + str(o1_delta)
  print 'o2_delta:' + str(o2_delta)

  print '\ncalculate hidden unit errors'
  # backpropgate weighted errors to hidden units
  # delta = output * derivative of logistic + sum of net weight errors
  # e.g. delta = h1(1 - h1) sum[o1_delta(-2) + o2_delta(-2)]
  # (use the same error weights as above, while in reverse...backpropagation)
  h1_delta = h1 * (1 - h1) * (o1_delta * -2 + o2_delta * -2)
  h2_delta = h2 * (1 - h2) * (o1_delta * 1 + o2_delta * -2)
  print 'h1_delta:' + str(h1_delta)
  print 'h2_delta:' + str(h2_delta)

  print '\ncalculate weight changes'
  # minimize squared error, & the learning rate is .1
  l = 0.1
  # weight_update = eta * delta * output
  weight_delta_o1_h1   = l * 
  weight_delta_o2_h1   = l * 
  weight_delta_o1_h2   = l * 
  weight_delta_o2_h2   = l * 
  weight_delta_bias_o1 = l * 
  weight_delta_bias_o2 = l * 
  weight_delta_bias_h1 = l * 
  weight_delta_bias_h2 = l * 
  weight_delta_h1_x1   = l * 
  weight_delta_h2_x1   = l * 
  weight_delta_h1_x2   = l * 
  weight_delta_h2_x2   = l * 


if __name__ == "__main__":
  main(sys.argv)