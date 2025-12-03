"""
Universidad Politécnica de Chiapas
Lenguajes y Autómatas - Cuatrimestre 7
Práctica 3: Separador Silábico Básico (DFA e Implementación)

Autores: [Tu nombre y matrícula]
Fecha: Diciembre 2024
"""

class SeparadorSilabico:
    """
    Implementación de un Autómata Finito Determinista (DFA)
    para la separación silábica en español.
    """
    
    def __init__(self):
        # Definición del alfabeto
        self.vocales_fuertes = set('aeoáéó')
        self.vocales_debiles = set('iuíú')
        self.vocales = self.vocales_fuertes | self.vocales_debiles
        self.vocales_acentuadas = set('áéíóú')
        self.digrafos = ['ch', 'll', 'rr']
        self.grupos_consonanticos = ['pr', 'pl', 'br', 'bl', 'fr', 'fl', 
                                     'tr', 'dr', 'cr', 'cl', 'gr', 'gl']
    
    def es_vocal_fuerte(self, char):
        """Determina si un carácter es vocal fuerte (a, e, o)"""
        return char.lower() in self.vocales_fuertes
    
    def es_vocal_debil(self, char):
        """Determina si un carácter es vocal débil (i, u)"""
        return char.lower() in self.vocales_debiles
    
    def es_vocal(self, char):
        """Determina si un carácter es vocal"""
        return char.lower() in self.vocales
    
    def tiene_acento(self, char):
        """Determina si una vocal tiene acento ortográfico"""
        return char.lower() in self.vocales_acentuadas
    
    def es_digrafo(self, char1, char2):
        """Verifica si dos caracteres forman un dígrafo (ch, ll, rr)"""
        par = (char1 + char2).lower()
        return par in self.digrafos
    
    def es_grupo_consonantico(self, char1, char2):
        """
        Verifica si dos consonantes forman un grupo consonántico 
        irrompible (pr, tr, cl, bl, etc.)
        """
        par = (char1 + char2).lower()
        return par in self.grupos_consonanticos
    
    def clasificar_caracteres(self, palabra):
        """
        Preprocesamiento: Clasifica cada carácter como VF, VD o C
        Retorna una lista de tuplas (carácter, clasificación)
        """
        clasificacion = []
        for char in palabra:
            if self.es_vocal_fuerte(char):
                clasificacion.append((char, 'VF'))
            elif self.es_vocal_debil(char):
                clasificacion.append((char, 'VD'))
            else:
                clasificacion.append((char, 'C'))
        return clasificacion
    
    def es_diptongo(self, char1, char2):
        """
        Determina si dos vocales consecutivas forman un diptongo
        Reglas:
        - VF + VD (sin acento en VD) → Diptongo
        - VD + VF (sin acento en VD) → Diptongo
        - VD + VD → Diptongo
        """
        es_v1_fuerte = self.es_vocal_fuerte(char1)
        es_v2_fuerte = self.es_vocal_fuerte(char2)
        es_v1_debil = self.es_vocal_debil(char1)
        es_v2_debil = self.es_vocal_debil(char2)
        
        # VF + VF → Hiato
        if es_v1_fuerte and es_v2_fuerte:
            return False
        
        # VD acentuada → Hiato
        if es_v1_debil and self.tiene_acento(char1):
            return False
        if es_v2_debil and self.tiene_acento(char2):
            return False
        
        # Resto → Diptongo
        return True
    
    def separar_silabas(self, palabra):
        """
        Función principal que implementa el DFA para separar sílabas.
        
        Estados del autómata:
        - q0: Estado inicial (esperando carácter)
        - q1: Vocal detectada
        - q2: Consonante detectada
        - q3: Secuencia vocálica (VV)
        - q4: Secuencia consonántica (CC)
        - qf: Fin de sílaba (insertar separador)
        
        Retorna: tupla (palabra_separada, lista_de_reglas_aplicadas)
        """
        palabra_original = palabra
        palabra = palabra.lower().strip()
        
        if not palabra:
            return "", []
        
        chars = list(palabra)
        silabas = []
        silaba_actual = ""
        reglas_aplicadas = []
        i = 0
        
        while i < len(chars):
            char_actual = chars[i]
            char_siguiente = chars[i + 1] if i + 1 < len(chars) else None
            char_siguiente2 = chars[i + 2] if i + 2 < len(chars) else None
            char_siguiente3 = chars[i + 3] if i + 3 < len(chars) else None
            
            # Agregar carácter actual a la sílaba
            silaba_actual += char_actual
            separar = False
            regla = ""
            
            # ========== FASE 1: DETECCIÓN DE DÍGRAFOS ==========
            if char_siguiente and self.es_digrafo(char_actual, char_siguiente):
                silaba_actual += char_siguiente
                i += 1
                regla = "Dígrafo"
                reglas_aplicadas.append(regla)
            
            # ========== FASE 2: SECUENCIAS VOCÁLICAS (DIPTONGOS/HIATOS) ==========
            elif self.es_vocal(char_actual) and char_siguiente and self.es_vocal(char_siguiente):
                # Verificar si es diptongo o hiato
                if self.es_diptongo(char_actual, char_siguiente):
                    # DIPTONGO: No separar, agregar siguiente vocal
                    silaba_actual += char_siguiente
                    i += 1
                    regla = "Diptongo"
                    reglas_aplicadas.append(regla)
                else:
                    # HIATO: Separar después de la vocal actual
                    separar = True
                    if self.es_vocal_fuerte(char_actual) and self.es_vocal_fuerte(char_siguiente):
                        regla = "Hiato (VF+VF)"
                    else:
                        regla = "Hiato (VD acentuada)"
                    reglas_aplicadas.append(regla)
            
            # ========== FASE 3: PATRÓN V-C-V ==========
            elif (self.es_vocal(char_actual) and 
                  char_siguiente and not self.es_vocal(char_siguiente) and
                  char_siguiente2 and self.es_vocal(char_siguiente2)):
                
                # Verificar si las siguientes consonantes forman grupo
                if char_siguiente2 and char_siguiente3:
                    if self.es_grupo_consonantico(char_siguiente, char_siguiente2):
                        separar = True
                        regla = "V-C-V (grupo consonántico siguiente)"
                        reglas_aplicadas.append(regla)
                    else:
                        separar = True
                        regla = "V-C-V"
                        reglas_aplicadas.append(regla)
                else:
                    separar = True
                    regla = "V-C-V"
                    reglas_aplicadas.append(regla)
            
            # ========== FASE 4: PATRÓN V-CC-V (DOS CONSONANTES) ==========
            elif (self.es_vocal(char_actual) and 
                  char_siguiente and not self.es_vocal(char_siguiente) and
                  char_siguiente2 and not self.es_vocal(char_siguiente2)):
                
                # Verificar dígrafo
                if self.es_digrafo(char_siguiente, char_siguiente2):
                    separar = True
                    regla = "V-D (dígrafo)"
                    reglas_aplicadas.append(regla)
                # Verificar grupo consonántico irrompible
                elif self.es_grupo_consonantico(char_siguiente, char_siguiente2):
                    separar = True
                    regla = "V-GC (grupo consonántico)"
                    reglas_aplicadas.append(regla)
                # Separar entre las dos consonantes
                else:
                    silaba_actual += char_siguiente
                    i += 1
                    separar = True
                    regla = "V-C-C"
                    reglas_aplicadas.append(regla)
            
            # ========== FASE 5: TRES O MÁS CONSONANTES ==========
            elif (not self.es_vocal(char_actual) and 
                  char_siguiente and not self.es_vocal(char_siguiente) and
                  char_siguiente2 and not self.es_vocal(char_siguiente2)):
                
                # Verificar si las dos últimas forman grupo irrompible
                if char_siguiente3 and self.es_grupo_consonantico(char_siguiente2, char_siguiente3):
                    silaba_actual += char_siguiente
                    i += 1
                    separar = True
                    regla = "V-CC-GC"
                    reglas_aplicadas.append(regla)
                else:
                    silaba_actual += char_siguiente
                    i += 1
                    separar = True
                    regla = "V-CCC"
                    reglas_aplicadas.append(regla)
            
            # Separar sílaba si es necesario
            if separar and silaba_actual:
                silabas.append(silaba_actual)
                silaba_actual = ""
            
            i += 1
        
        # Agregar última sílaba
        if silaba_actual:
            silabas.append(silaba_actual)
        
        # Eliminar reglas duplicadas conservando orden
        reglas_unicas = []
        for regla in reglas_aplicadas:
            if regla not in reglas_unicas:
                reglas_unicas.append(regla)
        
        if not reglas_unicas:
            reglas_unicas = ["V-C-V básica"]
        
        return '-'.join(silabas), reglas_unicas


