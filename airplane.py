from vehicle import Vehicle

class Airplane(Vehicle):
    """Класс для представления самолета"""
    
    def __init__(self, capacity: float, max_altitude: float):
        super().__init__(capacity)
        self.max_altitude = max_altitude  # в метрах
    
    def get_type(self) -> str:
        return "Самолет"
    
    def can_reach_altitude(self, required_altitude: float) -> bool:
        """Проверяет, может ли самолет достичь заданной высоты"""
        return required_altitude <= self.max_altitude
    
    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str}, макс. высота: {self.max_altitude} м"