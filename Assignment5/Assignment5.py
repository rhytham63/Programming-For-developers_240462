import tkinter as tk
from tkinter import ttk, messagebox
import itertools
import math

# -----------------------------
# Tourist Spot Dataset
# -----------------------------
SPOTS = [
    {
        "name": "Pashupatinath Temple",
        "lat": 27.7104,
        "lon": 85.3488,
        "fee": 100,
        "tags": ["culture", "religious"]
    },
    {
        "name": "Swayambhunath Stupa",
        "lat": 27.7149,
        "lon": 85.2906,
        "fee": 200,
        "tags": ["culture", "heritage"]
    },
    {
        "name": "Garden of Dreams",
        "lat": 27.7125,
        "lon": 85.3170,
        "fee": 150,
        "tags": ["nature", "relaxation"]
    },
    {
        "name": "Chandragiri Hills",
        "lat": 27.6616,
        "lon": 85.2458,
        "fee": 700,
        "tags": ["nature", "adventure"]
    },
    {
        "name": "Kathmandu Durbar Square",
        "lat": 27.7048,
        "lon": 85.3076,
        "fee": 100,
        "tags": ["culture", "heritage"]
    }
]

VISIT_TIME = 1.0  # hours per place
SPEED = 30.0      # km/h (simulated)


# -----------------------------
# Utility Functions
# -----------------------------
def distance(a, b):
    return math.sqrt((a["lat"] - b["lat"]) ** 2 + (a["lon"] - b["lon"]) ** 2) * 111


def travel_time(a, b):
    return distance(a, b) / SPEED


def interest_score(spot, interests):
    return len(set(spot["tags"]) & interests)


# -----------------------------
# Greedy Heuristic Algorithm
# -----------------------------
def greedy_itinerary(spots, time_limit, budget, interests):
    remaining = spots[:]
    route = []
    total_time = 0
    total_cost = 0
    current = None
    explanation = []

    while remaining:
        best = None
        best_score = -1

        for s in remaining:
            travel = travel_time(current, s) if current else 0
            score = interest_score(s, interests) / (s["fee"] + 1) / (travel + 0.1)

            if (
                total_time + travel + VISIT_TIME <= time_limit
                and total_cost + s["fee"] <= budget
                and score > best_score
            ):
                best = s
                best_score = score

        if not best:
            break

        travel = travel_time(current, best) if current else 0
        total_time += travel + VISIT_TIME
        total_cost += best["fee"]
        explanation.append(
            f"Selected {best['name']} (Interest match & low cost)"
        )

        route.append(best)
        remaining.remove(best)
        current = best

    return route, total_time, total_cost, explanation


# -----------------------------
# Brute Force Algorithm
# -----------------------------
def brute_force_itinerary(spots, time_limit, budget):
    best_route = []
    best_count = 0

    for r in range(1, len(spots) + 1):
        for perm in itertools.permutations(spots, r):
            time = 0
            cost = 0
            valid = True
            current = None

            for s in perm:
                travel = travel_time(current, s) if current else 0
                time += travel + VISIT_TIME
                cost += s["fee"]
                current = s

                if time > time_limit or cost > budget:
                    valid = False
                    break

            if valid and len(perm) > best_count:
                best_count = len(perm)
                best_route = perm

    return best_route


# -----------------------------
# GUI Application
# -----------------------------
class ItineraryApp:
    def __init__(self, root):
        root.title("Tourist Itinerary Planner")
        root.geometry("900x600")

        # Input Frame
        frame = ttk.LabelFrame(root, text="User Preferences")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Available Time (hours):").grid(row=0, column=0)
        self.time_entry = ttk.Entry(frame)
        self.time_entry.insert(0, "6")
        self.time_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Max Budget:").grid(row=1, column=0)
        self.budget_entry = ttk.Entry(frame)
        self.budget_entry.insert(0, "800")
        self.budget_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Interests:").grid(row=2, column=0)
        self.interests = {
            "culture": tk.BooleanVar(),
            "nature": tk.BooleanVar(),
            "adventure": tk.BooleanVar(),
            "heritage": tk.BooleanVar(),
            "religious": tk.BooleanVar(),
            "relaxation": tk.BooleanVar(),
        }

        col = 1
        for tag in self.interests:
            ttk.Checkbutton(frame, text=tag, variable=self.interests[tag]).grid(
                row=2, column=col
            )
            col += 1

        ttk.Button(frame, text="Generate Itinerary", command=self.run).grid(
            row=3, column=1, pady=5
        )

        # Output Text
        self.output = tk.Text(root, height=18)
        self.output.pack(fill="both", padx=10, pady=5)

        # Canvas Map
        self.canvas = tk.Canvas(root, height=200, bg="white")
        self.canvas.pack(fill="x", padx=10)

    def run(self):
        try:
            time_limit = float(self.time_entry.get())
            budget = float(self.budget_entry.get())
        except:
            messagebox.showerror("Error", "Invalid input")
            return

        interests = {k for k, v in self.interests.items() if v.get()}

        route, t, c, explanation = greedy_itinerary(
            SPOTS, time_limit, budget, interests
        )

        brute = brute_force_itinerary(SPOTS[:5], time_limit, budget)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "GREEDY ITINERARY:\n")
        for i, s in enumerate(route, 1):
            self.output.insert(tk.END, f"{i}. {s['name']}\n")

        self.output.insert(
            tk.END,
            f"\nTotal Time: {t:.2f} hrs\nTotal Cost: Rs {c}\n\n"
        )

        self.output.insert(tk.END, "Decision Explanation:\n")
        for e in explanation:
            self.output.insert(tk.END, f"- {e}\n")

        self.output.insert(tk.END, "\nBRUTE FORCE RESULT (Small Set):\n")
        for s in brute:
            self.output.insert(tk.END, f"- {s['name']}\n")

        self.output.insert(
            tk.END,
            f"\nComparison:\nGreedy spots: {len(route)} | Optimal spots: {len(brute)}\n"
            "Greedy is faster but may miss the absolute best path.\n"
        )

        self.draw_map(route)

    def draw_map(self, route):
        self.canvas.delete("all")
        if not route:
            return

        lats = [s["lat"] for s in route]
        lons = [s["lon"] for s in route]

        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        def scale(x, minv, maxv, size):
            return 20 + (x - minv) / (maxv - minv + 0.0001) * (size - 40)

        points = []
        for s in route:
            x = scale(s["lon"], min_lon, max_lon, 900)
            y = scale(s["lat"], min_lat, max_lat, 200)
            points.append((x, y))

        for i in range(len(points)):
            x, y = points[i]
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
            self.canvas.create_text(x+10, y, text=str(i+1), anchor="w")

            if i > 0:
                self.canvas.create_line(
                    points[i-1][0], points[i-1][1], x, y, arrow=tk.LAST
                )


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ItineraryApp(root)
    root.mainloop()