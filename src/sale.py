class Sale:
    def __init__(self, sale_id, client_id : int, product: str, category: str, amount: int, date: str):
        self.sale_id = str(sale_id)
        self.client_id = int(client_id)
        self.product = str(product)
        self.category = str(category)
        self.amount = int(amount)
        self.date = str(date)

    def to_dict(self):
        return {
            'sale_id': self.sale_id,
            'client_id': self.client_id,
            'product': self.product,
            'category': self.category,
            'amount': self.amount,
            'date': self.date
        }