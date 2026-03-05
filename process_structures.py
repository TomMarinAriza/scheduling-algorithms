"""
Módulo que contiene las estructuras de datos para los procesos y resultados de planificación.
"""

class Process:
    """Clase que representa un proceso del sistema."""
    
    def __init__(self, pid=0, arrival_time=0, burst_time=0, priority=0):
        self.id = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.quantum = 2  
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completed = False
    
    def reset(self):
        """Reinicia el proceso a su estado inicial."""
        self.remaining_time = self.burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completed = False
    
    def calculate_times(self):
        """Calcula los tiempos de espera y retorno."""
        self.turnaround_time = self.completion_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time
    
    def __str__(self):
        return f"P{self.id} (Llegada: {self.arrival_time}, Rafaga: {self.burst_time}, Prioridad: {self.priority})"


class SchedulingResults:
    """Clase que almacena los resultados de un algoritmo de planificación."""
    
    def __init__(self):
        self.processes = []
        self.gantt_chart = []  # Lista de tuplas (process_id, start_time, duration)
        self.avg_waiting_time = 0.0
        self.avg_turnaround_time = 0.0
        self.execution_order = ""
        self.algorithm_title = ""  # Título del algoritmo con detalles
    
    def calculate_averages(self):
        """Calcula los tiempos promedio de espera y retorno."""
        if not self.processes:
            return
        
        total_waiting = sum(p.waiting_time for p in self.processes)
        total_turnaround = sum(p.turnaround_time for p in self.processes)
        
        self.avg_waiting_time = total_waiting / len(self.processes)
        self.avg_turnaround_time = total_turnaround / len(self.processes)
    
    def get_summary_text(self, algorithm_name):
        """Genera un resumen textual de los resultados."""
        text = f"╔═══════════════════════════════════════════════════════════════════════╗\n"
        text += f"║{algorithm_name.center(71)}║\n"
        text += f"╚═══════════════════════════════════════════════════════════════════════╝\n\n"
        
        text += f"Orden de Ejecucion: {self.execution_order}\n\n"
        
        # Tabla de resultados con mejor formato
        text += f"┌─────────┬─────────┬─────────┬──────────┬─────────────┬─────────┬──────────┐\n"
        text += f"│ Proceso │ Llegada │  Rafaga │ Prioridad│ Finalizacion│  Espera │  Retorno │\n"
        text += f"├─────────┼─────────┼─────────┼──────────┼─────────────┼─────────┼──────────┤\n"
        
        for process in self.processes:
            text += f"│   P{process.id:<4} │   {process.arrival_time:<4}  │   {process.burst_time:<4}  │    {process.priority:<5} │     {process.completion_time:<6}  │   {process.waiting_time:<4}  │    {process.turnaround_time:<5} │\n"
        
        text += f"└─────────┴─────────┴─────────┴──────────┴─────────────┴─────────┴──────────┘\n\n"
        
        # Solo estadísticas básicas
        text += f"Tiempo de Espera Promedio: {self.avg_waiting_time:.2f}\n"
        text += f"Tiempo de Retorno Promedio: {self.avg_turnaround_time:.2f}\n"
        
        return text