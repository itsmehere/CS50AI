# Machine Learning - CS50AI Lecture 4

Machine learning is the study of computer algorithms that improve automatically through experience.

## Supervised Learning:

Given a data set of input-output pairs, learn a function to map inputs to outputs.

## Classification:

Supervised learning task of learning a function mapping an input point to a dicrete category. For example, if we wanted to figure out whether it was going to rain tomorrow, based on past experiences/data, the computer should be able to draw reasonable conclusions. We have already taken a look at how to approach similar problems using probability but we won't always have definite probabilities that we use. Machine learning algorithms focus more on the idea of using historical data instead. An example of historical data could be the following:  
[Markdown Table Generator](https://github.com/itsmihirrao/MarkdownTableGenerator)

|Date     |Humidity|Pressure|Rain   |
|---------|--------|--------|-------|
|January 1|93%     |999.7   |Rain   |
|January 2|49%     |1015.5  |No Rain|
|January 3|79%     |1031.1  |No Rain|
|January 4|65%     |984.9   |Rain   |
|January 5|90%     |975.2   |Rain   |

What we would like to do is write a function _f_ that can predict something based on a certain input (_humidity_, _pressure_). 

```
f(humidity, pressure)
```
PREDICT:
```
f(93, 999.7) = Rain
f(49, 1015.5) = No Rain
f(79, 1031.1) = No Rain
```

Since we don't know exactly how _f_ works, we can write a _hypothesis_ function that does the same thing as _f_. _f_ and _h_ can then check each other's values for more reliable results.

### 2D Graphs:

One approach we can use to predict, in our case, `rain` or `no rain` would be to graph the data points. With `humidity` on the _x_ axis and `pressure` on the _y_ axis, we can first graph all the data points where it did rain.

![graph1](images/4_Learning/graph1.png)

Then, we can do the same for all the data points where it didn't rain.

![graph1](images/4_Learning/graph2.png)

### Nearest-Neighbor Classification:

Algorithm that, given an input, chooses the class of the nearest data point to that input. This algorithm, like most, has its downsides. When outliers exist in a data set, it won't always choose what is most appropriate. In the case below, us humans would probably agree that given the humidity and pressure of the white dot, it will rain. However, the computer will choose the closest data point, in this case, not raining.

![graph1](images/4_Learning/nnAlgorithm.png)

### _k_-Nearest-Neighbor Classification:

Algorithm that, given an input, chooses the most common class out of the _k_ nearest data points to that input. This is a much better approach because it takes into consideration "location" of the data point and doesn't reach conclusions based on just one neighbor. However, this algrithm also has a few downsides:

- It could be slow to go through every neighbor and measure distance(there are optimizations).
  - Data pruning
  - Data structures
  - Select relevant data

## Data Boundaries:

Another way to approach classification is to look at all the data and somehow come up with a decision boundary. In the case of two dimensions, we can draw a line that separates the rainy days from the non-rainy days.

![linearRegression](images/4_Learning/linearRegression.png)

Obviously, data sets will never be this clean. There are usually outliers and other factors that will pollute the data. We still want to be able to draw boundaries but these boundaries may not always be linear.

_x<sub>1</sub>_ = Humidity  
_x<sub>2</sub>_ = Pressure

_h_(_x<sub>1</sub>_, _x<sub>2</sub>_) = 1 if _w<sub>0</sub>_ + _w<sub>1</sub>x<sub>1</sub>_ + _w<sub>2</sub>x<sub>2</sub>_ ≥ 0.
0 _otherwise_

Where:
-  _w_'s are weights that determine the boundary
-  1 : Rain
-  0 : No Rain

The dot product of the following vectors represent the same idea:

Weight Vector: **w**:(_w<sub>0</sub>_, _w<sub>1</sub>_, _w<sub>2</sub>_)  
Input Vector: **x**:(1, _x<sub>1</sub>_, _x<sub>2</sub>_)  
**w** * **x**: _w<sub>0</sub>_ + _w<sub>1</sub>x<sub>1</sub>_ + _w<sub>2</sub>x<sub>2</sub>_

Then, we can later simplify the hypothesis function to look a little something like this:

_h_<sub>**w**</sub>(_X_) = 1 if **w** * **x** ≥ 0. 0 otherwise.

Now, the big question is how to determine the values of the weights. For this, we can use a technique known as perceptron learning rule.

## Perceptron Learning Rule:

Given data point (_**x**_, _**y**_), update each weight according to:
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?w_i%20=%20w_i%20+%20\alpha%20(y%20-%20h_w(X))%20*%20x_i">
</p>

More generally, this formula states:
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?w_i%20=%20w_i%20+%20\alpha%20(actual%20-%20estimate)%20*%20x_i">
</p>

If the actual value was equal to the value we predicted, then the right side of the expression would equal 0 and the weight wouldn't change. If the actual value was greater than our predicted value(_actual - estimate > 0_), we would increase the weight so the value of the dot product goes up. However, if the actual value was lower than the predicted value(_actual - estimate < 0_), we would decrease the weight so the value of the dot product goes down. This is one way we can teach the computer to "learn" and choose the appropriate boundaries.

### Hard & Soft Threshold:

One problem with our function is that it will always choose rain or no rain. In some cases, this may be what we want but if a data point is close the boundaries, it may not make sense to make such a definite conclusion. Looking at the image below, we see that if the value resulting from the dot product is barely to the right of the vertical line(the threshold), we strongly conclude a value of 1.

![hardThreshold](images/4_Learning/hardThreshold.png)

To represent this more logically, we can use soft thresholds instead.

![hardThreshold](images/4_Learning/softThreshold.png)

Now, as the output from the dot product gets larger and larger, we can conclude the outcome with more certainty. In other words, the output isn't restricted to either 1 or 0 and this allows to express likeliness and probability.

## Support Vector Machines:

### Maximum Margin Separator:

Boundary that maximizes the distance between any of the data points. In some cases, drawing boundaries may be rather aribtrary. For example, there isn't always just 1 way you can draw a line between data points and this ultimately leads to other problems:

- Data points for whom we want to predict the outcome could be really close to both data sets.
- This makes predicting outcomes hard.

To solve this issue, we can draw our line based on the idea of a **maximum margin separator** that will position the boundary as far away from the data points as possible.

Example:

![example](images/4_Learning/separator-example.png)

### Regression:

**Supervised learning task of learning a function mapping an input point to a continuous value.** Instead of creating boundaries, we can try to find the line of best fit and use that as a refernce to determine the result.

## Loss Functions:

Function that expresses how poorly our hypothesis performs.

### 0-1 Loss Function:

_L_(actual, predicted) = 0 if actual = predicted, 1 otherwise

### L<sub>1</sub> Loss Function:

**_L_(actual, predicted) = |actual - predicted|**. We can use this to find the line of best fit. The less loss, the more accurate our predictions will be.

![lossL1](images/4_Learning/lossL1.png)

### L<sub>2</sub> Loss Function:

**_L_(actual, predicted) = (actual - predicted)<sup>2</sup>**. This version penalizes outliers more harshly.

## Overfitting:

A model that fits too closely to a particular data set and therefore may fail to generalize to future data.

![overfitting](images/4_Learning/overfitting.png)

Sometimes, a boundary that has a loss is better than a boundary that has no loss.

## Cost:

With the cost function below, we run into the problem of overfitting.

_cost(h)_ = _loss(h)_

To fix this, we must introduce some other aspect to the cost function so that we don't end up drawing a boundary that exactly matches the data. One thing we can add is _complexity(h)_ that determines how complicated our boundary is. We would rather give precedence to something simpler rather than something complex. The new cost function could be written as follows:

_cost(h)_ = _loss(h)_ + _complexity(h)_

## Regularization:

Penalizing hypotheses thar are more complex to favor simpler, more general hypotheses.

In the above equation, we would like to penalize boundaries that are complex more than boundaries that are less complex.

_cost(h)_ = _loss(h)_ + _**λ**complexity(h)_

With this, we can represent the idea that if λ is larger, then we want to penalize that complexity more but if λ is smaller, then we want to penalize the complexity less.

## Holdout Cross-Validation:

Splitting data into a training set and a test set, such that learning happens on the training set and is evaluated on the test set.

## _k_-Fold Cross-Validation:

Splitting data into _k_ sets, and experimenting _k_ times, using each set as a test set once, and using remaining data as training set.