from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Plotter:
    def __init__(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

    def get_canvas(self):
        return self.canvas

    def plot_comparison(self, steel_costs, concrete_costs, labels):
        ax = self.figure.add_subplot(111)
        ax.clear()

        bar_width = 0.35
        x = range(len(labels))

        ax.bar(x, steel_costs, width=bar_width, label="Steel", color="blue")
        ax.bar([p + bar_width for p in x], concrete_costs, width=bar_width, label="Concrete", color="orange")

        ax.set_xticks([p + bar_width / 2 for p in x])
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_title("Cost Comparison: Steel vs. Concrete")
        ax.set_ylabel("Cost (₹)")
        ax.legend()
        self.canvas.draw()
