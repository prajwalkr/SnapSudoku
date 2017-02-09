import numpy as np
from random import shuffle


class QuadraticCost(object):

    @staticmethod
    def cost(a, y):
        # norm of a vector
        return 0.5 * (np.linalg.norm(a - y)**2)

    @staticmethod
    def delta(z, a, y):
        return (a - y) * sigmoid_prime(z)


class CrossEntropyCost(object):

    @staticmethod
    def cost(a, y):
        # nan_to_num handles log values when a =~ 0 or 1.
        return np.nan_to_num(-y * np.log(a) - (1 - y) * np.log(1 - a))

    @staticmethod
    def delta(z, a, y):
        return (a - y)


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

    def __init__(self, sizes=None, cost=CrossEntropyCost, customValues=None):
        if not customValues:
            self.layers = len(sizes)
            self.sizes = sizes
            self.biases = [np.random.randn(x, 1) for x in sizes[1:]]
            self.wts = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]
        else:
            self.sizes, self.biases, self.wts = customValues
            self.layers = len(self.sizes)
        self.cost = cost

    def feedforward(self, inputs):
        '''
                Return the outputs for a given set of inputs to the network.
        '''
        res = inputs 		# output = input for the first(input) layer
        for w, b in zip(self.wts, self.biases):
            res = sigmoid(np.dot(w, res) + b)
        return res

    def SGD(self, training_data, MBsize, eta, epochs, test, Lambda=0.0):
        '''
                Implements Stochastic Gradient Descent using Mini Batches,
                does `epochs` number of iterations on the training data with 
                learning rate `eta`.
        '''
        for iteration in xrange(epochs):
            if iteration % (epochs // 4) == 0:
                percent = str(100 * float(iteration) / epochs)
                correctness = str(self.evaluate(test))
                print "At {}% correctness is: {}".format(percent, correctness)
            shuffle(training_data)
            mini_batches = [training_data[i:i + MBsize]
                            for i in range(0, len(training_data), MBsize)]
            for mini_batch in mini_batches:
                self.train_network_on(
                    mini_batch, eta, Lambda, len(training_data))

    def train_network_on(self, batch, eta, Lambda, n):
        '''
                Updates the wts and biases of the Neural Network using 
                Gradient Descent on a given set of `m` training examples, with
                a learning rate `eta`.
        '''
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.wts]
        for x, y in batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.wts = [(1 - eta * Lambda / n) * w - (eta / len(batch)) * nw
                    for w, nw in zip(self.wts, nabla_w)]
        self.biases = [b - (eta / len(batch)) * nb
                       for b, nb in zip(self.biases, nabla_b)]

    # This function calculated the differentiation of Cost function (x)
    # wrt to biases or wts (y). This is the back propagation algorithm.
    # Treated as a black-box till now. Don't know what is happening!
    def backprop(self, x, y):
        """
                Return a tuple ``(nabla_b, nabla_w)`` representing the
                gradient for the cost function C_x.  ``nabla_b`` and
                ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
                to ``self.biases`` and ``self.wts``.
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.wts]
        # feedforward
        activation = x
        activations = [x]  # list to store all the activations, layer by layer
        zs = []  # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.wts):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost.delta(zs[-1], activations[-1], y)
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Here, l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.
        for l in xrange(2, self.layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.wts[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """
                Return the number of test inputs for which the neural
                network outputs the correct result. Note that the neural
                network's output is assumed to be the index of whichever
                neuron in the final layer has the highest activation.
        """
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        return (output_activations - y)


def sigmoid(z):
    return (1.0 / (1.0 + np.exp(-z)))


def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z) * (1 - sigmoid(z))
