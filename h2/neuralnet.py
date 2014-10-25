from lib import arff
from random import shuffle
import sys, helpers, math

#helpers
load_data = helpers.load_data
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


# The 'actual' number is the sigmoid activation
def get_actual(actual, class_labels):
  if actual[-1] == class_labels[0]:
    # we expected rock
    return 0.49
  else:
    # we expected mine
    return 0.51 # we can assume the 2nd class value is positive


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

  # return results
  return bias, weights, error


def split_instances(training_set, class_labels):
  """ split training set into positive / negative samples """
  pos_instances = []
  neg_instances = []

  for instance in training_set:
    class_type = get_actual(instance, class_labels)
    if class_type > 0.5:
      pos_instances.append(instance)
    else:
      neg_instances.append(instance)

  return pos_instances, neg_instances


def stratified_k_cross_folds(pos_instances, neg_instances, k_folds):
  pos_count = len(pos_instances)
  neg_count = len(neg_instances)
  
  # determine which count is less; this will determine fold_size
  if pos_count > neg_count:
    fold_size = neg_count / k_folds
  else:
    fold_size = pos_count / k_folds

  shuffle(pos_instances)
  shuffle(neg_instances)

  # For stratified cross-validation, the training set will have an equal number 
  # of patterns from each class (otherwise it isn't stratified)
  k_cross_folds = []
  i = 0
  for x in range(k_folds):
    curr_fold = []
    for y in range(fold_size):
      curr_fold.append(pos_instances[i])
      curr_fold.append(neg_instances[i])
      i += 1

    shuffle(curr_fold)
    k_cross_folds.append(curr_fold)

  # check count
  # count = 0
  # for fold in k_cross_folds:
  #   count += len(fold)
  #   # for x in fold:
  #   #   print x
  # print count
  # exit(0)

  return k_cross_folds

def validation_test(bias, weights, validation_set, class_labels):
  """ determine the error of the current weights vs the validation set"""

  # get the total error for this entire validation set
  error = 0
  for actual in validation_set:
    # add the bias
    net = bias
    # add the rest of the weighted units
    for i in range(len(actual) - 1):
      net += weights[i] * actual[i]

    o = sigmoid(net)
    y = get_actual(actual, class_labels)
    # print 'actual result:' + str(y)
    # print 'sigmoid:' + str(o)
    error += math.pow((o - y), 2) / 2.0

  return error;

def get_fold_number(k_cross_folds, instance):
  fold_count = 0
  for fold in k_cross_folds:
    fold_count += 1
    for row in fold:
      match = True
      i = 0
      for datum in row:
        if datum == row[i]:
          i += 1
          pass
        else:
          match = False
          break
      if match:
        return fold_count
      else:
        pass
    

def get_prediction(bias, weights, actual, class_labels):
  net = bias
  # add the rest of the weighted units
  for i in range(len(actual) - 1):
    net += weights[i] * actual[i]

  o = sigmoid(net)
  # greater than 0.5 == positive
  if o > 0.5:
    return class_labels[1], o
  else:
    return class_labels[0], o


def print_output(k_cross_folds, bias, weights, data, class_labels):
  """ print one line per instance in the same order as data file """
  for instance in data:
    output = ''
    fold = get_fold_number(k_cross_folds, instance)
    predicted, sigmoid = get_prediction(bias, weights, instance, class_labels)
    actual = instance[-1]
    print 'fold:%s  predicted:%s  actual:%s  confidence:%s' %(fold, predicted, actual, sigmoid)

def train_curr_fold(training_set, l, bias, weights, class_labels):
  errors = 0
  for instance in training_set:
    # training_set.append(fold)
    bias, weights, error = stochastic_gradient_descent(l, instance, bias, weights, class_labels)
    errors += error

  return bias, weights, errors

def print_weights(bias, weights):
  print 'weights!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
  print bias, weights

def main(args):
  """usage neuralnet.py <data-set-file> n l e"""
  """ n = the number of folds for cross validation """
  """ l = the learning rate """
  """ e = the number of training epochs """

  # train_set_file, n, l, e = get_arguments(args)
  n = 10  # number of cross validation folds
  l = 0.1 # learning rate
  e = 10 # training epochs

  # arff_file = load_data(train_set_file)
  arff_file = load_data('examples/sonar.arff')
  attributes = get_attributes(arff_file['attributes'])
  class_labels = attributes.get('Class').get('options')

  weights = init_weights(len(attributes))
  bias = .1

  data = arff_file['data']

  # debug variables
  prev_error = None
  up = 0
  down = 0

  # run the current epoch (one pass through the entire training set)
  pos_instances, neg_instances = split_instances(data, class_labels)
  k_cross_folds = stratified_k_cross_folds(pos_instances, neg_instances, n)

  min_error = None

  # print_weights(bias, weights)
  
  # run program for the specified number of epochs
  for epoch in range(e):

    # we only update the weights once per epoch; we cross-validate all folds,
    # then the fold that 'wins' becomes the update
    for v in range(n):
      # print 'on iteration k = %s of k-folds: %s' %(v, n)
      # get the current validation set
      validation_set = k_cross_folds[v]

      # reset variables
      min_error = None
      best_bias = None
      best_weights = None

      # loop through each training set, skipping the validation set
      for i in range(n):
        if i == v:
          pass # don't train on the validation set!!
        else:
          # run the current set
          curr_bias, curr_weights, error = train_curr_fold(k_cross_folds[i], l, bias, weights, class_labels)
          # check the predictive power of this set
          current_error = validation_test(curr_bias, curr_weights, validation_set, class_labels)
          # print 'set %s had error: %s' %(i, current_error)
          
          # update our weights if this is better than the last set
          if min_error == None or current_error < min_error:
            min_error = current_error
            best_weights = curr_weights
            best_bias = curr_bias
          else:
            pass
      # update our results from this epoch with the best values
      if best_bias == None or best_weights == None:
        raise ValueError('(impossible)')
      else:
        pass
      weights = best_weights
      bias = best_bias
      # print_weights(bias, weights)
      # exit(0)
      # print 'error: ' + str(min_error)
  print_output(k_cross_folds, bias, weights, data, class_labels)


if __name__ == "__main__":
  main(sys.argv)


  # # test..... to see if things converge
  # for instance in data:
  #   break

  # count = 0
  # prev_error = 100
  # for i in range(1000):
  #   bias, weights, error = stochastic_gradient_descent(l, instance, bias, weights, class_labels)
  #   # if i % 100 == 0:
  #   #   if error < prev_error:
  #   #     print '-' + str(error) + ' vs prev_error:' + str(prev_error)
  #   #   else:
  #   #     print '+' + str(error) + ' vs prev_error:' + str(prev_error)
  #   #   prev_error = error
  #   count += 1
  # exit(0)