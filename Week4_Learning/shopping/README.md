# Shopping

An AI to predict whether online shopping customers will complete a purchase.

## Background:

When users are shopping online, not all will end up purchasing something. Most visitors to an online shopping website, in fact, likely don’t end up going through with a purchase during that web browsing session. It might be useful, though, for a shopping website to be able to predict whether a user intends to make a purchase or not: perhaps displaying different content to the user, like showing the user a discount offer if the website believes the user isn’t planning to complete the purchase. How could a website determine a user’s purchasing intent? That’s where machine learning will come in. Given information about a user — how many pages they’ve visited, whether they’re shopping on a weekend, what web browser they’re using, etc. — the classifier will predict whether or not the user will make a purchase.

## Sensitivity and Specificity:

How do we measure the accuracy of a system like this? If we have a testing data set, we could run our classifier on the data, and compute what proportion of the time we correctly classify the user’s intent. This would give us a single accuracy percentage. But that number might be a little misleading. Imagine, for example, if about 15% of all users end up going through with a purchase. A classifier that always predicted that the user would not go through with a purchase, then, we would measure as being 85% accurate: the only users it classifies incorrectly are the 15% of users who do go through with a purchase. And while 85% accuracy sounds pretty good, that doesn’t seem like a very useful classifier.

Instead, we’ll measure two values: sensitivity (also known as the “true positive rate”) and specificity (also known as the “true negative rate”). Sensitivity refers to the proportion of positive examples that were correctly identified: in other words, the proportion of users who did go through with a purchase who were correctly identified. Specificity refers to the proportion of negative examples that were correctly identified: in this case, the proportion of users who did not go through with a purchase who were correctly identified. So our “always guess no” classifier from before would have perfect specificity (1.0) but no sensitivity (0.0). Our goal is to build a classifier that performs reasonably on both metrics.

[Read more here](https://en.wikipedia.org/wiki/Sensitivity_and_specificity)

## Understanding:

First, open up `shopping.csv`, the data set for this project. You can open it in a text editor, but you may find it easier to understand visually in a spreadsheet application like Microsoft Excel, Apple Numbers, or Google Sheets.

There are about 12,000 user sessions represented in this spreadsheet: represented as one row for each user session. The first six columns measure the different types of pages users have visited in the session: the `Administrative`, `Informational`, and `ProductRelated` columns measure how many of those types of pages the user visited, and their corresponding `_Duration` columns measure how much time the user spent on any of those pages. The `BounceRates`, `ExitRates`, and `PageValues` columns measure information from [Google Analytics](https://analytics.google.com/analytics/web/provision/#/provision) about the page the user visited. `SpecialDay` is a value that measures how closer the date of the user’s session is to a special day (like Valentine’s Day or Mother’s Day). `Month` is an abbreviation of the month the user visited. `OperatingSystems`, `Browser`, `Region`, and `TrafficType` are all integers describing information about the user themself. `VisitorType` will take on the value `Returning_Visitor` for returning visitors and some other string value for non-returning visitors. `Weekend` is `TRUE` or `FALSE` depending on whether or not the user is visiting on a weekend.

Perhaps the most important column, though, is the last one: the `Revenue` column. This is the column that indicates whether the user ultimately made a purchase or not: `TRUE` if they did, `FALSE` if they didn’t. This is the column that we’d like to learn to predict (the “label”), based on the values for all of the other columns (the “evidence”).

Next, take a look at `shopping.py`. The `main` function loads data from a CSV spreadsheet by calling the `load_data` function and splits the data into a training and testing set. The `train_model` function is then called to train a machine learning model on the training data. Then, the model is used to make predictions on the testing data set. Finally, the `evaluate` function determines the sensitivity and specificity of the model, before the results are ultimately printed to the terminal.

## Usage:

`python shopping.py shopping.csv`

## Other Links:

Read more about cs50ai [here](https://cs50.harvard.edu/ai/2020/)   
[Original Problem Page](https://cs50.harvard.edu/ai/2020/projects/4/shopping/)

## Acknowledgements

Data set provided by [Sakar, C.O., Polat, S.O., Katircioglu, M. et al. Neural Comput & Applic (2018)](https://link.springer.com/article/10.1007%2Fs00521-018-3523-0) 