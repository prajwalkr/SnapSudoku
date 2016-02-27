import numpy as np
from random import shuffle

class NeuralNetwork(object):
	'''Represents a Neural Network with:
		1. sizes[i] representing the number of neurons in the ith layer
		2. biases[i] representing the biases of the ith layer
		3. wts[i][j][k] represents the wt from the kth neuron in the ith
		   layer to the jth neuron in the (i + 1)th layer.
	   Initially all are random values.
	   A Neural Network is initialised as NeuralNetwork(sizes), 
	   	sizes = array having number of neurons in each layer, eg. NeuralNetwork([1,2,3])
	'''
	def __init__(self, sizes):
		self.layers = len(sizes)
		self.sizes = sizes
		self.biases = [np.random.randn(x,1) for x in sizes[1:]]
		self.wts = [np.random.randn(y,x) for x,y in zip(sizes[:-1],sizes[1:])]

	def feedforward(self,inputs):
		'''
			Return the outputs for a given set of inputs to the network.
		'''
		res = inputs 		# output = input for the first(input) layer
		for w,b in zip(self.wts,self.biases):
			res = sigmoid(np.dot(w,res) + b)

	def SGD_MB(self,training_data,MBsize,eta,epochs):
		'''
			Implements Stochastic Gradient Descent using Mini Batches,
			does `epochs` number of iterations on the training data.
		'''
		for iteration in xrange(epochs):
			shuffle(training_data)
			mini_batches = [training_data[i:i + MBsize] for i in range(0,len(training_data),MBsize)]
			for mini_batch in mini_batches:
				self.train_network_on(mini_batch,eta)

	def train_network_on(self,batch,eta):
		'''
			Updates the weights and biases of the Neural Network using 
			Gradient Descent on a given set of `m` training examples
		'''
		


def sigmoid(z):
	return (1.0/(1.0 + np.exp(-z)))
