import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

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
    # Create the evidence list and the labels list
    evidence = []
    labels = []
    
    # Open the CSV file
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        
        # Loop over each row
        for row in reader:
            # Loop over the first 17 elements (evidence)
            evidence_sublist = []
            # First five elements
            for i in range(5):
                evidence_sublist.append(int(row[i])) if i % 2 == 0 else evidence_sublist.append(float(row[i]))
            # Elements from 5 to 9       
            for i in range(5, 10):
                evidence_sublist.append(float(row[i]))
            # 10th element           
            evidence_sublist.append(MONTHS.index(row[10]))
            # Elements from 11 to 14
            for i in range(11, 15):
                evidence_sublist.append(int(row[i]))
            # Elements 15 and 16
            evidence_sublist.append(1) if row[15] == "Returning_Visitor" else evidence_sublist.append(0)
            evidence_sublist.append(1) if row[16] == "TRUE" else evidence_sublist.append(0)
            
            # Insert the sublist of evidence in evidence
            evidence.append(evidence_sublist)
            
            # Labels list
            labels.append(1) if row[17] == "TRUE" else labels.append(0)
                
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positives = 0
    true_positives = 0
    negatives = 0
    true_negatives = 0
    
    for i in range(len(labels)):
        if labels[i] == 1:
            positives += 1
            if labels[i] == predictions[i]:
                true_positives += 1      
        else:
            negatives += 1
            if labels[i] == predictions[i]:
                true_negatives += 1

    # Sencitivity
    sensitivity = true_positives / positives
    # Specificity
    specificity = true_negatives / negatives
    
    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
