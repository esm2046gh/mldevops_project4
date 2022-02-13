from sklearn import metrics
import commons_proj as cproj


#%% global variables & constants


#%% Functions
def score_model(real, predicted):
    # this function should take a trained model, load test data, and calculate 
    # an F1 score for the model relative to the test data
    # it should write the result to the latestscore.txt file
    f1_score = metrics.f1_score(real, predicted, zero_division=1)
    return f1_score

#%%
if __name__ == '__main__':
    # load test data
    test_data = cproj.load_dataframe('test_data_path', 'testdata.csv')
    # load the trained model
    model = cproj.load_object('output_model_path', 'trainedmodel.pkl')
    # prepare data for model
    X, y = cproj.prepare_data(test_data, cproj.input_features, cproj.output_feature)
    # predict
    predicted = model.predict(X)
    # score model
    f1_score = round(score_model(y, predicted), 7)
    # save score
    cproj.save_value(f1_score, 'output_model_path', 'latestscore.txt', True)