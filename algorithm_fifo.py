"""
Implementación del algoritmo FIFO (First In First Out).
"""

from process_structures import SchedulingResults


def schedule_fifo(processes, quantum=None):
    """Implementa el algoritmo FIFO (First In First Out)."""
    if not processes:
        return SchedulingResults()
    
    results = SchedulingResults()
    
    # Ordenar por tiempo de llegada
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    
    current_time = 0
    execution_order = []
    
    for process in sorted_processes:
        # Si el proceso llega después del tiempo actual, esperar
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        
        # Ejecutar el proceso
        start_time = current_time
        current_time += process.burst_time
        process.completion_time = current_time
        
        # Agregar al diagrama de Gantt
        results.gantt_chart.append((process.id, start_time, process.burst_time))
        execution_order.append(f"P{process.id}")
    
    results.processes = sorted_processes
    results.execution_order = " -> ".join(execution_order)
    results.algorithm_title = "FIFO"
    
    return results