"""
Módulo para crear y mostrar diagramas de Gantt de los algoritmos de planificación.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class GanttChartWidget(FigureCanvas):
    """Widget personalizado para mostrar diagramas de Gantt en PyQt5."""
    
    def __init__(self, parent=None, width=12, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        
        # Colores para los procesos
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
                       '#FFEAA7', '#DDA0DD', '#98D8C8', '#F06292',
                       '#AED581', '#FFB74D', '#81C784', '#64B5F6']
    
    def clear_chart(self):
        """Limpia el diagrama."""
        self.fig.clear()
        self.draw()
    
    def create_gantt_chart(self, results, title="Diagrama de Gantt"):
        """Crea un diagrama de Gantt basado en los resultados de planificación."""
        self.fig.clear()
        
        if not results.gantt_chart:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, 'No hay datos para mostrar', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14)
            self.draw()
            return
        
        ax = self.fig.add_subplot(111)
        
        # Obtener información del diagrama de Gantt
        gantt_data = results.gantt_chart
        process_ids = list(set([entry[0] for entry in gantt_data]))
        process_ids.sort()
        
        # Mapear procesos a posiciones en Y
        y_positions = {pid: i for i, pid in enumerate(process_ids)}
        
        # Crear barras del diagrama de Gantt
        for process_id, start_time, duration in gantt_data:
            color = self.colors[process_id % len(self.colors)]
            y_pos = y_positions[process_id]
            
            # Crear barra
            bar = ax.barh(y_pos, duration, left=start_time, height=0.6, 
                         color=color, alpha=0.7, edgecolor='black', linewidth=0.5)
            
            # Agregar etiqueta del proceso en la barra
            if duration > 0.5:  # Solo mostrar etiqueta si la barra es suficientemente ancha
                ax.text(start_time + duration/2, y_pos, f'P{process_id}', 
                       ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Configurar ejes
        ax.set_xlabel('Tiempo', fontsize=12, fontweight='bold')
        ax.set_ylabel('Procesos', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Configurar etiquetas del eje Y
        ax.set_yticks(range(len(process_ids)))
        ax.set_yticklabels([f'P{pid}' for pid in process_ids])
        
        # Configurar grid
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Ajustar límites
        max_time = max([start + duration for _, start, duration in gantt_data])
        ax.set_xlim(0, max_time * 1.05)
        ax.set_ylim(-0.5, len(process_ids) - 0.5)
        
        # Agregar líneas de tiempo en el eje X
        time_ticks = list(range(0, int(max_time) + 1))
        ax.set_xticks(time_ticks)
        
        # Agregar información adicional
        info_text = f"Tiempo total: {max_time}\n"
        info_text += f"Tiempo promedio espera: {results.avg_waiting_time:.2f}\n"
        info_text += f"Tiempo promedio retorno: {results.avg_turnaround_time:.2f}"
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
               verticalalignment='top', bbox=dict(boxstyle='round', 
               facecolor='lightblue', alpha=0.5), fontsize=10)
        
        # Ajustar layout
        self.fig.tight_layout()
        self.draw()
    
    def create_comparison_chart(self, all_results, algorithm_names):
        """Crea un gráfico comparativo de múltiples algoritmos."""
        self.fig.clear()
        
        if not all_results:
            return
        
        # Crear subgráficos
        n_algorithms = len(all_results)
        fig_height = max(2 * n_algorithms, 8)
        
        for i, (results, name) in enumerate(zip(all_results, algorithm_names)):
            ax = self.fig.add_subplot(n_algorithms, 1, i + 1)
            
            if not results.gantt_chart:
                ax.text(0.5, 0.5, f'{name}: No hay datos', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, fontsize=12)
                continue
            
            # Crear diagrama de Gantt simplificado
            gantt_data = results.gantt_chart
            process_ids = list(set([entry[0] for entry in gantt_data]))
            process_ids.sort()
            
            y_positions = {pid: 0 for pid in process_ids}  # Todos en la misma línea para comparación
            
            for process_id, start_time, duration in gantt_data:
                color = self.colors[process_id % len(self.colors)]
                
                ax.barh(0, duration, left=start_time, height=0.4, 
                       color=color, alpha=0.7, edgecolor='black', linewidth=0.5)
                
                # Etiqueta del proceso
                if duration > 0.3:
                    ax.text(start_time + duration/2, 0, f'P{process_id}', 
                           ha='center', va='center', fontweight='bold', fontsize=9)
            
            # Configuración del subgráfico
            ax.set_title(f'{name} (Espera: {results.avg_waiting_time:.1f}, '
                        f'Retorno: {results.avg_turnaround_time:.1f})', 
                        fontsize=11, fontweight='bold')
            ax.set_xlim(0, max([start + duration for _, start, duration in gantt_data]) * 1.05)
            ax.set_ylim(-0.3, 0.3)
            ax.set_yticks([])
            ax.grid(True, axis='x', alpha=0.3)
            
            # Solo mostrar etiquetas X en el último gráfico
            if i == n_algorithms - 1:
                ax.set_xlabel('Tiempo', fontweight='bold')
            else:
                ax.set_xticks([])
        
        self.fig.tight_layout()
        self.draw()


def create_gantt_window(results, title="Diagrama de Gantt"):
    """Crea una ventana independiente con el diagrama de Gantt."""
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    
    # Verificar si hay una aplicación Qt ejecutándose
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Crear ventana
    window = QMainWindow()
    window.setWindowTitle(title)
    window.setGeometry(100, 100, 1000, 600)
    
    # Crear widget central
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # Crear layout
    layout = QVBoxLayout()
    central_widget.setLayout(layout)
    
    # Crear y agregar el diagrama de Gantt
    gantt_widget = GanttChartWidget()
    gantt_widget.create_gantt_chart(results, title)
    layout.addWidget(gantt_widget)
    
    # Mostrar ventana
    window.show()
    
    return window