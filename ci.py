import numpy as np
import matplotlib.pyplot as plt


def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a) if b != a else 1.0
    elif b < x < c:
        return (c - x) / (c - b) if c != b else 1.0


def fuzzify_temperature(temp):
    cold = triangular(temp, 0, 0, 25)
    warm = triangular(temp, 20, 30, 40)
    hot  = triangular(temp, 35, 50, 50)
    return cold, warm, hot


def apply_rules(cold, warm, hot):
    return {
        "low": cold,
        "medium": warm,
        "high": hot
    }


def defuzzify(output, plot=False):
    speed_range = np.linspace(0, 100, 1000)

    low = np.array([min(output["low"], triangular(x, 0, 0, 50)) for x in speed_range])
    medium = np.array([min(output["medium"], triangular(x, 25, 50, 75)) for x in speed_range])
    high = np.array([min(output["high"], triangular(x, 50, 100, 100)) for x in speed_range])

    aggregated = np.maximum(low, np.maximum(medium, high))

    if np.sum(aggregated) == 0:
        return 0

    centroid = np.sum(speed_range * aggregated) / np.sum(aggregated)

    if plot:
        plt.figure()
        plt.plot(speed_range, low, label="Low Speed")
        plt.plot(speed_range, medium, label="Medium Speed")
        plt.plot(speed_range, high, label="High Speed")
        plt.plot(speed_range, aggregated, label="Aggregated", linewidth=2)
        plt.axvline(centroid, linestyle="--", label=f"Centroid = {centroid:.2f}")
        plt.xlabel("Fan Speed (%)")
        plt.ylabel("Membership Degree")
        plt.title("Fan Speed Output (Defuzzification)")
        plt.legend()
        plt.grid(True)
        plt.show()

    return centroid


def plot_temperature_memberships(temp):
    temp_range = np.linspace(0, 60, 1000)

    cold = [triangular(x, 0, 0, 25) for x in temp_range]
    warm = [triangular(x, 20, 30, 40) for x in temp_range]
    hot  = [triangular(x, 35, 50, 50) for x in temp_range]

    plt.figure()
    plt.plot(temp_range, cold, label="Cold")
    plt.plot(temp_range, warm, label="Warm")
    plt.plot(temp_range, hot, label="Hot")
    plt.axvline(temp, linestyle="--", label=f"Input Temp = {temp}°C")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Membership Degree")
    plt.title("Temperature Membership Functions")
    plt.legend()
    plt.grid(True)
    plt.show()


def fuzzy_logic_system(temperature):
    plot_temperature_memberships(temperature)

    cold, warm, hot = fuzzify_temperature(temperature)
    rule_output = apply_rules(cold, warm, hot)

    fan_speed = defuzzify(rule_output, plot=True)
    return fan_speed


# ---- Test ----
temp_input = 30
result = fuzzy_logic_system(temp_input)

print(f"Input Temperature: {temp_input}°C")
print(f"Output Fan Speed: {result:.2f}%")
