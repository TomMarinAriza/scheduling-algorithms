"""
Módulo que contiene la implementación de los algoritmos de planificación de procesos.
"""

import copy
from process_structures import Process, SchedulingResults


class ProcessScheduler:
    """Clase que implementa diferentes algoritmos de planificación de procesos."""
    
    def __init__(self):
        self.processes = []
        self.quantum = 2
    
    def set_processes(self, processes):
        """Establece la lista de procesos a planificar."""
        self.processes = copy.deepcopy(processes)
    
    def set_quantum(self, quantum):
        """Establece el quantum para Round Robin."""
        self.quantum = quantum
    
    def _prepare_processes(self):
        """Prepara los procesos resetando sus valores."""
        for process in self.processes:
            process.reset()
    
    def _finalize_results(self, results, algorithm_name):
        """Finaliza los resultados calculando tiempos y promedios."""
        for process in results.processes:
            process.calculate_times()
        results.calculate_averages()
        return results
    
    def schedule_fifo(self):
        """Implementa el algoritmo FIFO (First In First Out)."""
        if not self.processes:
            return SchedulingResults()
        
        self._prepare_processes()
        results = SchedulingResults()
        
        # Ordenar por tiempo de llegada
        sorted_processes = sorted(self.processes, key=lambda p: p.arrival_time)
        
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
        
        return self._finalize_results(results, "FIFO")
    
    def schedule_sjf(self):
        """Implementa el algoritmo SJF (Shortest Job First)."""
        if not self.processes:
            return SchedulingResults()
        
        self._prepare_processes()
        results = SchedulingResults()
        
        processes = copy.deepcopy(self.processes)
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
        
        return self._finalize_results(results, "SJF")
    
    def schedule_priority(self):
        """Implementa el algoritmo de planificación por prioridad."""
        if not self.processes:
            return SchedulingResults()
        
        self._prepare_processes()
        results = SchedulingResults()
        
        processes = copy.deepcopy(self.processes)
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
        
        return self._finalize_results(results, "Priority")
    
    def schedule_round_robin_fifo(self):
        """Implementa Round Robin con cola FIFO."""
        if not self.processes:
            return SchedulingResults()
        
        self._prepare_processes()
        results = SchedulingResults()
        
        processes = copy.deepcopy(self.processes)
        current_time = 0
        completed = 0
        ready_queue = []
        execution_order = []
        in_queue = set()
        
        while completed < len(processes):
            # Agregar procesos que llegaron a la cola ready
            for process in processes:
                if (not process.completed and 
                    process.id not in in_queue and 
                    process.arrival_time <= current_time):
                    ready_queue.append(process)
                    in_queue.add(process.id)
            
            if ready_queue:
                current_process = ready_queue.pop(0)
                in_queue.remove(current_process.id)
                
                # Ejecutar por quantum o hasta completar
                execution_time = min(self.quantum, current_process.remaining_time)
                start_time = current_time
                current_time += execution_time
                current_process.remaining_time -= execution_time
                
                # Agregar al diagrama de Gantt
                results.gantt_chart.append((current_process.id, start_time, execution_time))
                execution_order.append(f"P{current_process.id}")
                
                # Agregar nuevos procesos que llegaron durante la ejecución
                for process in processes:
                    if (not process.completed and 
                        process.id not in in_queue and 
                        process.arrival_time <= current_time and
                        process.id != current_process.id):
                        ready_queue.append(process)
                        in_queue.add(process.id)
                
                # Verificar si el proceso se completó
                if current_process.remaining_time == 0:
                    current_process.completion_time = current_time
                    current_process.completed = True
                    completed += 1
                else:
                    # Regresar a la cola
                    ready_queue.append(current_process)
                    in_queue.add(current_process.id)
            else:
                current_time += 1
        
        results.processes = processes
        results.execution_order = " -> ".join(execution_order)
        
        return self._finalize_results(results, f"Round Robin FIFO (Q={self.quantum})")
    
    def schedule_round_robin_sjf(self):
        """Implementa Round Robin con planificación SJF dentro del quantum."""
        if not self.processes:
            return SchedulingResults()
        
        self._prepare_processes()
        results = SchedulingResults()
        
        processes = copy.deepcopy(self.processes)
        current_time = 0
        completed = 0
        execution_order = []
        
        while completed < len(processes):
            # Encontrar procesos disponibles
            available = [p for p in processes if not p.completed and p.arrival_time <= current_time]
            
            if available:
                # Ordenar por tiempo restante (SJF)
                available.sort(key=lambda p: p.remaining_time)
                selected = available[0]
                
                # Ejecutar por quantum o hasta completar
                execution_time = min(self.quantum, selected.remaining_time)
                start_time = current_time
                current_time += execution_time
                selected.remaining_time -= execution_time
                
                # Agregar al diagrama de Gantt
                results.gantt_chart.append((selected.id, start_time, execution_time))
                execution_order.append(f"P{selected.id}")
                
                # Verificar si se completó
                if selected.remaining_time == 0:
                    selected.completion_time = current_time
                    selected.completed = True
                    completed += 1
            else:
                current_time += 1
        
        results.processes = processes
        results.execution_order = " -> ".join(execution_order)
        
        return self._finalize_results(results, f"Round Robin SJF (Q={self.quantum})")
    
    def schedule_round_robin_priority(self):
        """Implementa Round Robin con planificación por prioridad dentro del quantum."""
        if not self.processes:
            return SchedulingResults()
        
        self._prepare_processes()
        results = SchedulingResults()
        
        processes = copy.deepcopy(self.processes)
        current_time = 0
        completed = 0
        execution_order = []
        
        while completed < len(processes):
            # Encontrar procesos disponibles
            available = [p for p in processes if not p.completed and p.arrival_time <= current_time]
            
            if available:
                # Ordenar por prioridad
                available.sort(key=lambda p: p.priority)
                selected = available[0]
                
                # Ejecutar por quantum o hasta completar
                execution_time = min(self.quantum, selected.remaining_time)
                start_time = current_time
                current_time += execution_time
                selected.remaining_time -= execution_time
                
                # Agregar al diagrama de Gantt
                results.gantt_chart.append((selected.id, start_time, execution_time))
                execution_order.append(f"P{selected.id}")
                
                # Verificar si se completó
                if selected.remaining_time == 0:
                    selected.completion_time = current_time
                    selected.completed = True
                    completed += 1
            else:
                current_time += 1
        
        results.processes = processes
        results.execution_order = " -> ".join(execution_order)
        
        return self._finalize_results(results, f"Round Robin Priority (Q={self.quantum})")