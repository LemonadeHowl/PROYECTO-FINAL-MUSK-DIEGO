import json
from pathlib import Path
import pandas as pd
from datetime import datetime
from src.client import Client
from src.sale import Sale
from src.sales_collection import SalesCollection
from src.client_collection import ClientCollection
from src.functional_utils import filter_sales_by_category

# Rutas de las carpetas necesarias.
root_dir = Path(__file__).parent.parent
data_dir = root_dir / 'data'

# Funciones que ayudan a posteriori.

def load_clients():
    path = data_dir / 'clients.json'
    with open (path, encoding='utf-8') as f:
        datos = json.load(f)

    clients = []
    for d in datos:
        clients.append(Client(**d))
    return clients 

def load_df():
    path = data_dir / 'sales.csv'
    df = pd.read_csv(path)
    return df

def load_sales():
    df = load_df()
    sales = []
    for row in df.itertuples():
        sale = Sale(row.sale_id, row.client_id, row.product, row.category, row.amount, row.date, )
        sales.append(sale)
    return sales

# Report.
def generate_report():
    clients = load_clients()
    sales = load_sales()
    df = load_df()

    summary = {
        'total_clients' : total_clients(),
        'total_sales' : total_sales(),
        'total_revenue' : total_revenue(),
            }

    return {
        'summary' : summary,
        'clients' : clients_report(clients, sales),
        'top_client_by_country' : top_client_by_country(clients, sales),
        'sales_by_category' : sales_by_category(df),
        'high_spending_clients' : high_spending_clients(clients, sales),
        'monthly_sales' : monthly_sales(df)
    
    }


# 1. Número total de clientes.

def total_clients():
    clients = load_clients()
    return len(clients)

# 2. Número total de ventas.

def total_sales():
    sales = load_sales()
    return len(sales)

# 3. Total ingresos por cliente.

def total_revenue():
    sales = load_sales()
    total = 0
    for sale in sales:
            total = total + sale.amount
    return total 

#  4 y 5. Número de ventas por cliente.

def clients_report(clients, sales):
    collection = SalesCollection(sales)
    report = []

    for client in clients:
        client_id = client.client_id
        report.append({
            'client_id': client_id,
            'name': client.name,
            'total_spent': collection.total_amount_by_client(client_id),
            'sale_count': len(collection.sales_by_client(client_id)),
            'average_sale': collection.average_sale_by_client(client_id),
        })

    return report

# 6. Cliente con mayor gasto por país.

def top_client_by_country(clients, sales):
    collection_clients = ClientCollection(clients)
    collection_sale = SalesCollection(sales)
    report = {}

    countries = set(client.country for client in clients)

    for country in countries:
        clients_in_country = collection_clients.clients_by_country(country)
        best_client = None
        best_total = -1

        for client in clients_in_country:
            total = collection_sale.total_amount_by_client(client.client_id)
            if total > best_total:
                best_total = total
                best_client = client.name

        report[country] = best_client

    return report

# 7. Total de ventas por categoría:

def sales_by_category(df):
    report = df.groupby('category')['amount'].sum().round(2).to_dict()

    return report
    
# 8. Cliente con más ventas en una categoría específica. No aparece en el report porque en 
#       la guía no había ninguna clave para ello.

def more_sales_by_category(clients, sales, category):
    sales_category = filter_sales_by_category(sales, category)
    collection = SalesCollection(sales_category)
    report = {}
    best_client = None
    best_count = -1

    for client in clients:
        count = len(collection.sales_by_category(category))
        
        if count > best_count:
            best_count = count
            best_client = client.name

    report[category] = best_client 

    return report

# 9. Clientes que superan un gasto minimo de 500€.

def high_spending_clients(clients, sales):
    collection = SalesCollection(sales)
    spending = []

    for client in clients:
        if collection.total_amount_by_client(client.client_id) > 500:
            spending.append(client.name)

    return spending  

# 10. Ventas acumuladas mes a mes.

def monthly_sales(df):
    dates = pd.to_datetime(df['date'])
    month = dates.dt.to_period('M').astype(str)
    report = df.groupby(month)['amount'].sum().round(2).to_dict()

    return report

# Para ver el report.

print(generate_report())

# Para crear el final_report.

# Guardar el informe en JSON.

def save_report(report, filename='final_report.json'):
    path = root_dir / filename
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    return path

