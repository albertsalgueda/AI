import csv
import sys
from time import strptime
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

# python3 shopping.py shopping.csv

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
        0 Administrative, an integer 
        1 Administrative_Duration, a floating point number
        2 Informational, an integer
        3 Informational_Duration, a floating point number
        4 ProductRelated, an integer
        5 ProductRelated_Duration, a floating point number
        
        6 BounceRates, a floating point number
        7 ExitRates, a floating point number
        8 PageValues, a floating point number
        9 SpecialDay, a floating point number
        
        10 Month, an index from 0 (January) to 11 (December)
        
        11 OperatingSystems, an integer
        12 Browser, an integer
        13 Region, an integer
        14 TrafficType, an integer
        
        15 VisitorType, an integer 0 (New_Visitor) or 1 (Returning_Visitor)
        16 Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    def monthtonum(month):
        if month == 'Jan':
            num = 0
        elif month == 'Feb':
            num = 1
        elif month == 'Mar':
            num = 2
        elif month == 'May':
            num = 4
        elif month == 'Jun':
            num = 5
        elif month == 'Jul':
            num = 6
        elif month == 'Aug':
            num = 1
        elif month == 'Sep':
            num = 1
        elif month == 'Oct':
            num = 1
        elif month == 'Dec':
            num = 1
        else:
            return 3
        return num
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        data = []
        for row in reader:
            data.append({
                "evidence": [str(cell) for cell in row[0:len(row)-1]],
                "label": 1 if row[-1:0] == "TRUE" else 0
            })
        #print(data[0]['evidence'])
        #data type transformation
        for i in range(len(data)):
            data[i]['evidence'][0] = int(data[i]['evidence'][0])
            data[i]['evidence'][1] = float(data[i]['evidence'][1])
            data[i]['evidence'][2] = int(data[i]['evidence'][2])
            data[i]['evidence'][3] = float(data[i]['evidence'][3])
            data[i]['evidence'][4] = int(data[i]['evidence'][4])
            data[i]['evidence'][5] = float(data[i]['evidence'][5])
            data[i]['evidence'][6] = float(data[i]['evidence'][6])
            data[i]['evidence'][7] = float(data[i]['evidence'][7])
            data[i]['evidence'][8] = float(data[i]['evidence'][8])
            data[i]['evidence'][9] = float(data[i]['evidence'][9])
            #ojo el mes 
            data[i]['evidence'][10] = monthtonum(data[i]['evidence'][10])
            data[i]['evidence'][11] = int(data[i]['evidence'][11])
            data[i]['evidence'][12] = int(data[i]['evidence'][12])
            data[i]['evidence'][13] = int(data[i]['evidence'][13])
            data[i]['evidence'][14] = float(data[i]['evidence'][14])
            data[i]['evidence'][15] = 1 if data[i]['evidence'][15] == 'Returning_Visitor' else False
            data[i]['evidence'][16] = True if data[i]['evidence'][16] == 'TRUE' else False
                
                
    #print(data[0])
    print('completed')
    return(tuple(data['evidence'],data['labels']))


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
