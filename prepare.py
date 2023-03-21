import pandas as pd

def prepare_telco(df):
    customer_id = df['customer_id']
 
    id_list = []
    my_object_list = []
    for cols in df.columns:
        if '.1' in cols:
            id_list.append(cols)
        else:
             pass

    # total charges are not in this list my hunch is that it is in the object section.

    # block two:
    # in the next few block we are generatring a list of columns we dont want so we can drop them at the end  
    for cols in df.columns:       
            if '_id' in cols:
                id_list.append(cols)
            else:
                pass



    # block two is also not the issue, as ttotal charges also dont appear in this list 

    #block three: 

    # Here we are adding more columns to the list of col¨mns to be dropped. 
    id_list.append('Unnamed: 0')
    #(df['churn_month'].isnull().sum()) / (len(df['churn_month']))
    id_list.append('churn_month')
    id_list.append('customer_id')
    id_list.append('signup_date')
    df = df.drop(columns=id_list)
    change_values = {
        'No phone service' : 0,
        'Male': 1,
        'Female': 0,
        'no' : 0,
        'No' : 0,
        'Yes' : 1,
        'No internet service': 0
    }
    df.columns
    df = df.rename(columns = {'gender': 'sex_male'})
    df = df.replace(change_values)
    df.total_charges = df['total_charges'].replace(' ', 0)
    df.total_charges = df['total_charges'].astype('float64')
    
    
    
    for cols in df.columns:
        if df[cols].dtype == 'O':
            my_object_list.append(cols)
        else:
           pass
    
    get_dummy_vales = (pd.get_dummies(df[my_object_list]))
    df = pd.concat([df, get_dummy_vales], axis=1)
    df = df.drop(columns=my_object_list)
    new_order =['sex_male', 'senior_citizen', 'partner', 'dependents', 'tenure',
       'phone_service', 'multiple_lines', 'online_security', 'online_backup',
       'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies',
       'paperless_billing', 'monthly_charges', 'total_charges', 
       'internet_service_type_dsl', 'internet_service_type_fiber_optic',
       'internet_service_type_none', 'contract_type_month-to-month',
       'contract_type_one_year', 'contract_type_two_year',
       'payment_type_bank_transfer_(automatic)',
       'payment_type_credit_card_(automatic)', 'payment_type_electronic_check',
       'payment_type_mailed_check','churn']
    df.columns = new_order
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    concat_cols = [customer_id,df]
    p_df = pd.concat(concat_cols, axis=1)
    
    return df




























def split_data(df):
    from sklearn.model_selection import train_test_split
    train_validate, test = train_test_split(df, test_size=.7, random_state=123, stratify=df.churn)
    train, validate = train_test_split(train_validate, 
                                       test_size=.3, 
                                       random_state=123, 
                                       stratify=train_validate.churn)
    return train, validate, test


my_list = ['tenure', 'monthly_charges', 'total_charges',
       'internet_service_type_fiber_optic', 'churn', ]


data_dict = {
    'tenure' : 'The number of months the customer has been with the provider',
    'monthly_charges' : 'the total charges for the month',
    ' total_charges' : 'the total charges to the customer',
    ' internet_service_type_fiber_optic' : ' bool values to repersent if the customer does have fiber optic' ,
    'churn' : 'Bool value to repersent the customers who leave'
}

