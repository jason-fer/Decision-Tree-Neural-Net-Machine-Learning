
# ********************************** PART 2 **********************************

# Plot learning curves that characterize the predictive accuracy the learned 
# trees as a function of the training set size. 
# Y-axis: accuracy
# X-axis: training set size
# 
# Two Problem Domains:
# 1-Predicting the presence or absence of heart disease
# - training set: heart_train.arff
# - test set: heart_test.arff
# 
# 2-Predicting whether a patient has diabetes or not
# - training set: diabetes_train.arff
# - test set: diabetes_test.arff
#
# Plot points for training set sizes that represent 5%, 10%, 20%, 50% and 100% 
# of the instances in each given training file. For each training-set 
# size (except the largest one), randomly draw 10 different training sets and <--random sampling!
# evaluate each resulting decision tree model on the test set. For each training
# set size, plot the average test-set accuracy and the minimum and maximum 
# test-set accuracy. Label the axes of the plots. Set the stopping criterion m=4
# for these experiments.