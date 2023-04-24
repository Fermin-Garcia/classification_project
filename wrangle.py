import pandas as pd
import acquire as a
from sklearn.model_selection import train_test_split


def get_connection():
    
    '''
    This function will return the link to access mysql database. 
    '''
    user=env.username
    password=env.password
    host=env.host
    db=env.db
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

    
# next we define the query that we are calling from sql 
query = '''select * 
from customers
left join internet_service_types using(internet_service_type_id)
left join contract_types using(contract_type_id)
left join payment_types using(payment_type_id)
left join customer_signups using (customer_id)
left join customer_churn using(customer_id)
left join customer_contracts using (customer_id)
left join customer_details using (customer_id)
left join customer_payments using (customer_id)
left join customer_subscriptions using (customer_id)
'''


# then we get this and use it to make a fucntion that 
# will check to see if a csv file containing the telco file named 
# telco.csv is it doesn't then the code will then run the query through 
# pymysql and cache the file locally so it is fastly accessiable 


def get_telco_data():
    if os.path.exists('telco.csv') == True:
        return pd.read_csv('telco.csv')
    else:
        df = pd.read_sql(query, get_connection())
        df.to_csv('telco.csv')
        return pd.read_csv('telco.csv')






# This function prepares data from a telco dataset by:
# - removing unnecessary columns and renaming them
# - encoding categorical values
# - converting total_charges column from string to float
# - creating dummy variables for categorical columns
# - adding a new column named 'customer_id'
# - returning the modified dataframe

def prepare():
    
    # Load the telco dataset
    df = a.get_telco_data()
    
    # Drop 'Unnamed: 0' column
    df.drop(columns='Unnamed: 0', inplace=True)
    
    # Drop columns with '_id' in their name
    for col in df.columns:
        if '_id' in col:
            df.drop(columns=col, inplace=True)
    
    # Drop columns with '.1' in their name
    for col in df.columns:
        if '.1' in col:
            df.drop(columns=col, inplace=True)
    
    # Drop 'churn_month' column
    df.drop(columns='churn_month', inplace=True)

    # Encode categorical values using a dictionary
    encoded_values = {
        'Yes' : 1,
        'No'  : 0,
        'No phone service' : 0,
        'No internet service' : 0,
        'Male' : 1,
        'Female' : 0
    }
    df.replace(encoded_values, inplace=True)

    # Rename columns for better readability
    df.columns = ['is_male', 'senior_citizen', 'partner', 'dependents', 'tenure',\
           'phone_service', 'multiple_lines', 'online_security', 'online_backup',\
           'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies',\
           'paperless_billing', 'monthly_charges', 'total_charges', 'churn',\
           'internet_service_type', 'contract_type', 'payment_type',\
           'signup_date']
    # Convert total_charges column from string to float
    df['total_charges'] = df['total_charges'].replace(' ', 0)
    df['total_charges'] = df['total_charges'].astype('float64')

    # Create dummy variables for categorical columns
    df.drop(columns='signup_date',inplace=True)
    objects = []
    for col in df.columns:
        if df[col].dtypes == 'O':
            objects.append(col)
    
    df = pd.get_dummies(df, columns=objects, drop_first=True)

    # Rename columns to lower case and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ','_')

    # Add 'customer_id' column and return the modified dataframe
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
