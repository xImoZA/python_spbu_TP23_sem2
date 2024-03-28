from collections import Counter
from src.Control_tests.control_test_1.task1 import *

import pytest

apple = Product("apple", 10.9, 4.99)
banana = Product("banana", 15.89, 4.99)
lemon = Product("lemon", 15.9, 4.99)


class TestBasket:
    @staticmethod
    @pytest.mark.parametrize(
        "products", [[(apple, 10)], [(apple, 10), (banana, 10)], [(apple, 5), (banana, 10), (lemon, 2)]]
    )
    def test_setitem(products: tuple) -> None:
        basket = Basket()
        for prod, count in products:
            basket[prod] = count

        assert Counter(basket.products.items()) == Counter(products)

    # @staticmethod
    # @pytest.mark.parametrize(
    #     "products, del_prod",
    #     [((apple, 10), apple), ([(apple, 10), (banana, 10)], banana), ([(apple, 5), (banana, 10), (lemon, 2)], lemon)])
    # def test_delitem(products, del_prod) -> None:
