import pandas as pd
import acquire as a

def prepare():
    
    df = a.get_telco_data()
    
    drop_list = ['Unnamed: 0']
    x = []

    for _id1 in df.columns:
        if '_id.1' in _id1:
            x.append(_id1)
        else:
            pass

    for xs in x:
        df.drop(columns=xs,inplace=True)


    for col in df.columns:
        if '_id' in col:
            df.drop(columns=col,inplace=True)

    for cols in df.columns:
            if '.1' in cols:
                df.drop(columns=cols,inplace=True)
            else:
                 pass
                
    df.drop(columns='Unnamed: 0',inplace=True)
    df.drop(columns='churn_month', inplace=True)

    encoded_values = {
        'Yes' : 1,
        'No'  : 0,
        'No phone service' : 0,
        'No internet service' : 0,
        'Male' : 1,
        'Female' : 0
    }

    df.replace(encoded_values,inplace=True)
    

    df.columns = ['is_male', 'senior_citizen', 'partner', 'dependents', 'tenure',\
           'phone_service', 'multiple_lines', 'online_security', 'online_backup',\
           'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies',\
           'paperless_billing', 'monthly_charges', 'total_charges', 'churn',\
           'internet_service_type', 'contract_type', 'payment_type',\
           'signup_date']
    df['total_charges'] = df['total_charges'].replace(' ', 0)
    df['total_charges'] = df['total_charges'].astype('float64')
    
    
    objects = []
    df.drop(columns='signup_date', inplace=True)
    for cols in df.columns:
        if df[cols].dtypes == 'O':
            objects.append(cols)
        else:
            pass


    df = pd.get_dummies(df, columns=objects, drop_first=True)

    df.columns = df.columns.str.lower().str.replace(' ','_')
	
	df['customer_id'] = (a.get_telco_data()).customer_id
    
    return df 



























def split(df):
    '''
    This function splits a dataframe into 
    train, validate, and test in order to explore the data and to create and validate models. 
    It takes in a dataframe and contains an integer for setting a seed for replication. 
    Test is 20% of the original dataset. The remaining 80% of the dataset is 
    divided between valiidate and train, with validate being .30*.80= 24% of 
    the original dataset, and train being .70*.80= 56% of the original dataset. 
    The function returns, train, validate and test dataframes. 
    '''
    train, test = train_test_split(df, test_size = .2, random_state=123)   
    train, validate = train_test_split(train, test_size=.3, random_state=123)
    
    return train, validate, test



