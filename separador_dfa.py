"""
Módulo: Separador DFA
Descripción: Implementación del Autómata Finito Determinista para separación silábica
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
            tuple: (palabra_separada, lista_de_reglas_aplicadas)
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
            if char_siguiente and self.reglas.es_digrafo(char_actual, char_siguiente):
                silaba_actual += char_siguiente
                i += 1
                regla = "Dígrafo"
                reglas_aplicadas.append(regla)
            
            # ========== FASE 2: SECUENCIAS VOCÁLICAS (DIPTONGOS/HIATOS) ==========
            elif self.reglas.es_vocal(char_actual) and char_siguiente and self.reglas.es_vocal(char_siguiente):
                # Verificar si es diptongo o hiato
                if self.reglas.es_diptongo(char_actual, char_siguiente):
                    # DIPTONGO: No separar, agregar siguiente vocal
                    silaba_actual += char_siguiente
                    i += 1
                    regla = "Diptongo"
                    reglas_aplicadas.append(regla)
                else:
                    # HIATO: Separar después de la vocal actual
                    separar = True
                    if self.reglas.es_vocal_fuerte(char_actual) and self.reglas.es_vocal_fuerte(char_siguiente):
                        regla = "Hiato (VF+VF)"
                    else:
                        regla = "Hiato (VD acentuada)"
                    reglas_aplicadas.append(regla)
            
            # ========== FASE 3: PATRÓN V-C-V ==========
            elif (self.reglas.es_vocal(char_actual) and 
                  char_siguiente and not self.reglas.es_vocal(char_siguiente) and
                  char_siguiente2 and self.reglas.es_vocal(char_siguiente2)):
                
                # Verificar si las siguientes consonantes forman grupo
                if char_siguiente2 and char_siguiente3:
                    if self.reglas.es_grupo_consonantico(char_siguiente, char_siguiente2):
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
            elif (self.reglas.es_vocal(char_actual) and 
                  char_siguiente and not self.reglas.es_vocal(char_siguiente) and
                  char_siguiente2 and not self.reglas.es_vocal(char_siguiente2)):
                
                # Verificar dígrafo
                if self.reglas.es_digrafo(char_siguiente, char_siguiente2):
                    separar = True
                    regla = "V-D (dígrafo)"
                    reglas_aplicadas.append(regla)
                # Verificar grupo consonántico irrompible
                elif self.reglas.es_grupo_consonantico(char_siguiente, char_siguiente2):
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
            elif (not self.reglas.es_vocal(char_actual) and 
                  char_siguiente and not self.reglas.es_vocal(char_siguiente) and
                  char_siguiente2 and not self.reglas.es_vocal(char_siguiente2)):
                
                # Verificar si las dos últimas forman grupo irrompible
                if char_siguiente3 and self.reglas.es_grupo_consonantico(char_siguiente2, char_siguiente3):
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
        reglas_unicas = self._eliminar_duplicados(reglas_aplicadas)
        
        if not reglas_unicas:
            reglas_unicas = ["V-C-V básica"]
        
        return '-'.join(silabas), reglas_unicas
    
    def _eliminar_duplicados(self, lista):
        """
        Elimina elementos duplicados de una lista preservando el orden
        
        Args:
            lista (list): Lista con posibles duplicados
            
        Returns:
            list: Lista sin duplicados
        """
        resultado = []
        for elemento in lista:
            if elemento not in resultado:
                resultado.append(elemento)
        return resultado
