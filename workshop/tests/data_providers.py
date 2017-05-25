from model.product import Product

products_to_buy = [
    (
        Product(name="Yellow Duck", quantity=1, size="Large"),
    ),
    (
        Product(name="Yellow Duck", quantity=1, size="Small"),
        Product(name="Green Duck", quantity=2),
        Product(name="Purple Duck", quantity=4)
    ),
    (
        Product(name="Red Duck", quantity=7),
        Product(name="Yellow Duck", quantity=2, size="Medium"),
        Product(name="Blue Duck", quantity=3)
    ),
    # ...
]