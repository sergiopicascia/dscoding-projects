class Hotel:
    def __init__(self, name, rooms, price):
        self.name = name
        self.rooms = rooms
        self.price = price
        self.customers = []

    def allocate_customer(self, guest):
        if self.rooms > 0:
            self.rooms -= 1
            self.customers.append(guest)
            return True
        return False

    def calculate_total_earnings(self):
        return self.price * len(self.customers)
