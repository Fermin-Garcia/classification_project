#import the libraries we are working with 
import pandas as pd 
import os 
import env


# First we need to use our env file to access our mysql data base
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