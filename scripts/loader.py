import pickle as pck

from train import NeuralNetwork

training = pck.load(open('train', 'r'))
testing = pck.load(open('test', 'r'))

net = NeuralNetwork([784, 30, 30, 10])
net.SGD(training, 1, 0.05, len(training), testing, 0.5)

pck.dump((net.sizes, net.biases, net.wts), open('../networks/net', 'w'))
