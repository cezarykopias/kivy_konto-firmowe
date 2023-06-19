import kivy
from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from datetime import datetime as dt
from collections import defaultdict


class MainApp(App):
    store = JsonStore('data.json')
    try:
        money_amount = store.get('Kame7C0')['balance']
        # Simple Seller
    except KeyError:
        money_amount = store.put("Kame7C0", balance=0)
        # first record init to  {"Kame7C0": {"balance": 0}}
    hardware_store = defaultdict(lambda: 0)
    
    # for kv lang
    def sell(self, name, price, count):
        avalible = self.hardware_store[name]
        if avalible >= count:
            self.store.put(str(dt.now()), name=name, price=price, count=-count)
            self.money_amount += price * count
            self.hardware_store[name] -= count
            self.store.put('Kame7C0', balance=self.money_amount)
            return f"Pomyślnie sprzedano produkt. {count}\n\
                Pozostało {avalible - count}"
        else:
            return f"Nie ma wystarczająco produktu w magazynie.\n\
                Pozostało {avalible}"
 
    def buy(self, name, price, count):
        if not price or not count:
            return f"Co?."
        cost = price * count
        if self.money_amount >= cost:
            self.store.put(str(dt.now()), name=name, price=price, count=count)
            self.hardware_store[name] += count
            self.money_amount -= cost
            self.store.put('Kame7C0', balance=self.money_amount)
            return f"Pomyślnie kupiono produkt.\n\
                {cost} PLN = {count} * {price} PLN"
        else:
            return f"Masz za mało sirodków na kącie.\n\
                Dostępne fundusze: {self.money_amount} PLN"

    
    def balance(self, amount=None):
        if amount:
            self.money_amount += amount
            self.store.put('Kame7C0', balance=self.money_amount)
        return f"Dostępne fundusze:\n{self.money_amount} PLN"
    
    
    def history_data(self, date_from=None, date_to=None):
        return [{'text': str(self.store[item])} for item in self.store]


    def hardware_data(self, name=None):
        data = defaultdict(lambda: 0)
        self.hardware_store = data
        for item in self.store:
            if item == 'Kame7C0':
                continue
            name = self.store[item]['name']
            count = self.store[item]['count']
            data[name] += count 
        
        return [{'text': f"{name} = {count}"} for name, count in data.items()]




if __name__ == '__main__':
    MainApp().run()