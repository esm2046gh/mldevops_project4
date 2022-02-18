import os
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import commons_proj as cproj
from diagnostics import model_predictions




#%% Function for reporting

def score_model():
    test_data = cproj.load_dataframe('test_data_path', 'testdata.csv')
    predicted, y_test = model_predictions(test_data)
    
    #calculate a confusion matrix 
    cm = confusion_matrix(y_test, predicted)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    #plt.show()
    
    #write the confusion matrix to the workspace
    file_path = os.path.join(os.getcwd(), cproj.config['output_model_path'], 'confusionmatrix.png')
    plt.title('Confusion Matrix. Attrition Risk')
    plt.ylabel('Real')
    plt.xlabel('Predicted')
    plt.savefig(file_path)

if __name__ == '__main__':
    score_model()
