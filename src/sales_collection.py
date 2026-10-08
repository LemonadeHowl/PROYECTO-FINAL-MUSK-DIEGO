class SalesCollection:
    def __init__(self, sales):
        self.sales = sales

    def sales_by_client(self, client_id):
        total_sales = []
        for sale in self.sales:
            if sale.client_id == client_id:
                total_sales.append(sale)
        return total_sales

    def sales_by_category(self, category):
        lista_category = []
        for sale in self.sales:
            if sale.category == category:
                lista_category.append(sale)
        return lista_category

                
    def total_amount_by_client(self, client_id):
        client_sales = self.sales_by_client(client_id)
        amounts = []
        for sale in client_sales:
            amounts.append(sale.amount)
        return sum(amounts)

    def total_amount_by_category(self, category):
        client_category  = self.sales_by_category(category)
        amounts = []
        for sale in client_category:
            amounts.append(sale.amount)
        return sum(amounts)

    def average_sale_by_client(self, client_id):
        count = len(self.sales_by_client(client_id))
        if count == 0:
            return 0.0
        total = self.total_amount_by_client(client_id)
        return round(total / count, 2)
            



    