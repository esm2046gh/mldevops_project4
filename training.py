from sklearn.linear_model import LogisticRegression
import commons_proj as cproj
#from scoring import score_model

#%% global variables & constants


#%% Functions

# Model training
def train_model(X, y):
    # Use this logistic regression for training
    model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    multi_class='auto', n_jobs=None, penalty='l2',
                    random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                    warm_start=False)
    
    #fit the logistic regression to your data
    model = model.fit(X, y)
    
    # predicted = model.predict(X)
    # f1_score = round(score_model(y, predicted), 7)
    
    return model #, f1_score

 
#%%
if __name__ == '__main__':
    fname = 'training.py'
    print(f"- {fname}. -->") 
    data = cproj.load_dataframe('output_folder_path', 'finaldata.csv')
    X, y = cproj.prepare_data(data, cproj.input_features, cproj.output_feature)
    model = train_model(X, y) #model, score_val = train_model(X, y)
    cproj.save_object(model, 'output_model_path', 'trainedmodel.pkl')
    #cproj.save_value(score_val, 'output_model_path', 'latestscore.txt')
    print(f"- {fname}. <--") 
 