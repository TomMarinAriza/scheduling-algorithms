"""
Implementación del algoritmo SJF (Shortest Job First).
"""

import copy
from process_structures import SchedulingResults


def schedule_sjf(processes, quantum=None):
    """Implementa el algoritmo SJF (Shortest Job First)."""
    if not processes:
        return SchedulingResults()
    
    results = SchedulingResults()
    
    processes = copy.deepcopy(processes)
    current_time = 0
    completed = 0
    execution_order = []
    
    while completed < len(processes):
        # Encontrar procesos disponibles
        available = [p for p in processes if not p.completed and p.arrival_time <= current_time]
        
        if available:
            # Seleccionar el proceso con menor ráfaga
            selected = min(available, key=lambda p: p.burst_time)
            
            # Ejecutar el proceso
            start_time = current_time
            current_time += selected.burst_time
            selected.completion_time = current_time
            selected.completed = True
            completed += 1
            
            # Agregar al diagrama de Gantt y orden de ejecución
            results.gantt_chart.append((selected.id, start_time, selected.burst_time))
            execution_order.append(f"P{selected.id}")
        else:
            current_time += 1
    
    results.processes = processes
    results.execution_order = " -> ".join(execution_order)
    results.algorithm_title = "SJF"
    
    return results