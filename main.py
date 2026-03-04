"""
Simulador de Algoritmos de Planificación de Procesos
Aplicación principal que ejecuta el simulador con interfaz gráfica.
"""

import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


def main():
    """Función principal que inicializa y ejecuta la aplicación."""
    app = QApplication(sys.argv)
    
    # Configurar la aplicación
    app.setApplicationName("Simulador de Algoritmos de Planificación")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Sistemas Operativos")
    
    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar la aplicación
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())