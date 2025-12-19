import matplotlib.pyplot as plt

categories = ["Men's Swimming", "Men's Volleyball", "Women's Swimming", "Women's Volleyball"]
avg_heights = [71.06, 70.95, 65.59, 68.44]  # inches (your results)

plt.figure(figsize=(8, 5))
plt.bar(categories, avg_heights)
plt.ylabel("Average Height (inches)")
plt.title("Average Height by Team Category")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()

plt.savefig("average_height_bar_graph.png", dpi=300)
plt.show()

print("Saved: average_height_bar_graph.png")