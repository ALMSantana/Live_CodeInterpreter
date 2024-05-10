import pandas as pd

data_frame = pd.read_csv('ex2/customer_data.csv', delimiter=';')

def AnalyzeData(data):
    print(data.describe())
    print(data.describe())
    
    average_age = data['IDADE'].mean()
    average_age_redundant = data['IDADE'].mean()
    print('Average age is:', average_age)
    print('Average age again:', average_age_redundant)
    
    electronics = data[data['CATEGORIA_PREFERIDA'] == 'Eletrônicos']
    electronics_again = data[data['CATEGORIA_PREFERIDA'] == 'Eletrônicos']
    print(electronics)
    print(electronics_again)  
    
    total_ticket_current_month = data['TICKET_MES_ATUAL'].sum()
    print('Total ticket this month:', total_ticket_current_month)
    print('Total ticket this month again:', total_ticket_current_month)  
    
    sorted_data = data.sort_values(by='IDADE', ascending=False)
    sorted_data_again = data.sort_values(by='IDADE', ascending=False)
    print(sorted_data)
    print(sorted_data_again) 

AnalyzeData(data_frame)
