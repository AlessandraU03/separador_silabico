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
        Procesa una lista de palabras con análisis completo.
        
        Args:
            palabras (list): Lista de palabras a procesar
            
        Returns:
            list: Lista de diccionarios con resultados (incluye análisis regex)
        """
        resultados = []
        for palabra in palabras:
            separacion, reglas, analisis = self.separador.separar_silabas(palabra)
            
            # Determinar tipo de fenómeno: DIPTONGO, DIGRAFO, HIATO
            digrafos = analisis.get('digrafos', [])
            diptongos = analisis.get('diptongos', [])
            hiatos = analisis.get('hiatos', [])
            
            # Prioridad: DIGRAFO > DIPTONGO > HIATO
            if digrafos:
                tipo_fenomeno = 'DIGRAFO'
            elif diptongos:
                tipo_fenomeno = 'DIPTONGO'
            elif hiatos:
                tipo_fenomeno = 'HIATO'
            else:
                tipo_fenomeno = '---'
            
            resultados.append({
                'original': palabra,
                'separacion': separacion,
                'reglas': ', '.join(reglas),
                'estructura': analisis.get('estructura', ''),
                'tipo_fenomeno': tipo_fenomeno,
                'digrafos': digrafos,
                'diptongos': diptongos,
                'hiatos': hiatos
            })
        return resultados
    
    def _generar_archivo_salida(self, archivo_salida, resultados):
        """
        Genera el archivo de salida con los resultados y análisis completo.
        
        Args:
            archivo_salida (str): Ruta del archivo de salida
            resultados (list): Lista de resultados a guardar
        """
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("=" * 130 + "\n")
                f.write("SEPARACION SILABICA - AUTOMATA FINITO DETERMINISTA CON EXPRESIONES REGULARES\n")
                f.write("Universidad Politecnica de Chiapas - Lenguajes y Automatas\n")
                f.write("=" * 130 + "\n\n")
                
                # Encabezados principales
                f.write(f"{'Palabra Original':<15} {'Separacion':<20} {'Tipo':<15} {'Estructura':<20} {'Digrafos/Diptongos':<20}\n")
                f.write("-" * 130 + "\n")
                
                # Resultados
                for resultado in resultados:
                    digrafos_str = ', '.join([d[1] for d in resultado['digrafos']]) if resultado['digrafos'] else ''
                    diptongos_str = ', '.join([d[1] for d in resultado['diptongos']]) if resultado['diptongos'] else ''
                    hiatos_str = ', '.join([d[1] for d in resultado['hiatos']]) if resultado['hiatos'] else ''
                    
                    # Combinar digrafos, diptongos e hiatos en una sola columna
                    patrones = digrafos_str if digrafos_str else (diptongos_str if diptongos_str else hiatos_str)
                    patrones = patrones if patrones else "---"
                    
                    f.write(f"{resultado['original']:<15} {resultado['separacion']:<20} {resultado['tipo_fenomeno']:<15} {resultado['estructura']:<20} {patrones:<20}\n")
                
                # Seccion de analisis detallado
                f.write("\n" + "=" * 130 + "\n")
                f.write("ANALISIS DETALLADO CON EXPRESIONES REGULARES\n")
                f.write("=" * 130 + "\n\n")
                
                for i, resultado in enumerate(resultados, 1):
                    f.write(f"[{i}] {resultado['original']}\n")
                    f.write(f"    Separacion: {resultado['separacion']}\n")
                    f.write(f"    Estructura V/C: {resultado['estructura']}\n")
                    f.write(f"    Tipo: {resultado['tipo_fenomeno']}\n")
                    f.write(f"    Reglas: {resultado['reglas']}\n")
                    
                    if resultado['digrafos']:
                        f.write(f"    Digrafos: {[d[1] for d in resultado['digrafos']]}\n")
                    if resultado['diptongos']:
                        f.write(f"    Diptongos: {[d[1] for d in resultado['diptongos']]}\n")
                    if resultado['hiatos']:
                        f.write(f"    Hiatos: {[d[1] for d in resultado['hiatos']]}\n")
                    f.write("\n")
                
                f.write("=" * 130 + "\n")
            
            print(f"OK - Resultados guardados en '{archivo_salida}'")
        except Exception as e:
            print(f"Error al generar el archivo de salida: {e}")
    
    def mostrar_resultados_consola(self, resultados):
        """
        Muestra los resultados en la consola con información extendida.
        
        Args:
            resultados (list): Lista de resultados a mostrar
        """
        print("\n" + "=" * 150)
        print("RESULTADOS DE LA SEPARACION SILABICA (con analisis de expresiones regulares)")
        print("=" * 150)
        print(f"{'Palabra':<15} {'Separacion':<20} {'Tipo':<15} {'Estructura':<20} {'Patrones':<20}")
        print("-" * 150)
        
        for resultado in resultados:
            digrafos_str = ', '.join([d[1] for d in resultado['digrafos']]) if resultado['digrafos'] else ''
            diptongos_str = ', '.join([d[1] for d in resultado['diptongos']]) if resultado['diptongos'] else ''
            hiatos_str = ', '.join([d[1] for d in resultado['hiatos']]) if resultado['hiatos'] else ''
            
            # Combinar digrafos, diptongos e hiatos en una sola columna
            patrones = digrafos_str if digrafos_str else (diptongos_str if diptongos_str else hiatos_str)
            patrones = patrones if patrones else "---"
            
            print(f"{resultado['original']:<15} {resultado['separacion']:<20} {resultado['tipo_fenomeno']:<15} {resultado['estructura']:<20} {patrones:<20}")
        
        print("=" * 150)
