"""
Test con debug para entender el problema paso a paso
"""

from process_structures import Process
import copy

def debug_round_robin_fifo(processes, quantum=2):
    """Round Robin FIFO con debug detallado"""
    processes = copy.deepcopy(processes)
    
    for p in processes:
        p.reset()
    
    ready_queue = []
    current_time = 0
    completed = 0
    execution_order = []
    step = 1
    
    print(f"\\n=== INICIANDO SIMULACION ===")
    print(f"Quantum: {quantum}")
    
    while completed < len(processes):
        print(f"\\n--- PASO {step} (Tiempo actual: {current_time}) ---")
        
        # Agregar procesos que han llegado
        before_queue = [p.id for p in ready_queue]
        for process in processes:
            if (not process.completed and 
                process.arrival_time <= current_time and 
                process not in ready_queue):
                ready_queue.append(process)
                print(f"  ➤ P{process.id} agregado a cola (llegó en tiempo {process.arrival_time})")
        
        after_queue = [p.id for p in ready_queue]
        print(f"  Cola antes: {before_queue} → Cola después: {after_queue}")
        
        if ready_queue:
            current_process = ready_queue.pop(0)
            print(f"  🎯 Ejecutando P{current_process.id} (tiempo restante: {current_process.remaining_time})")
            
            execution_time = min(quantum, current_process.remaining_time)
            start_time = current_time
            current_time += execution_time
            
            current_process.remaining_time -= execution_time
            execution_order.append(f"P{current_process.id}")
            
            print(f"      Ejecuta de {start_time} a {current_time} (duración: {execution_time})")
            print(f"      Tiempo restante después: {current_process.remaining_time}")
            
            # Agregar procesos que llegaron DURANTE la ejecución
            new_during_exec = []
            for process in processes:
                if (not process.completed and 
                    process.arrival_time <= current_time and 
                    process not in ready_queue and process != current_process):
                    new_during_exec.append(process)
                    ready_queue.append(process)
                    print(f"      ➤ P{process.id} llegó durante ejecución (tiempo {process.arrival_time})")
            
            if current_process.remaining_time == 0:
                print(f"      ✅ P{current_process.id} TERMINADO")
                current_process.completion_time = current_time
                current_process.completed = True
                completed += 1
            else:
                print(f"      ↻ P{current_process.id} regresa al final de la cola")
                ready_queue.append(current_process)
            
            print(f"      Nueva cola: {[p.id for p in ready_queue]}")
        else:
            print(f"  ⏰ No hay procesos listos, avanzando tiempo")
            current_time += 1
        
        step += 1
        if step > 20:  # Evitar loop infinito
            print("  ⚠️ Límite de pasos alcanzado")
            break
    
    return " -> ".join(execution_order)

if __name__ == "__main__":
    processes = [
        Process(pid=1, arrival_time=0, burst_time=4, priority=3),
        Process(pid=2, arrival_time=1, burst_time=2, priority=1)
    ]
    
    result = debug_round_robin_fifo(processes, quantum=2)
    print(f"\\n🎯 RESULTADO FINAL: {result}")
    print(f"🎯 ESPERADO: P1 -> P2 -> P1")