"""
Test específico para demostrar el problema de orden en Round Robin
"""

from process_structures import Process
from algorithm_rr_fifo import schedule_round_robin_fifo

def test_simple_case():
    """Test simple que demuestra el problema de orden"""
    print("=== TEST SIMPLE PARA DEMOSTRAR PROBLEMA ===")
    
    # Caso simple: P1 llega en 0, P2 llega en 1
    processes = [
        Process(pid=1, arrival_time=0, burst_time=4, priority=3),
        Process(pid=2, arrival_time=1, burst_time=2, priority=1)
    ]
    
    print("PROCESOS:")
    print("P1: Llegada=0, Ráfaga=4")  
    print("P2: Llegada=1, Ráfaga=2")
    print("Quantum=2\n")
    
    result = schedule_round_robin_fifo(processes, quantum=2)
    
    print("RESULTADO ACTUAL:")
    for pid, start, duration in result.gantt_chart:
        print(f"  P{pid}: tiempo {start}-{start+duration}")
    
    print(f"Secuencia: {result.execution_order}\n")
    
    print("LO QUE DEBERÍA SER:")
    print("  P1: tiempo 0-2  (P2 llega en tiempo 1, espera)")
    print("  P2: tiempo 2-4  (P2 ejecuta porque ya estaba esperando)")  
    print("  P1: tiempo 4-6  (P1 regresa para terminar)")
    print("Secuencia correcta: P1 -> P2 -> P1")

if __name__ == "__main__":
    test_simple_case()