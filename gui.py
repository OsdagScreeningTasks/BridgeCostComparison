from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from plot import Plotter
from database import DatabaseManager
from calculations import CostCalculator

class BridgeCostApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steel vs. Concrete Bridge Cost Comparison")
        self.setGeometry(100, 100, 1200, 600)

        # Components
        self.db_manager = DatabaseManager("bridge_costs.db")
        self.calculator = CostCalculator(self.db_manager)
        self.plotter = Plotter()

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Input
        self.input_widget = QWidget()
        self.input_layout = QVBoxLayout(self.input_widget)
        self.create_input_fields()
        main_layout.addWidget(self.input_widget)

        # Plot
        self.plot_canvas = self.plotter.get_canvas()
        main_layout.addWidget(self.plot_canvas)

        # Output
        self.output_widget = QWidget()
        self.output_layout = QVBoxLayout(self.output_widget)
        self.create_output_table()
        main_layout.addWidget(self.output_widget)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_input_fields(self):
        # Implement similar input layout as before
        pass

    def create_output_table(self):
        # Implement output table
        pass

    def calculate_costs(self):
        try:
            # Fetch data and perform calculations
            span_length = float(self.span_length_input.text())
            width = float(self.width_input.text())
            traffic_volume = float(self.traffic_volume.text())
            design_life = int(self.design_life.text())

            results = self.calculator.calculate_costs(span_length, width, traffic_volume, design_life)
            self.populate_output_table(results)
            self.update_plot(results)
        except ValueError:
            self.result_label.setText("Error: Invalid input values.")

    def populate_output_table(self, results):
        # Populate table
        pass

    def update_plot(self, results):
        labels = ["Construction", "Maintenance", "Repair", "Demolition", "Environmental", "Social", "User"]
        steel_costs = [results[0][i + 1] for i in range(len(labels))]
        concrete_costs = [results[1][i + 1] for i in range(len(labels))]

        self.plotter.plot_comparison(steel_costs, concrete_costs, labels)
