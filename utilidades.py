"""
Módulo: Utilidades
Descripción: Funciones auxiliares y utilidades del programa
"""

import os


class Utilidades:
    """
    Contiene funciones auxiliares y utilidades para el programa.
    """
    
    @staticmethod
    def crear_archivo_entrada(archivo='palabras_entrada.txt'):
        """
        Crea el archivo de entrada con palabras de ejemplo.
        
        Args:
            archivo (str): Nombre del archivo a crear
        """
        palabras = [
            "autonomia",
            "murcielago",
            "teatro",
            "ahorro",
            "computadora",
            "ciencia",
            "cancion"
        ]
        
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                for palabra in palabras:
                    f.write(palabra + '\n')
            print(f"✓ Archivo '{archivo}' creado exitosamente")
        except Exception as e:
            print(f"Error al crear el archivo: {e}")
    
    @staticmethod
    def archivo_existe(archivo):
        """
        Verifica si un archivo existe.
        
        Args:
            archivo (str): Ruta del archivo
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return os.path.exists(archivo)
    
    @staticmethod
    def mostrar_encabezado():
        """Muestra el encabezado del programa"""
        print("\n" + "=" * 100)
        print("SEPARADOR SILÁBICO BASADO EN AUTÓMATA FINITO DETERMINISTA (DFA)")
        print("Universidad Politécnica de Chiapas - Lenguajes y Autómatas")
        print("=" * 100 + "\n")
    
    @staticmethod
    def mostrar_pie():
        """Muestra el pie del programa"""
        print("\n✓ Proceso completado exitosamente\n")
