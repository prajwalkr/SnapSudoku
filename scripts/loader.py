import pickle as pck

from train import NeuralNetwork

training = pck.load(open('train','r'))
testing = pck.load(open('test','r'))

net = NeuralNetwork([784,30,10])
net.SGD(training, 2, 0.05, 300, testing,0.5)

pck.dump(net, open('../net','w'))