def procesar_archivo(archivo_entrada, archivo_salida):
    """
    Procesa un archivo de palabras y genera la salida con separación silábica
    """
    separador = SeparadorSilabico()
    
    # Leer palabras del archivo
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            palabras = [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")
        return
    
    # Procesar cada palabra
    resultados = []
    for palabra in palabras:
        separacion, reglas = separador.separar_silabas(palabra)
        resultados.append({
            'original': palabra,
            'separacion': separacion,
            'reglas': ', '.join(reglas)
        })
    
    # Generar archivo de salida
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
    
    # Mostrar resultados en consola
    print("\n" + "=" * 100)
    print("RESULTADOS DE LA SEPARACIÓN SILÁBICA")
    print("=" * 100)
    print(f"{'Palabra Original':<20} {'Separación Silábica':<25} {'Reglas Aplicadas':<50}")
    print("-" * 100)
    for resultado in resultados:
        print(f"{resultado['original']:<20} {resultado['separacion']:<25} {resultado['reglas']:<50}")
    print("=" * 100)
    print(f"\n✓ Resultados guardados en '{archivo_salida}'")


def crear_archivo_entrada():
    """Crea el archivo de entrada con las palabras de ejemplo"""
    palabras = [
        "autonomia",
        "murcielago",
        "teatro",
        "ahorro",
        "computadora",
        "ciencia",
        "cancion"
    ]
    
    with open('palabras_entrada.txt', 'w', encoding='utf-8') as f:
        for palabra in palabras:
            f.write(palabra + '\n')
    
    print("✓ Archivo 'palabras_entrada.txt' creado exitosamente")


def main():
    """Función principal del programa"""
    print("\n" + "=" * 100)
    print("SEPARADOR SILÁBICO BASADO EN AUTÓMATA FINITO DETERMINISTA (DFA)")
    print("Universidad Politécnica de Chiapas - Lenguajes y Autómatas")
    print("=" * 100 + "\n")
    
    # Crear archivo de entrada si no existe
    import os
    if not os.path.exists('palabras_entrada.txt'):
        print("Creando archivo de entrada con palabras de ejemplo...")
        crear_archivo_entrada()
        print()
    
    # Procesar archivo
    archivo_entrada = 'palabras_entrada.txt'
    archivo_salida = 'tokens_salida.txt'
    
    procesar_archivo(archivo_entrada, archivo_salida)
    
    print("\n✓ Proceso completado exitosamente\n")


if __name__ == "__main__":
    main()