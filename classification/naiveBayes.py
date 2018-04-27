# naiveBayes.py
# -------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1 # this is the smoothing parameter, ** use it in your train method **
        self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
        self.priorProb = util.Counter()
        self.condProb = util.Counter()

    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """

        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));

        if (self.automaticTuning):
            kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
        else:
            kgrid = [self.k]

        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter
        that gives the best accuracy on the held-out validationData.

        trainingData and validationData are lists of feature Counters.  The corresponding
        label lists contain the correct label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """

        "*** YOUR CODE HERE ***"
        largestK = 1
        kVal = 0
        bestProb = util.Counter()
        bestCond = util.Counter()

        for k in kgrid:
            conditional = util.Counter()
            counting = util.Counter()

            #P(y)
            for label in self.legalLabels:
                count = 0
                total = 0

                for item in trainingLabels:
                    if label == item:
                        count += 1.0
                    total += 1.0

                self.priorProb[label] = float(count) / float(total)

            #Get counts of data for c(f, y)
            for label in self.legalLabels:
                for i, data in enumerate(trainingData):
                    if trainingLabels[i] != label:
                        continue
                    for cord, val in data.items():
                       conditional[(cord, val, label)] += 1.0
                       counting[(cord, label)] += 1.0


            #Get P(f | y) =  c(f, y) / sum_f(c(f, y))
            for key, val in conditional.items():
                cord, val2, label = key
                conditional[key] = float((val + k)) / float((counting[(cord, label)] + 2.0*k ))

            for label in self.legalLabels:
                for cord in self.features:
                    conditional[cord, 1, label] = 1 - conditional[cord, 0, label]

            self.condProb = conditional

            guess = self.classify(validationData)

            temp = 0;
            for i, each in enumerate(guess):
                if each == validationLabels[i]:
                    temp+=1

            if temp > kVal:
                kVal = temp
                largestK = k
                bestCond = self.condProb
                bestProb = self.priorProb
            elif temp == kVal:
                kVal = temp
                largestK = min(largestK, k)
                bestCond = self.condProb
                bestProb = self.priorProb



        #largest k
        k = largestK
        self.priorProb = bestProb
        self.condProb = bestCond
        self.classify(validationData)




    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        You shouldn't modify this method.
        """
        guesses = []
        self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses

    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        logJoint = util.Counter()
        for label in self.legalLabels:
            prob = 0

            if self.priorProb[label] != 0:
                prob = math.log(self.priorProb[label])

            for cord, val in datum.items():
                if self.condProb[(cord, val, label)] != 0:
                    prob += math.log(self.condProb[(cord, val, label)])
            logJoint[label] = prob

        return logJoint

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                P(feature=1 | label1)/P(feature=1 | label2)

        Note: you may find 'self.features' a useful way to loop through all possible features
        """
        featuresOdds = []

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
        
        return featuresOdds