import random
class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        if not name or not isinstance(name, str):
            raise ValueError("Имя клиента должно быть строкой")
        if not isinstance(cargo_weight, (int, float)) or cargo_weight <= 0:
            raise ValueError("Вес груза должен быть числом > 0")
        
        self.name = name
        self.cargo_weight = float(cargo_weight)
        self.is_vip = bool(is_vip)
        self.client_id = f"C{random.randint(1000, 9999)}"
    
    def __str__(self):
        vip = "VIP" if self.is_vip else "обычный"
        return f"Клиент: {self.name}, груз: {self.cargo_weight}т, статус: {vip}"