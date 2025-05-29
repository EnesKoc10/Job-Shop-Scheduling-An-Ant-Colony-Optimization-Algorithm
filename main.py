from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from mainwindow import Ui_MainWindow
from aco_optimizer import ACOOptimizer
from ant import Ant, ProblemInstance
import pyqtgraph as pg
import random as rnd


def setup_jobs_table(table_widget, num_jobs, num_operations, num_machines):
    table_widget.clear()

    # Toplam sütun: her job için num_machines adet alt sütun
    total_columns = num_jobs * num_machines
    table_widget.setColumnCount(total_columns)

    # Toplam satır = operasyon sayısı
    table_widget.setRowCount(num_operations)

    # Yatay başlıklar (machines) ve üst başlıklar (job)
    horizontal_headers = []
    for job_id in range(num_jobs):
        for machine_id in range(num_machines):
            horizontal_headers.append(f"Job {job_id}\nM{machine_id}")

    table_widget.setHorizontalHeaderLabels(horizontal_headers)

    # Dikey başlıklar: Op 0, Op 1, ...
    for op_id in range(num_operations):
        item = QTableWidgetItem(f"Op {op_id}")
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        table_widget.setVerticalHeaderItem(op_id, item)

    # Hücreleri düzenlenebilir yap
    for row in range(num_operations):
        for col in range(total_columns):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemFlag.ItemIsSelectable |
                          Qt.ItemFlag.ItemIsEditable |
                          Qt.ItemFlag.ItemIsEnabled)
            table_widget.setItem(row, col, item)

    table_widget.resizeColumnsToContents()
    table_widget.resizeRowsToContents()


def create_problem_from_table(table_widget: QTableWidget) -> ProblemInstance:
    """
    QTableWidget'ten job tabanlı problem örneği oluşturur
    Tablo formatı:
    - Sütunlar: Job 0\nM1, Job 0\nM2, Job 1\nM1, ...
    - Satırlar: Operasyonlar
    - Hücreler: İşlem süreleri
    """
    from collections import defaultdict

    jobs_dict = defaultdict(lambda: defaultdict(list))

    for col in range(table_widget.columnCount()):
        header = table_widget.horizontalHeaderItem(col).text()
        try:
            job_line, machine_line = header.split('\n')
            job_id = int(job_line.split()[1])
            machine_id = int(machine_line[1:])  # "M1" → 1
        except (ValueError, AttributeError, IndexError):
            continue

        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, col)
            if item is None or item.text().strip() == "":
                continue

            try:
                proc_time = int(item.text())
                jobs_dict[job_id][row].append((machine_id, proc_time))
            except ValueError:
                continue

    data = []

    for job_id in sorted(jobs_dict.keys()):
        job_data = []
        for proc_id in sorted(jobs_dict[job_id].keys()):
            machine_options = jobs_dict[job_id][proc_id]
            job_data.append(machine_options)
        data.append(job_data)

    print(data)
    return ProblemInstance(data)


