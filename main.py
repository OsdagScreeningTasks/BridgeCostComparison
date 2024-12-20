import sys
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QGridLayout
)
from PyQt5.QtCore import Qt

class BridgeCostApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steel vs. Concrete Bridge Cost Comparison")
        self.setGeometry(100, 100, 1200, 600)

        # Main Layout
        main_layout = QHBoxLayout()

        # Left Dock: Input Parameters
        self.input_widget = QWidget()
        self.input_layout = QVBoxLayout()
        self.input_widget.setLayout(self.input_layout)
        main_layout.addWidget(self.input_widget)

        self.create_input_fields()

        # Center: Bar Plot
        self.plot_widget = QWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_widget.setLayout(self.plot_layout)
        main_layout.addWidget(self.plot_widget)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.plot_layout.addWidget(self.canvas)

        # Right Dock: Output Table
        self.output_widget = QWidget()
        self.output_layout = QVBoxLayout()
        self.output_widget.setLayout(self.output_layout)
        main_layout.addWidget(self.output_widget)

        self.create_output_table()

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Initialize Database
        self.init_database()

    def create_input_fields(self):
        grid = QGridLayout()

        # Labels and Inputs
        grid.addWidget(QLabel('Span Length (m):'), 0, 0)
        self.span_length_input = QLineEdit()
        grid.addWidget(self.span_length_input, 0, 1)

        grid.addWidget(QLabel('Width (m):'), 0, 2)
        self.width_input = QLineEdit()
        grid.addWidget(self.width_input, 0, 3)

        grid.addWidget(QLabel('Traffic Volume (vehicles/day):'), 1, 0)
        self.traffic_volume = QLineEdit()
        grid.addWidget(self.traffic_volume, 1, 1)

        grid.addWidget(QLabel('Design Life (years):'), 1, 2)
        self.design_life = QLineEdit()
        grid.addWidget(self.design_life, 1, 3)

        # Perform Calculation Button
        self.calculate_button = QPushButton('Calculate Costs')
        self.calculate_button.clicked.connect(self.calculate_costs)
        grid.addWidget(self.calculate_button, 2, 0, 1, 4)

        self.input_layout.addLayout(grid)
        self.result_label = QLabel('')
        self.input_layout.addWidget(self.result_label)

    def create_output_table(self):
        self.output_layout.addWidget(QLabel("Cost Comparison Table", alignment=Qt.AlignCenter))

        self.output_table = QTableWidget()
        self.output_table.setColumnCount(3)
        self.output_table.setHorizontalHeaderLabels(["Cost Component", "Steel Bridge (₹)", "Concrete Bridge (₹)"])
        self.output_layout.addWidget(self.output_table)

        self.export_button = QPushButton("Export Plot as PNG")
        self.export_button.clicked.connect(self.export_plot)
        self.output_layout.addWidget(self.export_button)

    def init_database(self):
        self.conn = sqlite3.connect("bridge_costs.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cost_data (
                Material TEXT,
                BaseRate REAL,
                MaintenanceRate REAL,
                RepairRate REAL,
                DemolitionRate REAL,
                EnvironmentalFactor REAL,
                SocialFactor REAL,
                DelayFactor REAL
            )
        """)

        self.cursor.execute("SELECT COUNT(*) FROM cost_data")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.executemany("""
                INSERT INTO cost_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                ("Steel", 3000, 50, 200, 100, 10, 0.5, 0.3),
                ("Concrete", 2500, 75, 150, 80, 8, 0.6, 0.2)
            ])
            self.conn.commit()

    def calculate_costs(self):
        try:
            span_length = float(self.span_length_input.text())
            width = float(self.width_input.text())
            traffic_volume = float(self.traffic_volume.text())
            design_life = int(self.design_life.text())
        except ValueError:
            self.result_label.setText("Error: Please enter valid numerical inputs.")
            return

        self.cursor.execute("SELECT * FROM cost_data")
        cost_data = self.cursor.fetchall()

        results = []
        for material, base_rate, maintenance_rate, repair_rate, demolition_rate, env_factor, social_factor, delay_factor in cost_data:
            construction_cost = span_length * width * base_rate
            maintenance_cost = span_length * width * maintenance_rate * design_life
            repair_cost = span_length * width * repair_rate
            demolition_cost = span_length * width * demolition_rate
            environmental_cost = span_length * width * env_factor
            social_cost = traffic_volume * social_factor * design_life
            user_cost = traffic_volume * delay_factor * design_life
            total_cost = (construction_cost + maintenance_cost + repair_cost +
                          demolition_cost + environmental_cost + social_cost + user_cost)

            results.append([material, construction_cost, maintenance_cost, repair_cost, demolition_cost,
                            environmental_cost, social_cost, user_cost, total_cost])

        self.populate_output_table(results)
        self.plot_costs(results)

    def populate_output_table(self, results):
        cost_components = ["Construction Cost", "Maintenance Cost", "Repair Cost", "Demolition Cost",
                           "Environmental Cost", "Social Cost", "User Cost", "Total Cost"]

        self.output_table.setRowCount(len(cost_components))

        for i, component in enumerate(cost_components):
            self.output_table.setItem(i, 0, QTableWidgetItem(component))
            self.output_table.setItem(i, 1, QTableWidgetItem(f"{results[0][i + 1]:,.2f}"))
            self.output_table.setItem(i, 2, QTableWidgetItem(f"{results[1][i + 1]:,.2f}"))

    def plot_costs(self, results):
        cost_components = ["Construction Cost", "Maintenance Cost", "Repair Cost", "Demolition Cost",
                           "Environmental Cost", "Social Cost", "User Cost"]

        steel_costs = [results[0][i + 1] for i in range(len(cost_components))]
        concrete_costs = [results[1][i + 1] for i in range(len(cost_components))]

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        x = range(len(cost_components))
        bar_width = 0.35

        ax.bar(x, steel_costs, width=bar_width, label="Steel", color="blue")
        ax.bar([p + bar_width for p in x], concrete_costs, width=bar_width, label="Concrete", color="orange")

        ax.set_xticks([p + bar_width / 2 for p in x])
        ax.set_xticklabels(cost_components, rotation=45, ha="right")
        ax.set_ylabel("Cost (₹)")
        ax.set_title("Cost Comparison: Steel vs. Concrete")
        ax.legend()

        self.canvas.draw()

    def export_plot(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png)", options=options)
        if file_path:
            self.figure.savefig(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BridgeCostApp()
    window.show()
    sys.exit(app.exec_())
