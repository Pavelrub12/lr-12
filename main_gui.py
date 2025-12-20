import dearpygui.dearpygui as dpg
import json
from transport.client import Client
from transport.vehicle import Vehicle
from transport.airplane import Airplane
from transport.van import Van
from transport.transport_company import TransportCompany

company = TransportCompany("Transport Company")

def add_client():
    with dpg.window(label="Add Client", modal=True, tag="win1"):
        dpg.add_text("Name:")
        n = dpg.add_input_text()
        dpg.add_text("Weight (kg):")
        w = dpg.add_input_text()
        v = dpg.add_checkbox(label="VIP")
        
        def save():
            name = dpg.get_value(n)
            weight_str = dpg.get_value(w)
            vip = dpg.get_value(v)
            
            if not name or len(name.strip()) < 2:
                dpg.set_value(n, "")
                return
            
            try:
                weight = float(weight_str)
                if weight <= 0 or weight > 10000:
                    dpg.set_value(w, "")
                    return
            except ValueError:
                dpg.set_value(w, "")
                return
            
            try:
                client = Client(name, weight/1000, vip)
                company.add_client(client)
                dpg.delete_item("win1")
            except Exception as e:
                print(f"Client error: {e}")
        
        dpg.add_button(label="Save", callback=save)
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("win1"))

def add_vehicle():
    with dpg.window(label="Add Vehicle", modal=True, tag="win2"):
        t = dpg.add_combo(items=["Airplane", "Van"])
        dpg.add_text("Capacity (kg):")
        c = dpg.add_input_text()
        
        plane_group = dpg.add_group(show=False)
        with dpg.group(parent=plane_group):
            dpg.add_text("Max Altitude (m):")
            alt = dpg.add_input_text(default_value="10000")
        
        van_group = dpg.add_group(show=False)
        with dpg.group(parent=van_group):
            dpg.add_text("Refrigerated:")
            ref = dpg.add_checkbox(label="Has refrigerator")
        
        def type_changed():
            vehicle_type = dpg.get_value(t)
            dpg.configure_item(plane_group, show=(vehicle_type == "Airplane"))
            dpg.configure_item(van_group, show=(vehicle_type == "Van"))
        
        dpg.configure_item(t, callback=lambda s, a: type_changed())
        
        def save():
            typ = dpg.get_value(t)
            cap_str = dpg.get_value(c)
            
            try:
                capacity = float(cap_str)
                if capacity <= 0:
                    dpg.set_value(c, "")
                    return
            except ValueError:
                dpg.set_value(c, "")
                return
            
            try:
                if typ == "Airplane":
                    max_altitude = float(dpg.get_value(alt))
                    if max_altitude <= 0:
                        dpg.set_value(alt, "10000")
                        return
                    vehicle = Airplane(capacity/1000, max_altitude)
                elif typ == "Van":
                    is_refrigerated = dpg.get_value(ref)
                    vehicle = Van(capacity/1000, is_refrigerated)
                
                company.add_vehicle(vehicle)
                dpg.delete_item("win2")
            except Exception as e:
                print(f"Vehicle error: {e}")
        
        dpg.add_button(label="Save", callback=save)
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("win2"))

def show_clients():
    with dpg.window(label="All Clients", modal=True, tag="clients_win", width=400, height=300):
        if not company.clients:
            dpg.add_text("No clients")
        else:
            for i, client in enumerate(company.clients, 1):
                dpg.add_text(f"{i}. {client.name} - {client.cargo_weight*1000:.1f}kg ({'VIP' if client.is_vip else 'Regular'})")
        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("clients_win"))

def show_vehicles():
    with dpg.window(label="All Vehicles", modal=True, tag="vehicles_win", width=500, height=300):
        if not company.vehicles:
            dpg.add_text("No vehicles")
        else:
            for i, vehicle in enumerate(company.vehicles, 1):
                vehicle_type = vehicle.__class__.__name__
                info = f"{i}. {vehicle_type} (ID: {vehicle.vehicle_id}) - {vehicle.capacity*1000:.1f}kg"
                if isinstance(vehicle, Airplane):
                    info += f" ({vehicle.max_altitude}m)"
                elif isinstance(vehicle, Van):
                    info += f" (Refrigerated: {'Yes' if vehicle.is_refrigerated else 'No'})"
                dpg.add_text(info)
        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("vehicles_win"))

def optimize():
    try: 
        results = company.optimize_cargo_distribution()
        
        with dpg.window(label="Optimization Results", modal=True, tag="opt_win", width=500, height=300):
            if not results:
                dpg.add_text("No results")
            else:
                if results.get("distributed"):
                    dpg.add_text("Distributed:", color=(0, 255, 0))
                    for item in results["distributed"]:
                        dpg.add_text(f"  {item}")
                
                if results.get("not_distributed"):
                    dpg.add_text("Not Distributed:", color=(255, 0, 0))
                    for item in results["not_distributed"]:
                        dpg.add_text(f"  {item}")
                
                if results.get("statistics"):
                    stats = results["statistics"]
                    dpg.add_text("Statistics:", color=(255, 255, 0))
                    dpg.add_text(f"  Total: {stats['total_clients']}")
                    dpg.add_text(f"  Distributed: {stats['distributed_count']}")
                    dpg.add_text(f"  Not Distributed: {stats['not_distributed_count']}")
            
            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("opt_win"))
        
    except Exception as e:
        print(f"Optimize error: {e}")

def export():
    try:
        data = {"clients": [], "vehicles": []}
        for c in company.clients:
            data["clients"].append({"name": c.name, "weight": c.cargo_weight, "vip": c.is_vip})
        for v in company.vehicles:
            vdata = {"type": v.__class__.__name__, "id": v.vehicle_id, "capacity": v.capacity}
            if isinstance(v, Airplane):
                vdata["altitude"] = v.max_altitude
            elif isinstance(v, Van):
                vdata["refrigerated"] = v.is_refrigerated
            data["vehicles"].append(vdata)
        with open("results.json", "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Export error: {e}")

def about():
    with dpg.window(label="About", modal=True, tag="win3"):
        dpg.add_text("Lab 13")
        dpg.add_text("Variant: 4")
        dpg.add_text("Student: Pavel Rubtsov")
        dpg.add_text("Group: 89TP")
        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("win3"))

def main():
    dpg.create_context()
    dpg.create_viewport(title='Transport Company', width=500, height=350)
    
    with dpg.window(label="Main", width=500, height=350):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Add Client", callback=add_client, width=120)
            dpg.add_button(label="Add Vehicle", callback=add_vehicle, width=120)
            dpg.add_button(label="Show Clients", callback=show_clients, width=120)
        
        dpg.add_spacer(height=5)
        
        with dpg.group(horizontal=True):
            dpg.add_button(label="Show Vehicles", callback=show_vehicles, width=120)
            dpg.add_button(label="Optimize", callback=optimize, width=120)
            dpg.add_button(label="Export JSON", callback=export, width=120)
        
        dpg.add_spacer(height=10)
        
        with dpg.group(horizontal=True):
            dpg.add_button(label="About", callback=about, width=120)
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()