from django.shortcuts import render


db = {
    "products": [
        {
            "id": 1,
            "name": "Молоко",
            "description": "Один из самых полезных для человека продуктов. Оно богато белком, витаминами A и D, кальцием. Недаром с давних пор люди стали не только покупать молоко оптом, но и придумывать рецепты изготовления из него разных продуктов.",
            "price": 100
        },
        {
            "id": 2,
            "name": "Творог",
            "description": "Он производится из пастеризованного молока, в которое добавляют закваску, после чего через некоторое время из образовавшейся зернистой массы удаляют сыворотку. Творог необычайно богат белком, витаминами группы В и незаменим в диетическом питании.",
            "price": 80
        },
        {
            "id": 3,
            "name": "Сливки",
            "description": "Изготавливаются с древнейших времен и представляют собой верхний, самый жирный слой отстоявшегося молока. Они очень калорийны и питательны, насыщены витаминами А, D и Е.",
            "price": 200
        },
        {
            "id": 4,
            "name": "Сметана",
            "description": "Получается из сливок путем добавления специальной закваски. Особенно популярна она в кухне славянских народов. Сметана богата белком и жирами, содержит витамины А, Е, В12.",
            "price": 50
        },
        {
            "id": 5,
            "name": "Кефир",
            "description": "Производится с помощью особого кефирного грибка. Очень полезен для здоровья, так же как и другие кисломолочные напитки (простокваша, ряженка, варенец, ацидофилин, мацони и т. д.).",
            "price": 120
        }
    ]
}


def getProducts():
    return db["products"]


def getProductById(product_id):
    for product in db["products"]:
        if product["id"] == product_id:
            return product


def searchProducts(product_name):
    products = getProducts()

    res = []

    for product in products:
        if product_name.lower() in product["name"].lower():
            res.append(product)

    return res


def index(request):
    query = request.GET.get("query", "")
    products = searchProducts(query)

    context = {
        "products": products,
        "query": query
    }

    return render(request, "home_page.html", context)


def product(request, product_id):
    context = {
        "id": product_id,
        "product": getProductById(product_id),
    }

    return render(request, "product_page.html", context)

