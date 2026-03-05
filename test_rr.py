"""
Test para verificar el comportamiento de los algoritmos Round Robin
"""

from process_structures import Process
from algorithm_rr_fifo import schedule_round_robin_fifo
from algorithm_rr_sjf import schedule_round_robin_sjf  
from algorithm_rr_priority import schedule_round_robin_priority

def create_test_processes():
    """Crear procesos de prueba para verificar Round Robin"""
    processes = [
        Process(pid=1, arrival_time=0, burst_time=6, priority=3),
        Process(pid=2, arrival_time=1, burst_time=4, priority=1), 
        Process(pid=3, arrival_time=3, burst_time=5, priority=2),
        Process(pid=4, arrival_time=5, burst_time=3, priority=4)
    ]
    return processes

def analyze_round_robin_behavior(gantt_chart, algorithm_name):
    """Analizar si el comportamiento cumple con Round Robin verdadero"""
    print(f"\n=== ANÁLISIS DE {algorithm_name} ===")
    print("Diagrama de Gantt:")
    
    # Mostrar secuencia de ejecución
    execution_sequence = []
    process_completion_times = {}
    
    for pid, start_time, duration in gantt_chart:
        execution_sequence.append(f"P{pid}")
        print(f"  P{pid}: tiempo {start_time}-{start_time + duration} (duración: {duration})")
        
        # Rastrear cuándo termina cada proceso
        end_time = start_time + duration
        if pid not in process_completion_times:
            # Primera ejecución
            process_completion_times[pid] = end_time
        else:
            # Actualizar tiempo de finalización
            process_completion_times[pid] = end_time
    
    print(f"\nSecuencia: {' -> '.join(execution_sequence)}")
    
    # Verificar si hay repeticiones inmediatas (violación de Round Robin)
    violations = []
    for i in range(len(execution_sequence) - 1):
        current_process = execution_sequence[i]
        next_process = execution_sequence[i + 1]
        
        if current_process == next_process:
            # Verificar si esto ocurre cuando es el último proceso activo
            current_time = gantt_chart[i][1] + gantt_chart[i][2]  # tiempo final de ejecución actual
            
            # Determinar qué procesos aún están activos en ese momento
            active_processes = set()
            for j, (pid, start, dur) in enumerate(gantt_chart):
                if j <= i:  # Solo considerar ejecuciones hasta este punto
                    active_processes.add(pid)
            
            # Si hay más de un proceso activo, es una violación real
            if len(active_processes) > 1:
                # Verificar si hay otros procesos que no han terminado completamente
                other_processes_remaining = False
                for pid in active_processes:
                    if pid != int(current_process[1:]):  # Excluir el proceso actual
                        # Verificar si este proceso ejecuta después
                        for k in range(i+2, len(gantt_chart)):
                            if gantt_chart[k][0] == pid:
                                other_processes_remaining = True
                                break
                
                if other_processes_remaining:
                    violations.append(f"Violación en posición {i}: {current_process} -> {next_process}")
    
    # Analizar rondas completas
    print("\n--- ANÁLISIS DE RONDAS ---")
    process_counts = {}
    round_number = 1
    processes_in_round = set()
    
    for i, process in enumerate(execution_sequence):
        if process in processes_in_round:
            # Nueva ronda detectada
            print(f"Ronda {round_number}: {processes_in_round}")
            round_number += 1
            processes_in_round = {process}
        else:
            processes_in_round.add(process)
    
    if processes_in_round:
        print(f"Ronda {round_number}: {processes_in_round}")
    
    # Resultado del análisis
    print("\n--- RESULTADO ---")
    if violations:
        print("❌ FALLA: Se detectaron violaciones de Round Robin:")
        for violation in violations:
            print(f"  • {violation}")
        print("  Los procesos no deberían ejecutar dos veces seguidas cuando hay otros procesos disponibles.")
    else:
        print("✅ CORRECTO: No se detectaron violaciones de Round Robin.")
        print("  Cada proceso ejecuta solo una vez antes de pasar al siguiente (excepto cuando es el último restante).")
    
    return len(violations) == 0

def test_round_robin_algorithms():
    """Ejecutar test completo de algoritmos Round Robin"""
    print("🧪 INICIANDO PRUEBAS DE ALGORITMOS ROUND ROBIN")
    print("=" * 60)
    
    # Crear procesos de prueba
    processes = create_test_processes()
    quantum = 2
    
    print("\nPROCESOS DE PRUEBA:")
    print("PID | Llegada | Ráfaga | Prioridad | Tiempo Restante")
    print("-" * 50)
    for p in processes:
        print(f"P{p.id:2d} |   {p.arrival_time:3d}   |   {p.burst_time:2d}   |    {p.priority:2d}     |      {p.remaining_time:2d}")
    
    print(f"\nQuantum = {quantum}")
    
    # Probar cada algoritmo
    algorithms = [
        ("Round Robin FIFO", schedule_round_robin_fifo),
        ("Round Robin SJF", schedule_round_robin_sjf),
        ("Round Robin Priority", schedule_round_robin_priority)
    ]
    
    results = {}
    
    for name, algorithm_func in algorithms:
        print("\n" + "=" * 60)
        
        # Resetear procesos
        test_processes = []
        for p in processes:
            new_process = Process(p.id, p.arrival_time, p.burst_time, p.priority)
            test_processes.append(new_process)
        
        # Ejecutar algoritmo
        try:
            result = algorithm_func(test_processes, quantum)
            results[name] = analyze_round_robin_behavior(result.gantt_chart, name)
            print(f"\nOrden de ejecución: {result.execution_order}")
            print(f"Título del algoritmo: {result.algorithm_title}")
            
        except Exception as e:
            print(f"❌ ERROR en {name}: {str(e)}")
            results[name] = False
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    all_passed = True
    for algorithm, passed in results.items():
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{algorithm}: {status}")
        if not passed:
            all_passed = False
    
    print(f"\n{'🎉 TODOS LOS TESTS PASARON' if all_passed else '⚠️  ALGUNOS TESTS FALLARON'}")
    print("=" * 60)

if __name__ == "__main__":
    test_round_robin_algorithms()