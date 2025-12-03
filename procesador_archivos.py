"""
Módulo: Procesador de Archivos
Descripción: Maneja la lectura y escritura de archivos de entrada y salida
"""

from separador_dfa import SeparadorDFA


class ProcesadorArchivos:
    """
    Gestiona la lectura de palabras de un archivo de entrada
    y la generación de un archivo de salida con los resultados de la separación silábica.
    """
    
    def __init__(self):
        """Inicializa el procesador de archivos"""
        self.separador = SeparadorDFA()
    
    def procesar_archivo(self, archivo_entrada, archivo_salida):
        """
        Procesa un archivo de palabras y genera la salida con separación silábica.
        
        Args:
            archivo_entrada (str): Ruta del archivo de entrada
            archivo_salida (str): Ruta del archivo de salida
            
        Returns:
            list: Lista de diccionarios con los resultados
        """
        # Leer palabras del archivo
        palabras = self._leer_archivo(archivo_entrada)
        
        if not palabras:
            return []
        
        # Procesar cada palabra
        resultados = self._procesar_palabras(palabras)
        
        # Generar archivo de salida
        self._generar_archivo_salida(archivo_salida, resultados)
        
        return resultados
    
    def _leer_archivo(self, archivo_entrada):
        """
        Lee palabras del archivo de entrada.
        
        Args:
            archivo_entrada (str): Ruta del archivo
            
        Returns:
            list: Lista de palabras
        """
        try:
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                palabras = [linea.strip() for linea in f if linea.strip()]
            return palabras
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{archivo_entrada}'")
            return []
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return []
    
    def _procesar_palabras(self, palabras):
        """
        Procesa una lista de palabras.
        
        Args:
            palabras (list): Lista de palabras a procesar
            
        Returns:
            list: Lista de diccionarios con resultados
        """
        resultados = []
        for palabra in palabras:
            separacion, reglas = self.separador.separar_silabas(palabra)
            resultados.append({
                'original': palabra,
                'separacion': separacion,
                'reglas': ', '.join(reglas)
            })
        return resultados
    
    def _generar_archivo_salida(self, archivo_salida, resultados):
        """
        Genera el archivo de salida con los resultados.
        
        Args:
            archivo_salida (str): Ruta del archivo de salida
            resultados (list): Lista de resultados a guardar
        """
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("=" * 100 + "\n")
                f.write("SEPARACIÓN SILÁBICA - AUTÓMATA FINITO DETERMINISTA\n")
                f.write("Universidad Politécnica de Chiapas - Lenguajes y Autómatas\n")
                f.write("=" * 100 + "\n\n")
                
                # Encabezados
                f.write(f"{'Palabra Original':<20} {'Separación Silábica':<25} {'Reglas Aplicadas':<50}\n")
                f.write("-" * 100 + "\n")
                
                # Resultados
                for resultado in resultados:
                    f.write(f"{resultado['original']:<20} {resultado['separacion']:<25} {resultado['reglas']:<50}\n")
                
                f.write("\n" + "=" * 100 + "\n")
            
            print(f"✓ Resultados guardados en '{archivo_salida}'")
        except Exception as e:
            print(f"Error al generar el archivo de salida: {e}")
    
    def mostrar_resultados_consola(self, resultados):
        """
        Muestra los resultados en la consola.
        
        Args:
            resultados (list): Lista de resultados a mostrar
        """
        print("\n" + "=" * 100)
        print("RESULTADOS DE LA SEPARACIÓN SILÁBICA")
        print("=" * 100)
        print(f"{'Palabra Original':<20} {'Separación Silábica':<25} {'Reglas Aplicadas':<50}")
        print("-" * 100)
        
        for resultado in resultados:
            print(f"{resultado['original']:<20} {resultado['separacion']:<25} {resultado['reglas']:<50}")
        
        print("=" * 100)
