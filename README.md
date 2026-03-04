# Simulador de Planificación de Procesos

## Descripción
Aplicación GUI desarrollada en **Python (PyQt5)** y **C++ (Qt)** que implementa algoritmos de planificación de procesos del sistema operativo con interfaz gráfica intuitiva.

## Versiones Disponibles

### 🐍 Python Version (PyQt5) - Completa ✅
- Diagramas de Gantt interactivos con matplotlib
- Interfaz gráfica avanzada
- Tests automatizados
- Archivo principal: `main.py`

### ⚡ C++ Version (Qt) - Nueva ✨  
- Interfaz nativa con Qt Widgets
- Mayor rendimiento y velocidad
- Compilación estática posible
- Archivos principales: `main.cpp`, `main_window.cpp`

**Ambas versiones comparten el mismo archivo `mainwindow.ui`** para consistencia de interfaz.

## Características

### Algoritmos Implementados
- **FIFO** (First In, First Out)
- **SJF** (Shortest Job First)  
- **Priority** (Planificación por Prioridad)
- **Round Robin + FIFO**
- **Round Robin + SJF**
- **Round Robin + Priority**

### Funcionalidades
- ✅ Interfaz gráfica intuitiva con PyQt5
- ✅ Diagramas de Gantt interactivos
- ✅ Cálculo automático de tiempos de espera y respuesta
- ✅ **Quantum global**: El valor de quantum se aplica a todos los procesos por igual
- ✅ Soporte para múltiples procesos (hasta 20)
- ✅ Exportación de resultados

## Uso del Quantum

### ⚠️ Importante: Quantum Global
El sistema utiliza un **quantum global** que se aplica a todos los procesos por igual:

1. **Control Principal**: Usa el spinbox "Quantum" en la parte superior para establecer el valor
2. **Columna Quantum**: La columna "Quantum*" en la tabla es **informativa** y no editable
3. **Actualización Automática**: Al cambiar el quantum superior, la tabla se actualiza automáticamente

### Ejemplo
- Si estableces Quantum = 3 en el control superior
- **TODOS** los procesos usarán quantum = 3 en Round Robin
- La columna "Quantum*" mostrará el mismo valor para todos

## Estructura del Proyecto

### 📁 Archivos Compartidos
```
mainwindow.ui             # Diseño de interfaz (Qt Designer) - Compartido ✨
```

### 🐍 Archivos Python
```
├── main.py                    # Punto de entrada Python
├── main_window.py             # Lógica de interfaz Python  
├── process_structures.py      # Clases de datos Python
├── scheduler_algorithms.py    # Algoritmos Python
├── gantt_chart.py            # Diagramas de Gantt (matplotlib)
├── test_algorithms.py        # Tests de validación
└── test_quantum_global.py    # Test quantum global
```

### ⚡ Archivos C++
```
├── main.cpp                   # Punto de entrada C++
├── main_window.h              # Header ventana principal
├── main_window.cpp            # Implementación ventana principal
├── process_structures.h       # Header estructuras de datos  
├── process_structures.cpp     # Implementación estructuras
├── scheduler_algorithms.h     # Header algoritmos
├── scheduler_algorithms.cpp   # Implementación algoritmos
├── CMakeLists.txt            # Configuración CMake
└── ProcessScheduler.pro      # Archivo proyecto qmake
```

## Instalación y Ejecución

### 🐍 Versión Python

#### Requisitos
```bash
pip install PyQt5 matplotlib
```

#### Ejecutar
```bash
python main.py
```

### ⚡ Versión C++

#### Requisitos
- **Qt5 o Qt6** (módulos Core y Widgets)
- **C++17** compatible compiler
- **CMake 3.16+** o **qmake**

#### Compilación

**Método 1: qmake (Recomendado)**
```bash
# Generar Makefile
qmake ProcessScheduler.pro

# Compilar
make
# En Windows con MinGW:
mingw32-make

# Ejecutar
./ProcessScheduler
```

**Método 2: CMake**
```bash
# Crear directorio build
mkdir build && cd build

# Configurar
cmake ..

# Compilar
cmake --build .

# Ejecutar  
./ProcessScheduler
```

**Método 3: Qt Creator**
1. Abrir `ProcessScheduler.pro` en Qt Creator
2. Configurar el proyecto con tu kit Qt
3. Build and Run (Ctrl+R)

## Ejemplo de Uso

1. **Configurar Procesos**:
   - Número de Procesos: 3
   - Quantum: 2
   
2. **Editar Tabla**:
   - P1: Llegada=0, Ráfaga=8, Prioridad=1
   - P2: Llegada=1, Ráfaga=4, Prioridad=2
   - P3: Llegada=2, Ráfaga=6, Prioridad=3

3. **Calcular**: Click "Calcular Algoritmos"

4. **Resultados**: Todos los algoritmos Round Robin usarán quantum=2

## Comparación de Versiones

| Característica | Python (PyQt5) | C++ (Qt) |  
|---|---|---|
| **Rendimiento** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Desarrollo rápido** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Diagramas Gantt** | ✅ matplotlib | ⚠️ Requiere Qt Charts |
| **Compilación** | Intérprete | Nativo |
| **Distribución** | Requiere Python | Ejecutable standalone |
| **Debugging** | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## Notas Técnicas

### Compatibilidad UI
- El archivo `mainwindow.ui` es **compatible entre ambas versiones**
- PyQt5 y Qt C++ usan la misma estructura XML
- Widgets soportados: QTableWidget, QSpinBox, QComboBox, QPushButton, QLabel

### Algoritmos Implementados
Ambas versiones implementan los **6 algoritmos idénticos**:
1. **FIFO**: Orden de llegada
2. **SJF**: Trabajo más corto primero  
3. **Priority**: Por prioridad (menor número = mayor prioridad)
4. **RR+FIFO**: Round Robin con cola FIFO
5. **RR+SJF**: Round Robin con selección SJF
6. **RR+Priority**: Round Robin con selección por prioridad

### Quantum Global
- **Concepto**: Un solo valor de quantum para todos los procesos
- **Implementado**: En ambas versiones (Python y C++)
- **Interfaz**: Control spinbox superior actualiza toda la tabla

## Mejoras Futuras

### Python
- [ ] Exportar diagramas de Gantt como imágenes
- [ ] Modo animado de ejecución
- [ ] Más tests automatizados

### C++ 
- [ ] Implementar diagramas de Gantt con Qt Charts
- [ ] Exportar resultados a PDF/CSV
- [ ] Herramientas de profiling de rendimiento
- [ ] Packaging para distribución

## Licencia
Proyecto educativo para el curso de Sistemas Operativos.

## Tests de Verificación

```bash
# Test de algoritmos básicos
python test_algorithms.py

# Test de quantum global
python test_quantum_global.py
```

## Notas Técnicas

- Los procesos con ráfaga <= 0 no son válidos
- El quantum debe ser >= 1
- Los diagramas de Gantt son interactivos (zoom, pan)
- La aplicación maneja errores de entrada automáticamente