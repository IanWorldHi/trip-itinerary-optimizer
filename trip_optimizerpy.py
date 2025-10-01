import math
import random
import matplotlib.pyplot as plt
from typing import List, Tuple

class Location:
    def __init__(self, name: str, lat: float, lon: float):
        self.name = name
        self.lat = lat
        self.lon = lon
    def __repr__(self):
        return f"{self.name} ({self.lat}, {self.lon})"

def haversine_distance(loc1: Location, loc2: Location) -> float:
    """Calculates distance between two locations on the Earth using Haversine formula 
    (determins the distance between two points on a sphere in km)"""
    R = 6371  # Earth's radius/km
    lat1 = math.radians(loc1.lat)
    lon1 = math.radians(loc1.lon)
    lat2 = math.radians(loc2.lat) 
    lon2 = math.radians(loc2.lon)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.asin(math.sqrt(a))
    return R*c

def calculate_total_distance(route: List[Location]) -> float:
    """Calculate stotal distance for a travel route"""
    total = 0
    for i in range(len(route) - 1):
        total += haversine_distance(route[i], route[i + 1])
    total += haversine_distance(route[-1], route[0])
    return total

def nearest_neighbor(locations: List[Location], start_idx: int = 0) -> List[Location]:
    """Greedy algorithm"""
    unvisited = locations.copy()
    route = [unvisited.pop(start_idx)]
    while unvisited:
        current = route[-1]
        nearest = min(unvisited, key=lambda loc: haversine_distance(current, loc))
        route.append(nearest)
        unvisited.remove(nearest)
    return route

def two_opt_optimization(route: List[Location], max_iterations: int = 1000) -> List[Location]:
    """Using 2-opt optimization to optimize route"""
    best_route = route.copy()
    best_distance = calculate_total_distance(best_route)
    improved = True
    iterations = 0
    
    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                new_route = best_route.copy()
                new_route[i:j+1] = reversed(new_route[i:j+1])
                new_distance = calculate_total_distance(new_route)
                
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True
                    break
            if improved:
                break 
    return best_route

def visualize_route(route: List[Location], title: str = "Trip Itinerary"):
    """Visualize the route on a 2D plot"""
    lats = [loc.lat for loc in route] + [route[0].lat]
    lons = [loc.lon for loc in route] + [route[0].lon]
    
    plt.figure(figsize=(12, 8))
    plt.plot(lons, lats, 'b-', linewidth=2, alpha=0.6, label='Route')
    plt.plot(lons, lats, 'ro', markersize=10)
    
    for i, loc in enumerate(route):
        plt.annotate(f"{i+1}. {loc.name}", 
                    (loc.lon, loc.lat),
                    xytext=(5, 5), 
                    textcoords='offset points',
                    fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.title(f"{title}\nTotal Distance: {calculate_total_distance(route):.2f} km", 
             fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('trip_route.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    # Sample locations 
    locations = [
        Location("Paris", 48.8566, 2.3522),
        Location("London", 51.5074, -0.1278),
        Location("Berlin", 52.5200, 13.4050),
        Location("Amsterdam", 52.3676, 4.9041),
        Location("Brussels", 50.8503, 4.3517),
        Location("Munich", 48.1351, 11.5820),
        Location("Prague", 50.0755, 14.4378),
        Location("Vienna", 48.2082, 16.3738),
        Location("Zurich", 47.3769, 8.5417),
        Location("Milan", 45.4642, 9.1900)
    ]
    
    print("=" * 60)
    print("TRIP ITINERARY OPTIMIZER")
    print("=" * 60)
    print(f"\nPlanning route for {len(locations)} locations:\n")
    for i, loc in enumerate(locations, 1):
        print(f"{i}. {loc.name}")
    
    print("\n" + "-" * 60)
    print("Calculating optimal route...")
    print("-" * 60)
    
    # Greedy solution to begin
    initial_route = nearest_neighbor(locations)
    initial_distance = calculate_total_distance(initial_route)
    print(f"\nInitial route (Nearest Neighbor): {initial_distance:.2f} km")
    
    # Optimized with 2-opt
    optimized_route = two_opt_optimization(initial_route)
    optimized_distance = calculate_total_distance(optimized_route)
    print(f"Optimized route (2-opt): {optimized_distance:.2f} km")
    print(f"Improvement: {initial_distance - optimized_distance:.2f} km ({((initial_distance - optimized_distance) / initial_distance * 100):.1f}%)")
    
    print("\n" + "=" * 60)
    print("OPTIMAL ROUTE:")
    print("=" * 60)
    for i, loc in enumerate(optimized_route, 1):
        print(f"{i}. {loc.name}")
    print(f"{len(optimized_route) + 1}. {optimized_route[0].name} (return to start)")
    
    visualize_route(optimized_route, "Optimized Trip Itinerary")
    print("\nRoute visualization saved as 'trip_route.png'")

if __name__ == "__main__":
    main()





