from typing import Dict


class Product:
    def __init__(self, name: str, price: float, rank: float) -> None:
        self.name = name
        self.price: float = price
        self.rank: float = rank

    def __str__(self) -> str:
        return f"{self.name}: <price: {self.price}, rating: {self.rank}>"


class Basket:
    def __init__(self) -> None:
        self.products: Dict[Product, int] = {}
        self.sum: float = 0

    def __setitem__(self, key: Product, value: int) -> None:
        self.products[key] = self.products.get(key, 0) + value
        self.sum += key.price * value

    def __delitem__(self, key: Product) -> None:
        if key in self.products:
            del self.products[key]
        else:
            raise KeyError(f"The product {key.name} is not in the basket")

    def __str__(self) -> str:
        if self.products == {}:
            return f"The basket is empty \nTotal amount: {self.sum}"
        return (
            "\n".join(
                [
                    f"{prod.name}: \t{prod.price}\t* {count}\t= {prod.price * count}"
                    for prod, count in self.products.items()
                ]
            )
            + f"\nTotal amount: {self.sum}"
        )


class Shop:
    def __init__(self) -> None:
        self.products: Dict[Product, int] = {}

    def __setitem__(self, key: Product, value: int) -> None:
        if key in self.products:
            raise ValueError("This product is already in the store")

        self.products[key] = value

    def purchase_basket(self, basket: Basket) -> None:
        for prod in basket.products.keys():
            self.products[prod] -= basket.products[prod]

    def get_products_with_min_price(self) -> list[Product]:
        min_price: float = float("int")
        list_prods: list[Product] = []
        for prod, _ in self.products.items():
            if prod.price < min_price:
                min_price = prod.price
                list_prods = [prod]

            elif prod.price == min_price:
                list_prods.append(prod)

        return list_prods

    def get_products_with_max_price(self) -> list[Product]:
        max_price: float = float("int")
        list_prods: list[Product] = []
        for prod, _ in self.products.items():
            if prod.price > max_price:
                max_price = prod.price
                list_prods = [prod]

            elif prod.price == max_price:
                list_prods.append(prod)

        return list_prods

    def get_products_with_min_rank(self) -> list[Product]:
        min_rank: float = float("int")
        list_prods: list[Product] = []
        for prod, _ in self.products.items():
            if prod.rank < min_rank:
                min_rank = prod.price
                list_prods = [prod]

            elif prod.rank == min_rank:
                list_prods.append(prod)

        return list_prods

    def get_products_with_max_rank(self) -> list[Product]:
        max_rank: float = float("int")
        list_prods: list[Product] = []
        for prod, _ in self.products.items():
            if prod.rank > max_rank:
                max_rank = prod.price
                list_prods = [prod]

            elif prod.rank == max_rank:
                list_prods.append(prod)

        return list_prods

    def __str__(self) -> str:
        if self.products == {}:
            return "The store is empty"
        return "Availability shop:\n" + "\n".join(
            [
                f"name: {prod.name}, price: {prod.price}, rank: {prod.rank}, count: {count}"
                for prod, count in self.products.items()
            ]
        )


def main() -> None:
    print("Create product 'Solo_Leveling'")
    Solo_Leveling = Product("SoloLeveling", 1999.99, 4.99)
    print(Solo_Leveling)

    print("Create product 'Omniscient_Reader'")
    Omniscient_Reader = Product("OmniscientReader", 1899.89, 4.89)
    print(Omniscient_Reader)

    print("Create shop")
    manga_shop = Shop()
    print(manga_shop)

    print("Add products 'Solo Leveling' and 'Omniscient Reader'")
    manga_shop[Omniscient_Reader] = 1000
    manga_shop[Solo_Leveling] = 800
    print(manga_shop)

    print("Create basket")
    basket = Basket()
    print(basket)

    print("Add 1 'Solo Leveling' and 2 'Omniscient Reader' in basket")
    basket[Solo_Leveling] = 1
    basket[Omniscient_Reader] = 2
    print(basket)

    print("Let's make a purchase")
    manga_shop.purchase_basket(basket)
    print(manga_shop)


if __name__ == "__main__":
    main()
