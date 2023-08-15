from decimal import Decimal
from django.conf import settings
from social.models import Product


class Cart:
    
    def __init__(self, request) -> None:
        """Initialize cart

        Args:
            request (request.request): _description_
        """
        self.session=request.session
        cart=self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart=self.session[settings.CART_SESSION_ID]={}
        
        self.cart=cart
    
    def __iter__(self):
        """Iterate over the product in the cart.
        """
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        cart=self.cart.copy()
        for product in products:
            cart[str(product.id)]['product']=product
        for item in cart.values():
               item['price'] = Decimal(item['price'])
               item['total_price'] = item['price'] * item['quantity']
               yield item
    
    def add(self, product, quantity, override_quantity=False):
        """Add product to the cart in user session

        Args:
            product (_type_): model.object
            quantity (_type_): Int
            override_quantity (bool, optional): override product quantity? Defaults to False.
        """
        product_id=str(product.id)
        if not self.cart.get(product_id):
            self.cart[product_id]={
                'quantity':0,
                'price':str(product.price) # check if it works without changing to str. debug
            }
        if override_quantity:
            self.cart[product_id]['quantity']=quantity
        else:
            self.cart[product_id]['quantity']+=quantity
        self.save()
    
    def save(self):
        """Mark session as modified to make sure it gets saved.
        """
        self.session.modified=True
    
    def remove(self, product):
        """Remove product from the cart
        """
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __len__(self):
        """Return total no.of products.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """Get total price of the cart
        """
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """Clear all the cart items.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
    