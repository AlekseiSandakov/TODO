import json

from falcon import Request, Response, HTTP_201, HTTP_400, HTTP_404


PRODUCTS = {
    1: "milk",
    2: "bacon",
    3: "bread",
}


class ProductsListResource:
    def on_get(self, req: Request, res: Response):
        products_as_list = [
            {"id": product_id, "product": product}
            for product_id, product in PRODUCTS.items()
        ]

        res.text = json.dumps(products_as_list)

    def on_post(self, req: Request, res: Response):
        media: dict = req.get_media()
        print(media)
        data: dict = json.loads(media["data"])
        print(data)
        try:
            product_id = int(data["id"])
            product = data["product"]
        except (ValueError, KeyError):
            res.status = HTTP_400
            result = {"message": "bad request"}
        else:
            if product_id in PRODUCTS:
                res.status = HTTP_400
                result = {"message": f"product with id #{product_id} already exists!"}
            else:
                PRODUCTS[product_id] = product
                res.status = HTTP_201
                result = {"id": product_id, "product": product}

        res.media = result


class ProductDetailsResource:
    def on_get(self, req: Request, res: Response, product_id: str):
        try:
            product_id = int(product_id)
            product = PRODUCTS[product_id]
        except ValueError:
            res.status = HTTP_400
            result = {"message": f"not valid id {product_id!r}"}
        except KeyError:
            res.status = HTTP_404
            result = {"message": f"product #{product_id!r} not found"}
        else:
            result = {"id": product_id, "product": product}

        res.text = json.dumps(result)

    def on_delete(self, req: Request, res: Response, product_id: str):
        try:
            product_id = int(product_id)
            product = PRODUCTS.pop(product_id)
        except ValueError:
            res.status = HTTP_400
            result = {"message": f"not valid id {product_id!r}"}
        except KeyError:
            res.status = HTTP_404
            result = {"message": f"product #{product_id!r} not found"}
        else:
            result = {"message": f"deleted product #{product_id} with product {product!r}"}

        res.text = json.dumps(result)
