"""
Módulo: Separador DFA
Descripción: Implementación del Autómata Finito Determinista para separación silábica
             Integrado con expresiones regulares para análisis avanzado
"""

from reglas_silabicas import ReglasSilabicas


class SeparadorDFA:
    """
    Implementa un Autómata Finito Determinista (DFA) para la separación silábica
    en español según las reglas de la Real Academia Española.
    
    Estados del autómata:
    - q0: Estado inicial (esperando carácter)
    - q1: Vocal detectada
    - q2: Consonante detectada
    - q3: Secuencia vocálica (VV)
    - q4: Secuencia consonántica (CC)
    - qf: Fin de sílaba (insertar separador)
    """
    
    def __init__(self):
        """Inicializa el separador DFA"""
        self.reglas = ReglasSilabicas()
    
    def separar_silabas(self, palabra):
        """
        Función principal que implementa el DFA para separar sílabas.
        
        Args:
            palabra (str): Palabra a separar
            
        Returns:
            tuple: (palabra_separada, lista_de_reglas_aplicadas, analisis_con_regex)
        """
        palabra_original = palabra
        palabra = palabra.lower().strip()
        
        if not palabra:
            return "", [], {}
        
        # Análisis previo con expresiones regulares
        analisis = {
            'estructura': self.reglas.extraer_estructura(palabra),
            'digrafos': self.reglas.detectar_digrafos(palabra),
            'diptongos': self.reglas.detectar_diptongos(palabra),
            'hiatos': self.reglas.detectar_hiatos(palabra),
        }
        
        chars = list(palabra)
        n = len(chars)
        posiciones_separacion = []  # Posiciones donde se debe separar
        reglas_aplicadas = set()
        
        i = 0
        while i < n:
            # ========== REGLA 1: HIATO (VF+VF) ==========
            if (i + 1 < n and 
                self.reglas.es_vocal(chars[i]) and 
                self.reglas.es_vocal(chars[i + 1]) and
                not self.reglas.es_diptongo(chars[i], chars[i + 1])):
                # Es hiato: separar después de primera vocal
                posiciones_separacion.append(i + 1)
                reglas_aplicadas.add("Hiato")
                i += 1
                continue
            
            # ========== REGLA 2: V-C-V (consonante entre vocales) ==========
            if (i + 2 < n and
                self.reglas.es_vocal(chars[i]) and
                not self.reglas.es_vocal(chars[i + 1]) and
                self.reglas.es_vocal(chars[i + 2])):
                
                # Verificar si siguiente consonante + la siguiente forman grupo irrompible
                if (i + 3 < n and
                    not self.reglas.es_vocal(chars[i + 2]) and
                    self.reglas.es_grupo_consonantico(chars[i + 1], chars[i + 2])):
                    # Patrón V-GC: separar antes del grupo irrompible
                    posiciones_separacion.append(i + 1)
                    reglas_aplicadas.add("V-GC")
                else:
                    # Patrón V-C-V: separar entre consonante y vocal
                    posiciones_separacion.append(i + 1)
                    reglas_aplicadas.add("V-C-V")
                
                i += 1
                continue
            
            # ========== REGLA 3: V-CC-V (dos consonantes entre vocales) ==========
            if (i + 3 < n and
                self.reglas.es_vocal(chars[i]) and
                not self.reglas.es_vocal(chars[i + 1]) and
                not self.reglas.es_vocal(chars[i + 2]) and
                self.reglas.es_vocal(chars[i + 3])):
                
                # Verificar si es dígrafo
                if self.reglas.es_digrafo(chars[i + 1], chars[i + 2]):
                    # CC es dígrafo: no separar el dígrafo
                    posiciones_separacion.append(i + 1)
                    reglas_aplicadas.add("V-Digrafo-V")
                # Verificar si es grupo consonántico irrompible
                elif self.reglas.es_grupo_consonantico(chars[i + 1], chars[i + 2]):
                    # CC es grupo irrompible: separar antes del grupo
                    posiciones_separacion.append(i + 1)
                    reglas_aplicadas.add("V-GC-V")
                else:
                    # CC normal: separar entre las dos consonantes
                    posiciones_separacion.append(i + 2)
                    reglas_aplicadas.add("VC-CV")
                
                i += 1
                continue
            
            # ========== REGLA 4: V-CCC-V (tres consonantes) ==========
            if (i + 4 < n and
                self.reglas.es_vocal(chars[i]) and
                not self.reglas.es_vocal(chars[i + 1]) and
                not self.reglas.es_vocal(chars[i + 2]) and
                not self.reglas.es_vocal(chars[i + 3]) and
                self.reglas.es_vocal(chars[i + 4])):
                
                # Verificar si las dos últimas forman grupo irrompible
                if self.reglas.es_grupo_consonantico(chars[i + 2], chars[i + 3]):
                    # Separar: VC-C-CCV → VCC-CCV
                    posiciones_separacion.append(i + 2)
                    reglas_aplicadas.add("VCC-GC")
                else:
                    # Separar: VCC-CV
                    posiciones_separacion.append(i + 2)
                    reglas_aplicadas.add("VCC-V")
                
                i += 1
                continue
            
            i += 1
        
        # Construir sílabas basadas en posiciones de separación
        silabas = []
        posiciones_separacion.sort()
        inicio = 0
        
        for pos in posiciones_separacion:
            if pos > inicio:
                silabas.append(''.join(chars[inicio:pos]))
                inicio = pos
        
        # Agregar resto
        if inicio < n:
            silabas.append(''.join(chars[inicio:]))
        
        # Si no hay separaciones, la palabra es una sola sílaba
        if not silabas:
            silabas = [palabra]
        
        reglas_lista = sorted(list(reglas_aplicadas))
        if not reglas_lista:
            reglas_lista = ["Sílaba simple"]
        
        return '-'.join(silabas), reglas_lista, analisis
