"""
Implementación del algoritmo de planificación por prioridad.
"""

import copy
from process_structures import SchedulingResults


def schedule_priority(processes, quantum=None):
    """Implementa el algoritmo de planificación por prioridad."""
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
            # Seleccionar el proceso con mayor prioridad (menor número = mayor prioridad)
            selected = min(available, key=lambda p: p.priority)
            
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
    results.algorithm_title = "Priority"
    
    return results