import json
from decimal import Decimal
from Shop.models import Product

def decimal_default(object):
    if isinstance(object, Decimal):
        return float(object)


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get("session_key2", {})

        if not isinstance(cart, dict):
            cart = {}

        self.cart = cart

    def add(self, products,state):
        Productss_id = str(products.id)
        Productss_state = state
        Productss_situation = str(products.is_sale )
        print(Productss_situation)

        if products in self.cart:
            pass
        else:
            if Productss_situation == "True" or Productss_situation == "true":
                self.cart[Productss_id] = {"price": float(products.sale_price),
                                                     "state": Productss_state,
                                                     }   
            else:
                self.cart[Productss_id] = {"price": float(products.price),
                                                     "state": Productss_state,
                                                     }

        self.session.modified = True
        self.session["session_key2"] = self.cart
    def update(self, Productss_id, Productss_state, Productss_price):
        Productss_id = str(Productss_id)

        copy_cart = self.cart
        copy_cart[Productss_id] = {
            "price": float(Productss_price),
            "state": Productss_state,
        }
        self.session.modified = True

        return self.cart


    def save(self):
        self.session["session_key2"] = json.dump(self.cart, default=decimal_default)
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        Productss1_id = self.cart.keys()
        Productss = Product.objects.filter(id__in=Productss1_id)
        return Productss
    def get_real_session(self):
        return self.cart


    def delete(self,products):
        Productss_id = str(products.id)
        if Productss_id in self.cart:
            del self.cart[Productss_id]

        self.session.modified = True