from transport.vehicle import Vehicle

class Van(Vehicle):
    """Класс для представления фургона"""
    
    def __init__(self, capacity: float, is_refrigerated: bool = False):
        super().__init__(capacity)
        self.is_refrigerated = is_refrigerated
    
    def get_type(self) -> str:
        return "Фургон"
    
    def can_transport_perishable(self) -> bool:
        """Проверяет, может ли перевозить скоропортящиеся грузы"""
        return self.is_refrigerated
    
    def __str__(self) -> str:
        base_str = super().__str__()
        ref_status = "с холодильником" if self.is_refrigerated else "без холодильника"
        return f"{base_str}, {ref_status}"