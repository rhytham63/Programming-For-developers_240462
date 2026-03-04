from matplotlib import pyplot as plt


def plot_path(spots):
    lats = [s["lat"] for s in spots]
    lons = [s["lon"] for s in spots]

    plt.figure()
    plt.plot(lons, lats, marker='o')
    for i, s in enumerate(spots):
        plt.text(s["lon"], s["lat"], str(i+1))
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Tourist Itinerary Path")
    plt.show()
