import pytest
from .data_providers import items_to_buy

@pytest.mark.parametrize("items", list(items_to_buy))
def test_shopping_cart(app, items):
    app.add_products_to_card(items)
    app.clear_shopping_cart()
