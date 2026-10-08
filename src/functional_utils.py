def filter_sales_by_category(sales, category):
    return list(filter(lambda s: s.category == category, sales))