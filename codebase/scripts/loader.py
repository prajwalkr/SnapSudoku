import pickle

from train import NeuralNetwork

with open('train', 'r') as in_file:
    training = pickle.load(in_file)
with open('test', 'r') as in_file:
    testing = pickle.load(in_file)

net = NeuralNetwork([784, 30, 30, 10])
net.SGD(training, 1, 0.05, len(training), testing, 0.5)

with open('../networks/net', 'w') as out_file:
    pickle.dump((net.sizes, net.biases, net.wts), out_file)
