# KPP Programming
# UKM Robotika ITS 2025
#
# Hendra Manudinata / 5027251051
# Teknologi Informasi / FTEIC

# KPP ini menggunakan algoritma Dijkstra
# yang dimodifikasi untuk sekalian menghitung
# waktu (ganjil/genap) dan charging point

MAX_ENERGY = 1000
SPEED = 100
MIN_EDGE_TIME = 2

class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = {}
    def add_edge(self, u, v, w, o):
        self.adj.setdefault(u, []).append((v, w, o))
        self.adj.setdefault(v, []).append((u, w, o))

class KPPRobotik:
    def __init__(self, n):
        self.Graph = Graph(n)

    def get_best_routes(self, n, start, target, rest_points, charging_stations, start_hour):
        # states: list of (energy_used, time, node, energy_left, path, timeline)
        states = [(0, start_hour*60, start, MAX_ENERGY, [start], [0])]
        visited = {}

        while states:
            # pick the state with the smallest energy_used (linear search)
            idx = min(range(len(states)), key=lambda i: states[i][0])
            energy_used, time, node, energy_left, path, timeline = states.pop(idx)

            # reached target
            if node == target:
                print("Total energi minimum:", energy_used)
                print("Jalur:", " -> ".join(path))
                print("Waktu tiba:")
                for n, t in zip(path, timeline):
                    print(f"{n} (menit {t})")
                return

            # key: (node, time parity, energy_left bucketed)
            state_key = (node, time // 60 % 2, energy_left)
            if state_key in visited and visited[state_key] <= energy_used:
                continue
            visited[state_key] = energy_used

            # charging station
            if node in charging_stations and energy_left < MAX_ENERGY:
                states.append((energy_used, time, node, MAX_ENERGY, path, timeline))

            # rest point (wait until next even hour)
            if node in rest_points:
                hour = time // 60
                if hour % 2 == 1:
                    minutes_to_next_hour = 60 - (time % 60)
                    new_time = time + minutes_to_next_hour
                    states.append((energy_used, new_time, node, energy_left, path, timeline+[new_time]))

            # explore neighbors
            for v, w, o in self.Graph.adj.get(node, []):
                base_cost = w + o
                hour = time // 60
                if hour % 2 == 1:
                    cost = int(base_cost * 1.3)
                else:
                    cost = int(base_cost * 0.8)

                if cost <= energy_left:
                    travel_time = max(MIN_EDGE_TIME, round(w / SPEED))
                    new_time = time + travel_time
                    states.append((
                        energy_used + cost,
                        new_time,
                        v,
                        energy_left - cost,
                        path + [v],
                        timeline + [new_time]
                    ))

        print("Robot gagal dalam mencapai tujuan :(")

if __name__ == "__main__":
    # N, M (Jumlah node, jumlah edge)
    n, m = map(int, input().split())

    # Initialize program
    kppGwe = KPPRobotik(n)

    # Add edges to Graph
    for _ in range(m):
        u, v, w, o = input().split()
        w, o = int(w), int(o)
        kppGwe.Graph.add_edge(u, v, w, o)

    # Input: Start, Target
    S, T = input().split()

    # Rest points
    rest_points = set(input().split())
    if "-" in rest_points: rest_points = set()

    # Charging stations
    charging_stations = set(input().split())
    if "-" in charging_stations: charging_stations = set()

    # Mechanic & Electrial (UNUSED)
    input()
    input()

    # Start hour
    start_hour = int(input())

    # Execute dawg
    kppGwe.get_best_routes(n, S, T, rest_points, charging_stations, start_hour)
