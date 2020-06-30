import csv
import sys
import calendar

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    NUMCOLS = 18
    evidence = []
    labels = []

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    with open(filename, 'r') as f:
        csvReader = csv.reader(f)
        header = next(csvReader)

        if header != None:
            for row in csvReader:
                userEvidence = []

                for i in range(0, NUMCOLS - 1):
                    # Columns where the type should be int: Administrative, Informational, ...
                    intIndexes = [0, 2, 4, 10, 11, 12, 13, 14, 15, 16]
                    # Columns where the type should be float: Administrative_Duration, Informational_Duration, ...
                    floatIndexes = [1, 3, 5, 6, 7, 8, 9]

                    if i in intIndexes:
                        # If the column is Month
                        if i == 10:
                            userEvidence.append(months.index(row[i]))
                        # If the column is VisitorType
                        elif i == 15:
                            userEvidence.append(visitorToInt(row[i]))
                        # If the column is Weekend
                        elif i == 16:
                            userEvidence.append(boolToInt(row[i]))
                        else:
                            # Cast to int
                            userEvidence.append(int(row[i]))
                    elif i in floatIndexes:
                        # Cast to float
                        userEvidence.append(float(row[i]))

                evidence.append(userEvidence)
                labels.append(boolToInt(row[NUMCOLS - 1]))

    # Return tuple of evidence and labels
    return (evidence, labels)


def boolToInt(boolVal):
    if boolVal == "TRUE":
        return 1
    else:
        return 0


def visitorToInt(visitor):
    if visitor == "Returning_Visitor":
        return 1
    else:
        return 0


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
