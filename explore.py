def X_and_y_split(train, validate, test):
    feature_list = ['contract_type_one_year', 'contract_type_two_year', 'monthly_charges', 'total_charges', 'churn']
    X_train = train[feature_list].drop(columns='churn')
    y_train = train['churn']
    ########################## Now we do the same with validate and test ################################
    X_validate = validate[feature_list].drop(columns='churn')
    y_validate = validate['churn']
    ######################### Now to test ###############################################################
    X_test = test[feature_list].drop(columns='churn')
    y_test = test['churn']
    
    return X_train, y_train, X_validate, y_validate, X_test, y_test