"""
Implementación del algoritmo Round Robin con Priority Scheduling.
Los nuevos procesos que llegan se insertan en la cola de listos según prioridad,
pero una vez en la cola, siguen el orden Round Robin (circular).
"""

import copy
from process_structures import SchedulingResults


def schedule_round_robin_priority(processes, quantum=2):
    """
    Implementa el algoritmo Round Robin con inserción por prioridad.
    Los nuevos procesos se insertan según prioridad, pero el orden de ejecución
    sigue siendo Round Robin (circular).
    
    Args:
        processes: Lista de procesos a planificar
        quantum: Quantum de tiempo para cada proceso (default=2)
        
    Returns:
        SchedulingResults: Resultados de la planificación
    """
    if not processes:
        return SchedulingResults()
    
    results = SchedulingResults()
    processes = copy.deepcopy(processes)
    
    # Cola de procesos listos (Priority - se ordenan por prioridad)
    ready_queue = []
    current_time = 0
    completed = 0
    execution_order = []
    
    # Reiniciar todos los procesos
    for p in processes:
        p.reset()
    
    while completed < len(processes):
        # Agregar nuevos procesos que han llegado a la cola de listos
        # Los nuevos procesos se insertan según prioridad
        new_arrivals = []
        for process in processes:
            if (not process.completed and 
                process.remaining_time > 0 and
                process.arrival_time <= current_time and 
                process not in ready_queue):
                new_arrivals.append(process)
        
        # Insertar nuevos procesos en orden de prioridad
        if new_arrivals:
            new_arrivals.sort(key=lambda p: p.priority)
            ready_queue.extend(new_arrivals)
        
        if ready_queue:
            # Tomar el primer proceso de la cola (orden Round Robin)
            current_process = ready_queue.pop(0)

            # Salvaguarda contra entradas duplicadas o inconsistentes.
            if current_process.completed or current_process.remaining_time <= 0:
                continue
            
            # Calcular tiempo de ejecución (quantum o tiempo restante)
            execution_time = min(quantum, current_process.remaining_time)
            start_time = current_time
            current_time += execution_time
            
            # Actualizar proceso
            current_process.remaining_time -= execution_time
            
            # Agregar al diagrama de Gantt
            results.gantt_chart.append((current_process.id, start_time, execution_time))
            execution_order.append(f"P{current_process.id}")
            
            # Agregar procesos que llegaron DURANTE la ejecución
            new_arrivals = []
            for process in processes:
                if (not process.completed and 
                    process.remaining_time > 0 and
                    process.arrival_time <= current_time and 
                    process != current_process and
                    process not in ready_queue):
                    new_arrivals.append(process)
            
            if new_arrivals:
                new_arrivals.sort(key=lambda p: p.priority)
                ready_queue.extend(new_arrivals)
            
            # Verificar si el proceso terminó
            if current_process.remaining_time == 0:
                current_process.completion_time = current_time
                current_process.completed = True
                current_process.calculate_times()
                completed += 1
            else:
                # El proceso no terminó, agregarlo al final de la cola
                ready_queue.append(current_process)
        else:
            # No hay procesos listos, avanzar el tiempo
            current_time += 1
    
    results.processes = processes
    results.execution_order = " -> ".join(execution_order)
    results.algorithm_title = f"Round Robin + Priority (Q={quantum})"
    results.calculate_averages()
    
    return results