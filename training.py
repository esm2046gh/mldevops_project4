from sklearn.linear_model import LogisticRegression
import commons_proj as cproj

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
    
    return model

 
#%%
if __name__ == '__main__':
    data = cproj.load_dataframe('output_folder_path', 'finaldata.csv')
    X, y = cproj.prepare_data(data, cproj.input_features, cproj.output_feature)
    model = train_model(X, y)
    cproj.save_object(model, 'output_model_path', 'trainedmodel.pkl')
 