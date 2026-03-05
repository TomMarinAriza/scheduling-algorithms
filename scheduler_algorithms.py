"""
Módulo que contiene la implementación de los algoritmos de planificación de procesos.
"""

import copy
from process_structures import Process, SchedulingResults

# Importar algoritmos modulares
from algorithm_fifo import schedule_fifo
from algorithm_sjf import schedule_sjf
from algorithm_priority import schedule_priority
from algorithm_rr_fifo import schedule_round_robin_fifo
from algorithm_rr_sjf import schedule_round_robin_sjf
from algorithm_rr_priority import schedule_round_robin_priority


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
    
    def _finalize_results(self, results):
        """Finaliza los resultados calculando tiempos y promedios."""
        for process in results.processes:
            process.calculate_times()
        results.calculate_averages()
        return results
    
    def schedule_fifo(self):
        """Implementa el algoritmo FIFO (First In First Out)."""
        self._prepare_processes()
        results = schedule_fifo(self.processes)
        return self._finalize_results(results)
    
    def schedule_sjf(self):
        """Implementa el algoritmo SJF (Shortest Job First)."""
        self._prepare_processes()
        results = schedule_sjf(self.processes)
        return self._finalize_results(results)
    
    def schedule_priority(self):
        """Implementa el algoritmo de planificación por prioridad."""
        self._prepare_processes()
        results = schedule_priority(self.processes)
        return self._finalize_results(results)
    
    def schedule_round_robin_fifo(self):
        """Implementa Round Robin con cola FIFO."""
        self._prepare_processes()
        results = schedule_round_robin_fifo(self.processes, self.quantum)
        return self._finalize_results(results)
    
    def schedule_round_robin_sjf(self):
        """Implementa Round Robin con planificación SJF."""
        self._prepare_processes()
        results = schedule_round_robin_sjf(self.processes, self.quantum)
        return self._finalize_results(results)
    
    def schedule_round_robin_priority(self):
        """Implementa Round Robin con planificación por prioridad."""
        self._prepare_processes()
        results = schedule_round_robin_priority(self.processes, self.quantum)
        return self._finalize_results(results)