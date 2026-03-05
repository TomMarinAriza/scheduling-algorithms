# Simulador de Planificación de Procesos

## Descripción
Aplicación GUI desarrollada en Python con QT que implementa algoritmos de planificación de procesos del sistema operativo con interfaz gráfica intuitiva.


## Características

### Algoritmos Implementados
- **FIFO** (First In, First Out)
- **SJF** (Shortest Job First)  
- **Priority** (Planificación por Prioridad)
- **Round Robin + FIFO**
- **Round Robin + SJF**
- **Round Robin + Priority**

### Funcionalidades
- Interfaz gráfica intuitiva con PyQt5
- Diagramas de Gantt interactivos
- Cálculo automático de tiempos de espera y respuesta
- **Quantum global**: El valor de quantum se aplica a todos los procesos por igual
- Soporte para múltiples procesos (hasta 20)


## Uso del Quantum

### Importante: Quantum Global
El sistema utiliza un **quantum global** que se aplica a todos los procesos por igual:

1. **Control Principal**: Usa el spinbox "Quantum" en la parte superior para establecer el valor
2. **Columna Quantum**: La columna "Quantum*" en la tabla es **informativa** y no editable
3. **Actualización Automática**: Al cambiar el quantum superior, la tabla se actualiza automáticamente

### Ejemplo
- Si estableces Quantum = 3 en el control superior
- **TODOS** los procesos usarán quantum = 3 en Round Robin
- La columna "Quantum*" mostrará el mismo valor para todos

## Licencia
Proyecto educativo para el curso de Sistemas Operativos.

## Notas Técnicas

- Los procesos con ráfaga <= 0 no son válidos
- El quantum debe ser >= 1
- Los diagramas de Gantt son interactivos (zoom, pan)
- La aplicación maneja errores de entrada automáticamente

## Créditos

**Desarrolladores:**
- Santiago Guevara Méndez
- Tomás Marín Ariza