from lib import arff
from random import shuffle
import sys, helpers, math

#helpers
dump_attributes = helpers.dump_attributes
load_data = helpers.load_data
dump_splits = helpers.dump_splits
homogenous_check = helpers.homogenous_check
get_attributes = helpers.get_attributes
get_class_counts = helpers.get_class_counts
get_arguments = helpers.get_arguments

# no hidden units or momentum are used
# one sigmoid output only, since the problem is binary 
# one input per numeric feature (e.g. 60x in the current example)
# All weights and the bias parameter are initialized to the value 0.1
# Stochasic gradient descent is used to minimize squared error
def sigmoid(x):
  # run the sigmoid function
  return 1.0 / (1.0 + math.exp( - x))


def init_weights(num_features):
  weights = []
  # initialize all features to .1, except class which we exclude
  for x in range(num_features):
    weights.append(0.1)

  return weights


def get_actual(actual, class_labels):
  if actual[-1] == class_labels[0]:
    # we expected rock
    return 0.0
  else:
    # we expected mine
    return 1.0


def stochastic_gradient_descent(learn_rate, actual, bias, weights, class_labels):
  # stochastic gradient descent algorithm:
  # for each (x(d), y(d)) in the training set
  #   input x(d) to the network & compute output o(d)
  #    calculate the error E(w) = 1/2 (y(d) - o(d))^2
  #    calculate the gradient
  #    VE(w) = [dE/dw_0, dE/dw_1, ...] 
  #    update the weights
  #    /\w = - learn_rate * VE(w)

  # add the bias
  net = bias
  # add the rest of the weighted units
  for i in range(len(actual) - 1):
    net += weights[i] * actual[i]

  # push the net our next layer (the sigmoid)
  o = sigmoid(net)
  # get the actual result ('rock' or 'mine')
  y = get_actual(actual, class_labels)

  # sum up 1/2 the squared error distances
  error = math.pow((o - y), 2) / 2.0

  derivative_err_out = - (y - o)
  # the derivative of the error with respect to the weight
  derivative_out_net = o * (1 - o)
  
  # calculate the partial derivative for each weight
  for i in range(len(actual) - 1):
    X_i = weights[i] * actual[i]
    # the partial error derivative with respect W_i
    error_derivative_w = derivative_err_out * derivative_out_net * X_i

    # now we can update the weight for this item
    weights[i] += - learn_rate * error_derivative_w

  # update the bias
  error_derivative_w = derivative_err_out * derivative_out_net * bias
  bias += - learn_rate * error_derivative_w

  # return results (incomplete)
  return bias, weights, error


def print_error(error, prev_error, up, down):
    if (error - prev_error) > 0.0:
      print '+' + str(error - prev_error)
      up += 1
    else:
      print str(error - prev_error)
      down += 1
    prev_error = error
    return prev_error, up, down


def print_result(up, down, bias):
  print 'it was up %s' % (up)
  print 'it was down %s' % (down)
  print 'bias was: %f' %(bias)

def main(args):
  """usage neuralnet.py <data-set-file> n l e"""
  """ n = the number of folds for cross validation """
  """ l = the learning rate """
  """ e = the number of training epochs """

  # train_set_file, n, l, e = get_arguments(args)
  n = 10  # number of cross validation folds
  l = 0.1 # learning rate
  e = 100 # training epochs

  # arff_file = load_data(train_set_file)
  arff_file = load_data('examples/sonar.arff')
  attributes = get_attributes(arff_file['attributes'])
  class_labels = attributes.get('Class').get('options')
  #weight zero = bias unit
  weights = init_weights(len(attributes))
  bias = 0.1
  training_set = arff_file['data']

  prev_error = 0
  # stochastic, online, gradient descent
  count = 0
  up = 0
  down = 0

  for i in range(1, e):
    for instance in training_set:
      bias, weights, error = stochastic_gradient_descent(l, instance, bias, weights, class_labels)
      count += 1

    prev_error, up, down = print_error(error, prev_error, up, down)

  print_result(up, down, bias)
  # When the activation on the output unit (i.e. the value computed by the sigmoid) > 0.5
  # Stochasic gradient descent is used to minimize squared error


if __name__ == "__main__":
  main(sys.argv)