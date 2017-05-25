import pytest
from .data_providers import products_to_buy

@pytest.mark.parametrize("items", products_to_buy)
def test_shopping_cart(app, items):
    list_to_buy = [x for x in items]

    app.add_products_to_card(list_to_buy)
    app.clear_shopping_cart()
