# Neural Networks - CS50AI Lecture 5

Biological neural networks are a system in the human body that consist of three stages: receptors, a neural network, and effectors. The receptors receive the stimuli either internally or from the external world, then pass the information into the neurons in a form of electrical impulses.

## Artificial Neural Networks:

- Mathematical model for learning inspired by biological neural networks that constitute animal brains. It works by mapping inputs to outputs based on the structure and parameters of the network.
- Allows for learning the network's parameters based on data.

To model this in our computer, we'll use an artificial neuron known as a unit. Units can connect to each other in different ways to map outputs to inputs. The main goal of these units is to work together to solve a certain problem with a unique configuration of outputs to inputs.

## Neural Network Structure:

![nnStructure](images/5_NeuralNetworks/nnStructureLabeled.png)

This is similar to the idea of hypothesis and classification functions. The units on the left can be thought of as the inputs and the unit on the right can be thought of as the output.

We can use a simple neural network to implement the **or** function, for example.  
- _x_<sub>0</sub>(bias): -1
- _x_<sub>1</sub>: 1 
- _x_<sub>2</sub>: 0
- Weights: 1
- Step Classification Function _g_

![nnStructure](images/5_NeuralNetworks/nn-Or.png)

The input to _g_ can be simplified to _g_(-1 + 1(1) + 1(0)), or _g_(0) when we substitute the values of the weights. Then, _g_, or the step function evaluates the input value of 0 to the output value of 1(TRUE).

|x1|x2|g input|Output|
|--|--|-------|------|
|0 |0 |-1     |0     |
|1 |0 |0      |1     |
|0 |1 |0      |1     |
|1 |1 |1      |1     |

Similarly, if we wanted to implement a neural network to be able to function as **and**, we can change the bias to -2 instead of -1 so that 0 will only be reached if both _x_<sub>1</sub> and _x_<sub>2</sub> are 1.