class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui._createProblemBtn.clicked.connect(self.create_table)
        self.ui.startScheduler.clicked.connect(self.optimize_aco)
        self.ui._randomFill.clicked.connect(self.random_fill_table)

    def optimize_aco(self):
        params = {
            'num_ants': self.ui._ants.value(),
            'num_iterations': self.ui._iterations.value(),
            'evaporation_rate': self.ui._evaporation.value(),
            'alpha': self.ui._alpha.value(),
            'beta': self.ui._beta.value()
        }

        problem = create_problem_from_table(table_widget=self.ui._jobsTable)
        optimizer = ACOOptimizer(problem, **params)
        best_schedule = optimizer.run()
        self.plot_schedule_with_pyqtgraph(best_schedule, problem, self.ui._viewSchedule)

    def plot_schedule_with_pyqtgraph(self, schedule, problem, view_widget):
        layout = view_widget.layout()
        if layout is None:
            layout = QVBoxLayout(view_widget)
            view_widget.setLayout(layout)

        for i in reversed(range(layout.count())):
            widgetToRemove = layout.itemAt(i).widget()
            if widgetToRemove is not None:
                layout.removeWidget(widgetToRemove)
                widgetToRemove.deleteLater()

        plot_widget = pg.PlotWidget()
        layout.addWidget(plot_widget)

        machine_times = {}
        y_ticks = []
        y_value_map = {}
        y_counter = 1

        for op in schedule:

            machine_id = op.machine_id
            job_id = op.job_id
            duration = op.processing_time
            start_time = op.start_time

            if machine_id not in y_value_map:
                y_value_map[machine_id] = y_counter
                y_ticks.append((y_counter, f"M{machine_id}"))
                y_counter += 1

            y_val = y_value_map[machine_id]
            color = self.get_color_for_job(job_id)

            # Çubuğu çiz
            bar = pg.BarGraphItem(
                x=[start_time + duration / 2],
                height=0.8,
                width=duration,
                y=[y_val],
                brushes=[color]
            )
            plot_widget.addItem(bar)

            # Job ID metnini ekle
            text = pg.TextItem(text=f"Job {job_id} \nOp {op.order}", color=(255, 255, 255))
            text.setPos(start_time + duration / 2, y_val + 0.3)
            plot_widget.addItem(text)

        plot_widget.getPlotItem().getAxis('left').setTicks([y_ticks])
        plot_widget.setLabel('bottom', 'Time')
        plot_widget.setLabel('left', 'Machines')
        plot_widget.setTitle('Job Shop Schedule')

    def create_table(self):
        setup_jobs_table(
            self.ui._jobsTable,
            self.ui._jobs.value(),
            self.ui._operations.value(),
            self.ui._machines.value()
        )

    def random_fill_table(self):
        # Get current values from spinboxes
        num_jobs = min(self.ui._jobs.value(), 10)
        num_operations = min(self.ui._operations.value(), 10)
        num_machines = min(self.ui._machines.value(), 10)
        
        # Set the values back to spinboxes if they were over 10
        self.ui._jobs.setValue(num_jobs)
        self.ui._operations.setValue(num_operations)
        self.ui._machines.setValue(num_machines)
        
        # Create the table with the specified dimensions
        self.ui._jobsTable.clear()
        total_columns = num_jobs * num_machines
        self.ui._jobsTable.setColumnCount(total_columns)
        self.ui._jobsTable.setRowCount(num_operations)
        
        # Set horizontal headers
        horizontal_headers = []
        for job_id in range(num_jobs):
            for machine_id in range(num_machines):
                horizontal_headers.append(f"Job {job_id}\nM{machine_id}")
        self.ui._jobsTable.setHorizontalHeaderLabels(horizontal_headers)
        
        # Set vertical headers
        for op_id in range(num_operations):
            item = QTableWidgetItem(f"Op {op_id}")
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.ui._jobsTable.setVerticalHeaderItem(op_id, item)
        
        # Fill cells with random processing times
        for row in range(num_operations):
            for col in range(total_columns):
                item = QTableWidgetItem(str(rnd.randint(1, 70)))
                item.setFlags(Qt.ItemFlag.ItemIsSelectable |
                             Qt.ItemFlag.ItemIsEditable |
                             Qt.ItemFlag.ItemIsEnabled)
                self.ui._jobsTable.setItem(row, col, item)
        
        self.ui._jobsTable.resizeColumnsToContents()
        self.ui._jobsTable.resizeRowsToContents()

    def get_color_for_job(self, job_id):
        rnd.seed(job_id)
        r = rnd.randint(50, 255)
        g = rnd.randint(50, 255)
        b = rnd.randint(50, 255)
        return (r, g, b)

if __name__ == "__main__":
    app = QApplication([])
    window = main()
    window.show()
    app.exec()
