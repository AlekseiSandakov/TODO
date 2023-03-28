from falcon import App, CORSMiddleware
from waitress import serve

from products_views import ProductsListResource, ProductDetailsResource

ALLOW_ORIGINS = [
    "abc.com",
    "www.google.com",
    "http://httpbin.org",
]

cors = CORSMiddleware(allow_origins=ALLOW_ORIGINS)

products_list = ProductsListResource()
product_details = ProductDetailsResource()

app = App(middleware=cors)

app.add_route("/products", products_list)
app.add_route("/products/{product_id}", product_details)

serve(app, host="127.0.0.1", port=8000)
