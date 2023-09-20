from tinydb import TinyDB, Query

class Cart:
    def __init__(self,cart_path:str):
        self.db = TinyDB(cart_path, indent=4)
        self.table = self.db.table('cart')

    def add(self, brand, doc_id, chat_id):
        """
        add card

        data = {
            'brand':brand,
            'doc_id': doc_id,
            chat_id: chat_id
            }
        """
        data=self.db.table('cart')
        document={
            'brand':brand,
            'doc_id':doc_id,
            'chat_id':chat_id
        }
        self.table.insert(document)
        return data

    def get_cart(self,chat_id):
        cart=self.db.table("cart")
        User = Query()
        return cart.search(User.chat_id == int(chat_id))
    
    def remove(self, chat_id):
        User=Query()
        cart=self.db.table("cart")
        data=cart.remove(User.chat_id == int(chat_id))
        
        return data
if __name__ == "__main__":
    cart = Cart("cart.json")

    print(cart.remove(5826220976))