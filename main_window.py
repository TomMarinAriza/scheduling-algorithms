"""
Módulo que contiene la interfaz principal de usuario.
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QTableWidget, QTableWidgetItem, QPushButton, 
                           QSpinBox, QLabel, QTextEdit, QTabWidget, 
                           QMessageBox, QHeaderView, QSplitter, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import os

from process_structures import Process, SchedulingResults
from scheduler_algorithms import ProcessScheduler
from gantt_chart import GanttChartWidget


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        super().__init__()
        self.scheduler = ProcessScheduler()
        self.gantt_widgets = {}
        self.current_results = {}
        
        self.init_ui()
        self.connect_signals()
        self.setup_initial_data()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        # Intentar cargar el archivo .ui
        ui_file = "mainwindow.ui"
        if os.path.exists(ui_file):
            try:
                loadUi(ui_file, self)
                self.setup_gantt_widgets()
                return
            except Exception as e:
                print(f"Error cargando UI: {e}")
        
        # Si no se puede cargar el .ui, crear la interfaz manualmente
        self.create_manual_ui()
    
    def create_manual_ui(self):
        """Crea la interfaz manualmente si no se puede cargar el .ui."""
        self.setWindowTitle("Simulador de Algoritmos de Planificación")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Título
        title_label = QLabel("Simulador de Algoritmos de Planificación de Procesos")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Tab widget principal
        self.tabWidget = QTabWidget()
        main_layout.addWidget(self.tabWidget)
        
        self.create_input_tab()
        self.create_results_tab()
        
        self.setup_gantt_widgets()
    
    def create_input_tab(self):
        """Crea la pestaña de entrada de datos."""
        input_tab = QWidget()
        self.tabWidget.addTab(input_tab, "Entrada de Procesos")
        
        layout = QVBoxLayout(input_tab)
        
        # Controles superiores con marco
        controls_frame = QFrame()
        controls_frame.setFrameStyle(QFrame.StyledPanel)
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(20)
        controls_layout.setContentsMargins(15, 10, 15, 10)
        
        # Grupo de número de procesos
        proc_label = QLabel("📊 Número de Procesos:")
        proc_label.setStyleSheet("font-size: 13px; color: #2c3e50;")
        controls_layout.addWidget(proc_label)
        
        self.processCountSpinBox = QSpinBox()
        self.processCountSpinBox.setRange(1, 20)
        self.processCountSpinBox.setValue(3)
        controls_layout.addWidget(self.processCountSpinBox)
        
        controls_layout.addSpacing(30)
        
        # Grupo de quantum
        quantum_label = QLabel("⏱️ Quantum Global:")
        quantum_label.setStyleSheet("font-size: 13px; color: #2c3e50;")
        controls_layout.addWidget(quantum_label)
        
        self.quantumSpinBox = QSpinBox()
        self.quantumSpinBox.setRange(1, 20)
        self.quantumSpinBox.setValue(2)
        controls_layout.addWidget(self.quantumSpinBox)
        
        controls_layout.addStretch()
        layout.addWidget(controls_frame)
        
        # Marco para la tabla
        table_frame = QFrame()
        table_frame.setFrameStyle(QFrame.StyledPanel)
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        # Título de la tabla
        table_title = QLabel("📋 Configuración de Procesos")
        table_title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
            padding: 5px;
            margin-bottom: 5px;
        """)
        table_layout.addWidget(table_title)
        
        # Tabla de procesos
        self.processTable = QTableWidget()
        self.processTable.setColumnCount(5)
        headers = ["🔢 Proceso", "📅 Tiempo Llegada", "⚡ Ráfaga", "🎯 Prioridad", "⏱️ Quantum*"]
        self.processTable.setHorizontalHeaderLabels(headers)
        self.processTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.processTable.setAlternatingRowColors(True)
        
        # Tooltip explicativo para la columna quantum
        self.processTable.horizontalHeaderItem(4).setToolTip(
            "* La columna Quantum es informativa. El valor real se toma del control 'Quantum Global' superior."
        )
        
        table_layout.addWidget(self.processTable)
        layout.addWidget(table_frame)
        
        # Marco para botones
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.addStretch()
        
        self.calculateButton = QPushButton("🚀 Calcular Algoritmos")
        self.calculateButton.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #27ae60, stop: 1 #2ecc71);
                color: white;
                font-weight: bold;
                font-size: 13px;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                min-width: 160px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #229954, stop: 1 #27ae60);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #1e8449, stop: 1 #229954);
            }
        """)
        buttons_layout.addWidget(self.calculateButton)
        
        buttons_layout.addSpacing(10)
        
        self.clearButton = QPushButton("🗑️ Limpiar")
        self.clearButton.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #e74c3c, stop: 1 #c0392b);
                color: white;
                font-weight: bold;
                font-size: 13px;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #c0392b, stop: 1 #a93226);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #a93226, stop: 1 #922b21);
            }
        """)
        buttons_layout.addWidget(self.clearButton)
        
        buttons_layout.addStretch()
        layout.addWidget(buttons_frame)
    
    def create_results_tab(self):
        """Crea la pestaña de resultados."""
        results_tab = QWidget()
        self.tabWidget.addTab(results_tab, "Resultados")
        
        layout = QVBoxLayout(results_tab)
        
        # Tab widget para algoritmos
        self.algorithmsTabWidget = QTabWidget()
        layout.addWidget(self.algorithmsTabWidget)
        
        # Pestañas para cada algoritmo
        self.create_algorithm_tab("FIFO", "fifoResultsTable")
        self.create_algorithm_tab("SJF", "sjfResultsTable")
        self.create_algorithm_tab("Prioridad", "priorityResultsTable")
        self.create_round_robin_tab()
    
    def create_algorithm_tab(self, name, table_attr):
        """Crea una pestaña para un algoritmo específico."""
        tab = QWidget()
        self.algorithmsTabWidget.addTab(tab, name)
        
        layout = QVBoxLayout(tab)
        
        # Crear splitter para dividir tabla y gráfico
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Contenedor para la tabla y información adicional
        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        
        # Título del algoritmo
        title_label = QLabel(name)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; background-color: #34495e; color: white; border-radius: 5px;")
        title_label.setAlignment(Qt.AlignCenter)
        table_layout.addWidget(title_label)
        
        # Tabla de resultados
        table = QTableWidget()
        table.setColumnCount(7)
        headers = ["Proceso", "Llegada", "Rafaga", "Prioridad", "Finalizacion", "Espera", "Retorno"]
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setMaximumWidth(650)
        
        setattr(self, table_attr, table)
        table_layout.addWidget(table)
        
        # Labels para estadísticas
        stats_label = QLabel("")
        stats_label.setStyleSheet("font-size: 12px; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
        setattr(self, table_attr.replace('Table', 'Stats'), stats_label)
        table_layout.addWidget(stats_label)
        
        splitter.addWidget(table_container)
        
        # Widget para el diagrama de Gantt
        gantt_widget = GanttChartWidget()
        self.gantt_widgets[name.lower()] = gantt_widget
        splitter.addWidget(gantt_widget)
        
        # Configurar proporciones del splitter
        splitter.setSizes([500, 700])  # Más espacio para el texto con nuevo formato
    
    def create_round_robin_tab(self):
        """Crea la pestaña de Round Robin con sub-pestañas."""
        rr_tab = QWidget()
        self.algorithmsTabWidget.addTab(rr_tab, "Round Robin")
        
        layout = QVBoxLayout(rr_tab)
        
        # Sub-tab widget para RR
        self.rrSubTabWidget = QTabWidget()
        layout.addWidget(self.rrSubTabWidget)
        
        # Sub-pestañas para RR
        self.create_rr_subtab("RR + FIFO", "rrFifoResultsTable", "rr_fifo")
        self.create_rr_subtab("RR + SJF", "rrSjfResultsTable", "rr_sjf") 
        self.create_rr_subtab("RR + Prioridad", "rrPriorityResultsTable", "rr_priority")
    
    def create_rr_subtab(self, name, table_attr, gantt_key):
        """Crea una sub-pestaña para Round Robin."""
        tab = QWidget()
        self.rrSubTabWidget.addTab(tab, name)
        
        layout = QVBoxLayout(tab)
        
        # Crear splitter
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Contenedor para la tabla y información adicional
        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        
        # Título del algoritmo
        title_label = QLabel(name)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; background-color: #8e44ad; color: white; border-radius: 5px;")
        title_label.setAlignment(Qt.AlignCenter)
        table_layout.addWidget(title_label)
        
        # Tabla de resultados
        table = QTableWidget()
        table.setColumnCount(7)
        headers = ["Proceso", "Llegada", "Rafaga", "Prioridad", "Finalizacion", "Espera", "Retorno"]
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setMaximumWidth(650)
        
        setattr(self, table_attr, table)
        table_layout.addWidget(table)
        
        # Labels para estadísticas
        stats_label = QLabel("")
        stats_label.setStyleSheet("font-size: 12px; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
        setattr(self, table_attr.replace('Table', 'Stats'), stats_label)
        table_layout.addWidget(stats_label)
        
        splitter.addWidget(table_container)
        
        # Widget para Gantt
        gantt_widget = GanttChartWidget()
        self.gantt_widgets[gantt_key] = gantt_widget
        splitter.addWidget(gantt_widget)
        
        # Configurar proporciones
        splitter.setSizes([500, 700])  # Más espacio para el texto
    
    def populate_results_table(self, table, stats_label, results, algorithm_name):
        """Llena la tabla con los resultados del algoritmo."""
        table.setRowCount(len(results.processes))
        
        for i, process in enumerate(results.processes):
            # Proceso
            item = QTableWidgetItem(f"P{process.id}")
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 0, item)
            
            # Llegada
            item = QTableWidgetItem(str(process.arrival_time))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 1, item)
            
            # Rafaga
            item = QTableWidgetItem(str(process.burst_time))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 2, item)
            
            # Prioridad
            item = QTableWidgetItem(str(process.priority))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 3, item)
            
            # Finalizacion
            item = QTableWidgetItem(str(process.completion_time))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 4, item)
            
            # Espera
            item = QTableWidgetItem(str(process.waiting_time))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 5, item)
            
            # Retorno
            item = QTableWidgetItem(str(process.turnaround_time))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 6, item)
        
        # Actualizar estadísticas
        stats_text = f"<b>Orden de Ejecución:</b> {results.execution_order}<br><br>"
        stats_text += f"<b>Tiempo de Espera Promedio:</b> {results.avg_waiting_time:.2f}<br>"
        stats_text += f"<b>Tiempo de Retorno Promedio:</b> {results.avg_turnaround_time:.2f}"
        stats_label.setText(stats_text)
    
    def setup_gantt_widgets(self):
        """Configura los widgets de Gantt si no existen."""
        if not hasattr(self, 'gantt_widgets'):
            self.gantt_widgets = {}
        
        # Verificar si ya se crearon manualmente
        if self.gantt_widgets:
            return
        
        # Si se cargó desde .ui, necesitamos crear los widgets manualmente
        # y agregarlos a los layouts existentes
        try:
            # Obtener las pestañas existentes y agregar los widgets de Gantt
            algorithms = ['fifo', 'sjf', 'priority']
            
            for i, alg in enumerate(algorithms):
                if hasattr(self, 'algorithmsTabWidget'):
                    tab = self.algorithmsTabWidget.widget(i)
                    if tab:
                        layout = tab.layout()
                        if not layout:
                            layout = QVBoxLayout(tab)
                        
                        # Crear splitter si no existe
                        splitter = QSplitter(Qt.Horizontal)
                        layout.addWidget(splitter)
                        
                        # Encontrar el QTextEdit existente y moverlo al splitter
                        text_edit = getattr(self, f'{alg}ResultsTextEdit', None)
                        if text_edit:
                            text_edit.setMaximumWidth(500)
                            splitter.addWidget(text_edit)
                        
                        # Crear widget de Gantt
                        gantt_widget = GanttChartWidget()
                        self.gantt_widgets[alg] = gantt_widget
                        splitter.addWidget(gantt_widget)
                        
                        splitter.setSizes([400, 800])
            
            # Round Robin tabs
            rr_algorithms = ['rr_fifo', 'rr_sjf', 'rr_priority']
            rr_attrs = ['rrFifoResultsTextEdit', 'rrSjfResultsTextEdit', 'rrPriorityResultsTextEdit']
            
            if hasattr(self, 'rrSubTabWidget'):
                for i, (alg, attr) in enumerate(zip(rr_algorithms, rr_attrs)):
                    tab = self.rrSubTabWidget.widget(i)
                    if tab:
                        layout = tab.layout()
                        if not layout:
                            layout = QVBoxLayout(tab)
                        
                        splitter = QSplitter(Qt.Horizontal)
                        layout.addWidget(splitter)
                        
                        text_edit = getattr(self, attr, None)
                        if text_edit:
                            text_edit.setMaximumWidth(500)
                            splitter.addWidget(text_edit)
                        
                        gantt_widget = GanttChartWidget()
                        self.gantt_widgets[alg] = gantt_widget
                        splitter.addWidget(gantt_widget)
                        
                        splitter.setSizes([400, 800])
        
        except Exception as e:
            print(f"Error configurando widgets de Gantt: {e}")
    
    def connect_signals(self):
        """Conecta las señales de los widgets."""
        if hasattr(self, 'calculateButton'):
            self.calculateButton.clicked.connect(self.calculate_algorithms)
        if hasattr(self, 'clearButton'):
            self.clearButton.clicked.connect(self.clear_results)
        if hasattr(self, 'processCountSpinBox'):
            self.processCountSpinBox.valueChanged.connect(self.generate_table)
        if hasattr(self, 'quantumSpinBox'):
            self.quantumSpinBox.valueChanged.connect(self.update_quantum_column)
    
    def setup_initial_data(self):
        """Configura los datos iniciales."""
        self.generate_table()
    
    def generate_table(self):
        """Genera la tabla de procesos."""
        if not hasattr(self, 'processCountSpinBox') or not hasattr(self, 'processTable'):
            return
        
        process_count = self.processCountSpinBox.value()
        self.processTable.setRowCount(process_count)
        
        for i in range(process_count):
            # Proceso ID (no editable)
            item = QTableWidgetItem(f"P{i + 1}")
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.processTable.setItem(i, 0, item)
            
            # Tiempo de llegada
            self.processTable.setItem(i, 1, QTableWidgetItem("0"))
            
            # Ráfaga
            self.processTable.setItem(i, 2, QTableWidgetItem("1"))
            
            # Prioridad
            self.processTable.setItem(i, 3, QTableWidgetItem("1"))
            
            # Quantum (valor informativo basado en el control superior)
            quantum_value = str(self.quantumSpinBox.value()) if hasattr(self, 'quantumSpinBox') else "2"
            quantum_item = QTableWidgetItem(quantum_value)
            quantum_item.setFlags(quantum_item.flags() & ~Qt.ItemIsEditable)  # No editable
            self.processTable.setItem(i, 4, quantum_item)
    
    def update_quantum_column(self):
        """Actualiza la columna quantum cuando cambia el valor del spinbox."""
        if not hasattr(self, 'processTable') or not hasattr(self, 'quantumSpinBox'):
            return
            
        quantum_value = str(self.quantumSpinBox.value())
        
        for i in range(self.processTable.rowCount()):
            quantum_item = QTableWidgetItem(quantum_value)
            quantum_item.setFlags(quantum_item.flags() & ~Qt.ItemIsEditable)  # No editable
            self.processTable.setItem(i, 4, quantum_item)
    
    def get_processes_from_table(self):
        """Obtiene los procesos de la tabla."""
        processes = []
        
        if not hasattr(self, 'processTable'):
            return processes
        
        for i in range(self.processTable.rowCount()):
            try:
                pid = i + 1
                arrival_time = int(self.processTable.item(i, 1).text())
                burst_time = int(self.processTable.item(i, 2).text())
                priority = int(self.processTable.item(i, 3).text())
                # Ignoramos la columna quantum de la tabla, usamos el quantum global
                
                process = Process(pid, arrival_time, burst_time, priority)
                # El quantum se establece globalmente en el scheduler
                processes.append(process)
            except (ValueError, AttributeError) as e:
                QMessageBox.warning(self, "Error", f"Error en la fila {i+1}: {e}")
                return []
        
        return processes
    
    def calculate_algorithms(self):
        """Calcula todos los algoritmos de planificación."""
        try:
            processes = self.get_processes_from_table()
            
            if not processes:
                QMessageBox.warning(self, "Advertencia", "No hay procesos para calcular.")
                return
            
            # Validar que todos los procesos tengan ráfaga > 0
            for process in processes:
                if process.burst_time <= 0:
                    QMessageBox.warning(self, "Error", "Todos los procesos deben tener ráfaga mayor a 0.")
                    return
            
            # Configurar el planificador
            self.scheduler.set_processes(processes)
            
            if hasattr(self, 'quantumSpinBox'):
                self.scheduler.set_quantum(self.quantumSpinBox.value())
            
            # Ejecutar algoritmos y mostrar resultados
            self.execute_and_display_algorithms()
            
            # Cambiar a la pestaña de resultados
            if hasattr(self, 'tabWidget'):
                self.tabWidget.setCurrentIndex(1)
            
            QMessageBox.information(self, "Éxito", 
                                  "Algoritmos calculados correctamente. "
                                  "Revisa la pestaña de Resultados.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo: {str(e)}")
    
    def execute_and_display_algorithms(self):
        """Ejecuta y muestra los resultados de todos los algoritmos."""
        algorithms = [
            ("FIFO", self.scheduler.schedule_fifo, "fifoResultsTable", "fifoResultsStats", "fifo"),
            ("SJF", self.scheduler.schedule_sjf, "sjfResultsTable", "sjfResultsStats", "sjf"), 
            ("Prioridad", self.scheduler.schedule_priority, "priorityResultsTable", "priorityResultsStats", "priority"),
            ("Round Robin FIFO", self.scheduler.schedule_round_robin_fifo, "rrFifoResultsTable", "rrFifoResultsStats", "rr_fifo"),
            ("Round Robin SJF", self.scheduler.schedule_round_robin_sjf, "rrSjfResultsTable", "rrSjfResultsStats", "rr_sjf"),
            ("Round Robin Prioridad", self.scheduler.schedule_round_robin_priority, "rrPriorityResultsTable", "rrPriorityResultsStats", "rr_priority")
        ]
        
        for name, method, table_attr, stats_attr, gantt_key in algorithms:
            try:
                # Ejecutar algoritmo
                results = method()
                self.current_results[gantt_key] = results
                
                # Llenar tabla
                if hasattr(self, table_attr) and hasattr(self, stats_attr):
                    table = getattr(self, table_attr)
                    stats_label = getattr(self, stats_attr)
                    self.populate_results_table(table, stats_label, results, name)
                
                # Mostrar diagrama de Gantt
                if gantt_key in self.gantt_widgets:
                    self.gantt_widgets[gantt_key].create_gantt_chart(results, name)
                
            except Exception as e:
                print(f"Error procesando {name}: {e}")
    
    def clear_results(self):
        """Limpia todos los resultados."""
        # Limpiar tablas
        tables = [
            'fifoResultsTable', 'sjfResultsTable', 'priorityResultsTable',
            'rrFifoResultsTable', 'rrSjfResultsTable', 'rrPriorityResultsTable'
        ]
        
        for attr in tables:
            if hasattr(self, attr):
                table = getattr(self, attr)
                table.setRowCount(0)
        
        # Limpiar labels de estadísticas
        stats_labels = [
            'fifoResultsStats', 'sjfResultsStats', 'priorityResultsStats',
            'rrFifoResultsStats', 'rrSjfResultsStats', 'rrPriorityResultsStats'
        ]
        
        for attr in stats_labels:
            if hasattr(self, attr):
                label = getattr(self, attr)
                label.setText("")
        
        # Limpiar diagramas de Gantt
        for gantt_widget in self.gantt_widgets.values():
            gantt_widget.clear_chart()
        
        # Limpiar resultados almacenados
        self.current_results.clear()
        
        # Regenerar tabla
        self.generate_table()