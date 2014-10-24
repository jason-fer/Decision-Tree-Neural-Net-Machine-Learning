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
  # get negative x
  x = x * -1
  # run the sigmoid function
  return 1 / (1 + math.exp(x))

def main(args):
  """usage neuralnet.py <data-set-file> n l e"""
  """ n = the number of folds for cross validation """
  """ l = the learning rate """
  """ e = the number of training epochs """

  x = -5
  print sigmoid(x)

  # train_set_file, n, l, e = get_arguments(args)
  # arff_file = load_data(train_set_file)
  arff_file = load_data('examples/sonar.arff')
  attributes = get_attributes(arff_file['attributes'])
  class_labels = attributes.get('Class').get('options')
  data = arff_file['data']



if __name__ == "__main__":
  main(sys.argv)