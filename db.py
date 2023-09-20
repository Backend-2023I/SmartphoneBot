from tinydb import TinyDB, Query
from telegram import update, InlineKeyboardButton, InlineKeyboardMarkup
class DB:

    def __init__(self,path):
        self.db = TinyDB(path)

    # def send_list(self,):
    #     for i in len(data):
    #         return 

    def get_tables(self):
        """
        To get the list of all the tables in the database
        """
        phone = ["Apple","Huawei","Nokia","Oppo","Redmi","Samsung","Vivo"]
        return phone
        
    def get_phone(self, brand, doc_id):
        """
        Return phone data by brand
        args:
            brand: str
        return:
            dict
        """
        phones = self.db.table(brand)
        phone = phones.get(doc_id=doc_id)
        return phone

    def get_phone_list(self,brand):
        """
        Return phone list
        """
        phone = self.db.table(brand)
        return phone.all()


    
if __name__ == "__main__":
    smartphone = DB("data.json")

    tables = smartphone.get_tables()
    brand = tables[0]
    phones = smartphone.get_phone_list(brand)

    phone = phones[4]
    doc_id = phone.doc_id
    print(smartphone.get_phone(brand, doc_id))