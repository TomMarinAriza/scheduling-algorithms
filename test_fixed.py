"""
Test directo con función incluida para evitar problemas de caché
"""

import copy
from process_structures import Process, SchedulingResults

def schedule_round_robin_fifo_fixed(processes, quantum=2):
    """Round Robin FIFO corregido"""
    if not processes:
        return SchedulingResults()
    
    results = SchedulingResults()
    processes = copy.deepcopy(processes)
    
    ready_queue = []
    current_time = 0
    completed = 0
    execution_order = []
    
    for p in processes:
        p.reset()
    
    while completed < len(processes):
        # Agregar procesos que han llegado a la cola de listos (orden FIFO)
        for process in processes:
            if (not process.completed and 
                process.arrival_time <= current_time and 
                process not in ready_queue):
                ready_queue.append(process)
        
        if ready_queue:
            # Tomar el primer proceso de la cola (FIFO)
            current_process = ready_queue.pop(0)
            
            # Calcular tiempo de ejecución (quantum o tiempo restante)
            execution_time = min(quantum, current_process.remaining_time)
            start_time = current_time
            current_time += execution_time
            
            # Actualizar proceso
            current_process.remaining_time -= execution_time
            
            # Agregar al diagrama de Gantt
            results.gantt_chart.append((current_process.id, start_time, execution_time))
            execution_order.append(f"P{current_process.id}")
            
            print(f"  DEBUG: P{current_process.id} ejecutó de {start_time}-{current_time}")
            print(f"  DEBUG: Cola antes de agregar nuevos: {[p.id for p in ready_queue]}")
            
            # CLAVE: Agregar procesos que llegaron DURANTE la ejecución
            for process in processes:
                if (not process.completed and 
                    process.arrival_time <= current_time and 
                    process not in ready_queue):
                    print(f"  DEBUG: Agregando P{process.id} que llegó en tiempo {process.arrival_time}")
                    ready_queue.append(process)
            
            print(f"  DEBUG: Cola después de agregar nuevos: {[p.id for p in ready_queue]}")
            
            # Verificar si el proceso terminó
            if current_process.remaining_time == 0:
                current_process.completion_time = current_time
                current_process.completed = True
                current_process.calculate_times()
                completed += 1
                print(f"  DEBUG: P{current_process.id} TERMINÓ")
            else:
                # El proceso no terminó, agregarlo al final de la cola
                ready_queue.append(current_process)
                print(f"  DEBUG: P{current_process.id} regresa al final (restante: {current_process.remaining_time})")
            
            print(f"  DEBUG: Cola final: {[p.id for p in ready_queue]}\\n")
        else:
            # No hay procesos listos, avanzar el tiempo
            current_time += 1
    
    results.processes = processes
    results.execution_order = " -> ".join(execution_order)
    results.algorithm_title = f"Round Robin + FIFO (Q={quantum})"
    results.calculate_averages()
    
    return results

def test_fixed():
    """Test con función corregida incluida directamente"""
    print("=== TEST CON FUNCIÓN CORREGIDA ===")
    
    processes = [
        Process(pid=1, arrival_time=0, burst_time=4, priority=3),
        Process(pid=2, arrival_time=1, burst_time=2, priority=1)
    ]
    
    print("PROCESOS:")
    print("P1: Llegada=0, Ráfaga=4")  
    print("P2: Llegada=1, Ráfaga=2")
    print("Quantum=2\\n")
    
    result = schedule_round_robin_fifo_fixed(processes, quantum=2)
    
    print("RESULTADO CORREGIDO:")
    for pid, start, duration in result.gantt_chart:
        print(f"  P{pid}: tiempo {start}-{start+duration}")
    
    print(f"\\nSecuencia: {result.execution_order}")
    
    if result.execution_order == "P1 -> P2 -> P1":
        print("✅ ¡CORRECTO! El orden ahora es el esperado")
    else:
        print("❌ Aún hay problema con el orden")

if __name__ == "__main__":
    test_fixed()