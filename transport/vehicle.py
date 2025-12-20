import uuid

class Vehicle:
    def __init__(self, capacity):
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть > 0")
        
        self.vehicle_id = str(uuid.uuid4())[:8]
        self.capacity = float(capacity)
        self.current_load = 0.0
        self.clients_list = []
    
    def load_cargo(self, client):
        from transport.client import Client
        if not isinstance(client, Client):
            raise TypeError("Нужен объект Client")
        
        if self.current_load + client.cargo_weight > self.capacity:
            return False
        
        self.current_load += client.cargo_weight
        self.clients_list.append(client)
        return True
    
    def get_free_space(self):
        return self.capacity - self.current_load
    
    def __str__(self):
        return f"ID: {self.vehicle_id}, вместимость: {self.capacity}т, загружено: {self.current_load}т"