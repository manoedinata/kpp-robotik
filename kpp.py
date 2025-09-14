import heapq

MAX_ENERGY = 1000

class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = { }  # adjacency list: node -> [(neighbor, w, o)]
    
    def add_edge(self, u, v, w, o):
        if u not in self.adj: self.adj[u] = []
        if v not in self.adj: self.adj[v] = []
        self.adj[u].append((v, w, o))
        self.adj[v].append((u, w, o))

def solve(graph, start, target, rest_points, charging_stations, start_hour):
    # Priority queue: (total_energy_used, time, node, energy_left, path)
    pq = []
    heapq.heappush(pq, (0, 0, start, MAX_ENERGY, [start]))
    
    visited = dict()  # (node, energy_left, time_parity) -> best_energy
    
    while pq:
        energy_used, time, node, energy_left, path = heapq.heappop(pq)
        
        # Sudah sampai tujuan
        if node == target:
            print(f"Total energi minimum: {energy_used}")
            print("Jalur: " + " -> ".join(path))
            print("Waktu tiba:")
            for i, n in enumerate(path):
                print(f"{n} (menit {i*2})")  # asumsi tiap edge waktu = 2 menit di contoh
            return
        
        state = (node, energy_left, time % 2)
        if state in visited and visited[state] <= energy_used:
            continue
        visited[state] = energy_used
        
        # Charging
        if node in charging_stations and energy_left < MAX_ENERGY:
            heapq.heappush(pq, (energy_used, time, node, MAX_ENERGY, path))
        
        # Rest point → bisa tunggu 1 menit
        if node in rest_points:
            heapq.heappush(pq, (energy_used, time + 1, node, energy_left, path))
        
        # Explore neighbors
        for v, w, o in graph.adj.get(node, []):
            base_cost = w + o
            # Efek waktu
            hour = (start_hour*60 + time) // 60
            if hour % 2 == 1:  # ganjil
                cost = int(base_cost * 1.3)
            else:  # genap
                cost = int(base_cost * 0.8)
            
            if cost <= energy_left:
                heapq.heappush(pq, (energy_used + cost, time + 2, v, energy_left - cost, path + [v]))
    
    print("Robot gagal dalam mencapai tujuan :(")

def main():
    # Contoh input sesuai sample
    n, m = map(int, input().split())
    graph = Graph(n)
    for _ in range(m):
        u, v, w, o = input().split()
        w, o = int(w), int(o)
        graph.add_edge(u, v, w, o)
    
    S, T = input().split()
    rest_points = set(input().split())
    if "-" in rest_points: rest_points = set()
    charging_stations = set(input().split())
    if "-" in charging_stations: charging_stations = set()
    input()  # mechanic (unused)
    input()  # electrical (unused)
    start_hour = int(input())
    
    solve(graph, S, T, rest_points, charging_stations, start_hour)

if __name__ == "__main__":
    main()
