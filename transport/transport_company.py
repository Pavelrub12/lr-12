from typing import List, Dict, Tuple
from transport.vehicle import Vehicle
from transport.client import Client
from transport.airplane import Airplane
from transport.van import Van

class TransportCompany:
    """Класс для управления транспортной компанией"""
    
    def __init__(self, name: str):
        self.name = name
        self.vehicles: List[Vehicle] = []
        self.clients: List[Client] = []
    
    def add_vehicle(self, vehicle: Vehicle) -> bool:
        """
        Добавляет транспортное средство в компанию
        
        Args:
            vehicle: объект транспортного средства
            
        Returns:
            bool: True если успешно добавлено, False в противном случае
        """
        # Валидация типа
        if not isinstance(vehicle, Vehicle):
            print(f"Ошибка: {vehicle} не является транспортным средством")
            return False
        
        # Проверка уникальности ID
        for v in self.vehicles:
            if v.vehicle_id == vehicle.vehicle_id:
                print(f"Ошибка: транспорт с ID {vehicle.vehicle_id} уже существует")
                return False
        
        self.vehicles.append(vehicle)
        return True
    
    def list_vehicles(self) -> List[str]:
        """Возвращает список всех транспортных средств в виде строк"""
        return [str(vehicle) for vehicle in self.vehicles]
    
    def list_available_vehicles(self) -> List[Vehicle]:
        """Возвращает список транспортных средств с доступной емкостью"""
        return [v for v in self.vehicles if v.get_remaining_capacity() > 0]
    
    def add_client(self, client: Client) -> bool:
        """
        Добавляет клиента в компанию
        
        Args:
            client: объект клиента
            
        Returns:
            bool: True если успешно добавлено, False в противном случае
        """
        # Валидация типа
        if not isinstance(client, Client):
            print(f"Ошибка: {client} не является клиентом")
            return False
        
        # Проверка уникальности ID
        for c in self.clients:
            if c.client_id == client.client_id:
                print(f"Ошибка: клиент с ID {client.client_id} уже существует")
                return False
        
        self.clients.append(client)
        return True
    
    def list_clients(self) -> List[str]:
        """Возвращает список всех клиентов в виде строк"""
        return [str(client) for client in self.clients]
    
    def sort_vehicles_by_efficiency(self) -> List[Vehicle]:
        """
        Сортирует транспортные средства по эффективности 
        (грузоподъемность / количество возможных загрузок)
        """
        return sorted(self.vehicles, 
                     key=lambda v: v.capacity, 
                     reverse=True)
    
    def optimize_cargo_distribution(self) -> Dict[str, List[str]]:
        """
        Оптимизирует распределение грузов по транспортным средствам
        
        Returns:
            Словарь с результатами распределения
        """
        if not self.clients:
            print("Нет клиентов для распределения грузов")
            return {}
        
        if not self.vehicles:
            print("Нет транспортных средств для распределения грузов")
            return {}
        
        # Сортируем клиентов: сначала VIP, затем по весу груза (по убыванию)
        sorted_clients = sorted(self.clients, 
                               key=lambda c: (not c.is_vip, -c.cargo_weight))
        
        # Сортируем транспорт по эффективности (грузоподъемность по убыванию)
        sorted_vehicles = self.sort_vehicles_by_efficiency()
        
        # Создаем копии для работы
        remaining_clients = sorted_clients.copy()
        vehicles_copy = sorted_vehicles.copy()
        
        results = {
            "distributed": [],
            "not_distributed": [],
            "vehicle_usage": {v.vehicle_id: [] for v in vehicles_copy}
        }
        
        # Распределяем грузы VIP клиентов в первую очередь
        vip_clients = [c for c in remaining_clients if c.is_vip]
        for vip_client in vip_clients:
            loaded = False
            for vehicle in vehicles_copy:
                if vehicle.load_cargo(vip_client):
                    results["vehicle_usage"][vehicle.vehicle_id].append(vip_client.name)
                    results["distributed"].append(f"VIP {vip_client.name}: {vip_client.cargo_weight} т -> {vehicle.vehicle_id}")
                    remaining_clients.remove(vip_client)
                    loaded = True
                    break
            
            if not loaded:
                results["not_distributed"].append(f"VIP {vip_client.name}: {vip_client.cargo_weight} т (нет подходящего транспорта)")
                remaining_clients.remove(vip_client)
        
        # Распределяем остальных клиентов
        for client in remaining_clients:
            loaded = False
            # Пытаемся загрузить в уже частично загруженные транспортные средства
            for vehicle in vehicles_copy:
                if vehicle.load_cargo(client):
                    results["vehicle_usage"][vehicle.vehicle_id].append(client.name)
                    results["distributed"].append(f"{client.name}: {client.cargo_weight} т -> {vehicle.vehicle_id}")
                    loaded = True
                    break
            
            if not loaded:
                results["not_distributed"].append(f"{client.name}: {client.cargo_weight} т (нет места)")
        
        # Добавляем статистику по использованию транспорта
        results["statistics"] = {
            "total_clients": len(self.clients),
            "distributed_count": len(results["distributed"]),
            "not_distributed_count": len(results["not_distributed"]),
            "vehicles_used": sum(1 for v in vehicles_copy if v.current_load > 0),
            "total_vehicles": len(vehicles_copy),
            "load_percentage": sum(v.current_load for v in vehicles_copy) / 
                              sum(v.capacity for v in vehicles_copy) * 100
        }
        
        return results
    
    def clear_all_loads(self):
        """Очищает все грузы со всех транспортных средств"""
        for vehicle in self.vehicles:
            vehicle.unload_cargo()
        print("Все транспортные средства разгружены")
    
    def get_statistics(self) -> Dict:
        """Возвращает статистику по компании"""
        total_capacity = sum(v.capacity for v in self.vehicles)
        used_capacity = sum(v.current_load for v in self.vehicles)
        vip_clients = sum(1 for c in self.clients if c.is_vip)
        
        return {
            "company_name": self.name,
            "total_vehicles": len(self.vehicles),
            "total_clients": len(self.clients),
            "vip_clients": vip_clients,
            "total_capacity": total_capacity,
            "used_capacity": used_capacity,
            "available_capacity": total_capacity - used_capacity,
            "utilization_percentage": (used_capacity / total_capacity * 100) if total_capacity > 0 else 0
        }