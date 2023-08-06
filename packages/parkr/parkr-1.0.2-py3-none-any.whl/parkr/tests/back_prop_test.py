import sys
import numpy as np

sys.path.append('..')

from parkr.network import Network
from parkr.activation import ActivationMethods  # TODO sort this multiple imports out

def test_back_prop():
    EXPECTED_VALUE = 0.53639513

    test_network = Network(2,[2],1, ActivationMethods.SIGMOID)
    
    test_network.weight_matrix = [np.array([[3,6],[4,5]]),
                                np.array([[2],[4]])]
    test_network.bias_matrix = [np.array([[1, -6]]), np.array([[-3.92]])]
    
    input_data = np.array([[1,0],[1,0]])
    expected_data = np.array([[1],[1]])
    
    test_network.train(2, (input_data, expected_data), step_size=0.1, batch_size=2)
    
    assert abs(test_network.forward_pass([1,0])[0][0]-EXPECTED_VALUE) < 0.00000001  # check if its close (double issues)

def test_momentum():

    EXPECTED_WEIGHT = 3.0012  # this should be the weight from node A->C 

    test_network = Network(2,[2],1, ActivationMethods.SIGMOID)
    
    test_network.weight_matrix = [np.array([[3,6],[4,5]]),
                                np.array([[2],[4]])]
    test_network.bias_matrix = [np.array([[1, -6]]), np.array([[-3.92]])]
    
    input_data = np.array([[1,0]])
    expected_data = np.array([[1]])
    
    test_network.train(2, (input_data, expected_data), step_size=0.1, momentum_rate=0.9)

    assert abs(test_network.weight_matrix[0][0][0] - EXPECTED_WEIGHT) < 0.0001