import csv
import sys
import pandas as pd

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
    data = []

    #load data from file into data:a list of dict corresponding to each row in the file
    with open("shopping.csv") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            data.append(
                {
                    "evidence": [cell for cell in row[:17]],
                    "label": 1 if row[17] == "TRUE" else 0
                }
            )

    #create lists of evidence and labels
    evidence = [row["evidence"] for row in data]
    labels = [row["label"] for row in data]

    #list to change the values of each row
    intIndex = [0,2,4,10,11,12,13,14,15,16]
    floatIndex = [1,3,5,6,7,8,9]
    months = ["Jan","Feb","Mar","Apr","May","June","Jul","Aug","Sep","Oct","Nov","Dec"]

    for eachRow in evidence:
        #convert administrative, informational etc col to integers
        for i in intIndex:
            #convert to equivalent number for month
            if i == 10:
                for mon in months:
                    if eachRow[i] == mon:
                        eachRow[i] = months.index(mon)
            
            #insert 1 if Returning visitior else 0
            elif i == 15:
                if eachRow[i] == "Returning_Visitor":
                    eachRow[i] = 1
                else:
                    eachRow[i] = 0
            
            #insert 1 if weekend = True else 0
            elif i == 16:
                if eachRow[i] == "True":
                    eachRow[i] = 1
                else:
                    eachRow[i] = 0
            else:
                eachRow[i] = int(eachRow[i])

        #convert cols like bounce rates, exit rates etc to float 
        for i in floatIndex:
            eachRow[i] = float(eachRow[i])
            

    return (evidence,labels)



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    #train a k-nearest neighbor classifier with k = 1
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)

    return model


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
    sensitivity = 0.0
    specificity = 0.0

    #create pandas series
    labels = pd.Series(labels,name="Labels")
    predictions = pd.Series(predictions,name="Predictions")

    #creating a dataframe representing the confusion matrix
    confusionMatrix = pd.crosstab(predictions,labels)

    truePositives = confusionMatrix.iloc[1,1]
    trueNegatives = confusionMatrix.iloc[0,0]
    falsePositives = confusionMatrix.iloc[0,1]
    falseNegatives = confusionMatrix.iloc[1,0]

    sensitivity = truePositives / (truePositives + falseNegatives)
    specificity = trueNegatives / (trueNegatives + falsePositives)

    return (sensitivity,specificity)

if __name__ == "__main__":
    main()
