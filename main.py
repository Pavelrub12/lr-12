from transport_company import TransportCompany
from airplane import Airplane
from van import Van
from client import Client

def print_menu():
    """Выводит меню программы"""
    print("\n" + "=" * 30)
    print("ТРАНСПОРТНАЯ КОМПАНИЯ")
    print("=" * 30)
    print("1. Добавить клиента")
    print("2. Добавить транспорт")
    print("3. Показать клиентов")
    print("4. Показать транспорт")
    print("5. Распределить грузы")
    print("6. Выход")
    print("=" * 30)

def add_client(company):
    """Добавляет нового клиента"""
    name = input("Имя клиента: ")
    weight = float(input("Вес груза (тонны): "))
    is_vip = input("VIP? (да/нет): ").lower() == 'да'
    
    client = Client(name, weight, is_vip)
    company.add_client(client)
    print(f"Клиент {name} добавлен")

def add_vehicle(company):
    """Добавляет новое транспортное средство"""
    print("1. Самолет")
    print("2. Фургон")
    choice = input("Выберите тип: ")
    
    capacity = float(input("Грузоподъемность (тонны): "))
    
    if choice == "1":
        altitude = float(input("максимальная высота полета (метры): "))
        vehicle = Airplane(capacity, altitude)
    else:
        is_ref = input("Холодильник? (да/нет): ").lower() == 'да'
        vehicle = Van(capacity, is_ref)
    
    company.add_vehicle(vehicle)
    print(f"Транспорт {vehicle.vehicle_id} добавлен")

def show_clients(company):
    """Показывает список клиентов"""
    print("\n--- Клиенты ---")
    for client in company.list_clients():
        print(f"  {client}")

def show_vehicles(company):
    """Показывает список транспорта"""
    print("\n--- Транспорт ---")
    for vehicle in company.list_vehicles():
        print(f"  {vehicle}")

def distribute_cargo(company):
    """Распределяет грузы"""
    results = company.optimize_cargo_distribution()
    
    if results:
        print("\n--- Результаты ---")
        for item in results["distributed"]:
            print(f"  ✓ {item}")
        
        if results["not_distributed"]:
            print("\n--- Не распределено ---")
            for item in results["not_distributed"]:
                print(f"  ✗ {item}")

def main():
    """Основная функция программы"""
    company = TransportCompany("Аэро-Транс")
    
    # Создаем тестовые данные для демонстрации
    test_vehicles = [
        Airplane(20, 12000),
        Airplane(15, 10000),
        Van(5, True),
    ]
    
    test_clients = [
        Client("Иванов Иван", 8.5, True),
        Client("Петров Петр", 12.0, False),
        Client("Сидорова Анна", 3.5, True),
    ]
    
    for v in test_vehicles:
        company.add_vehicle(v)
    for c in test_clients:
        company.add_client(c)
    
    while True:
        print_menu()
        choice = input("Выберите действие: ")
        
        if choice == "1":
            add_client(company)
        elif choice == "2":
            add_vehicle(company)
        elif choice == "3":
            show_clients(company)
        elif choice == "4":
            show_vehicles(company)
        elif choice == "5":
            distribute_cargo(company)
        elif choice == "6":
            print("Выход из программы")
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()