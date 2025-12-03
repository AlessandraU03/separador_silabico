"""
Universidad Politécnica de Chiapas
Lenguajes y Autómatas - Cuatrimestre 7
Práctica 3: Separador Silábico Básico (DFA e Implementación)

Autores: [Tu nombre y matrícula]
Fecha: Diciembre 2024

Descripción:
Este programa implementa un Autómata Finito Determinista (DFA) para la separación
silábica en español siguiendo las reglas de la Real Academia Española.

Módulos:
- reglas_silabicas.py: Define las reglas y clasificaciones
- separador_dfa.py: Implementa el DFA
- procesador_archivos.py: Gestiona entrada/salida
- utilidades.py: Funciones auxiliares
- main.py: Punto de entrada del programa
"""

from procesador_archivos import ProcesadorArchivos
from utilidades import Utilidades


def main():
    """Función principal del programa"""
    
    # Mostrar encabezado
    Utilidades.mostrar_encabezado()
    
    # Crear archivo de entrada si no existe
    archivo_entrada = 'palabras_entrada.txt'
    if not Utilidades.archivo_existe(archivo_entrada):
        print("Creando archivo de entrada con palabras de ejemplo...")
        Utilidades.crear_archivo_entrada(archivo_entrada)
        print()
    
    # Procesar archivo
    archivo_salida = 'tokens_salida.txt'
    procesador = ProcesadorArchivos()
    
    resultados = procesador.procesar_archivo(archivo_entrada, archivo_salida)
    
    # Mostrar resultados en consola
    if resultados:
        procesador.mostrar_resultados_consola(resultados)
    
    # Mostrar pie
    Utilidades.mostrar_pie()


if __name__ == "__main__":
    main()
