"""
Módulo: Reglas Silábicas
Descripción: Define las reglas y clasificaciones para la separación silábica en español
             Con expresiones regulares compiladas para optimización
"""

import re


class ReglasSilabicas:
    """
    Contiene todas las reglas y definiciones para la clasificación de caracteres
    y la separación silábica en español.
    """
    
    def __init__(self):
        """Inicializa las reglas silábicas con expresiones regulares compiladas"""
        # Definición del alfabeto
        self.vocales_fuertes = set('aeoáéó')
        self.vocales_debiles = set('iuíú')
        self.vocales = self.vocales_fuertes | self.vocales_debiles
        self.vocales_acentuadas = set('áéíóú')
        
        # Grupos especiales de consonantes
        self.digrafos = ['ch', 'll', 'rr']
        self.grupos_consonanticos = [
            'pr', 'pl', 'br', 'bl', 'fr', 'fl',
            'tr', 'dr', 'cr', 'cl', 'gr', 'gl'
        ]
        
        # ==================== EXPRESIONES REGULARES COMPILADAS ====================
        # Se compilan UNA VEZ para mejor rendimiento
        
        # Patrones vocálicos
        self.patron_vocal = re.compile(r'[aeiouáéíóú]', re.IGNORECASE)
        self.patron_vocal_fuerte = re.compile(r'[aeoáéó]', re.IGNORECASE)
        self.patron_vocal_debil = re.compile(r'[iuíú]', re.IGNORECASE)
        self.patron_vocal_acentuada = re.compile(r'[áéíóú]', re.IGNORECASE)
        
        # Patrones consonánticos
        self.patron_digrafo = re.compile(r'(ch|ll|rr)', re.IGNORECASE)
        self.patron_grupo_consonantico = re.compile(
            r'(pr|pl|br|bl|fr|fl|tr|dr|cr|cl|gr|gl)',
            re.IGNORECASE
        )
        
        # Patrones para análisis de diptongos
        self.patron_diptongo = re.compile(
            r'([aeoáéó][iuíú]|[iuíú][aeoáéó]|[iu][iu])',
            re.IGNORECASE
        )
    
    def es_vocal_fuerte(self, char):
        """Determina si un carácter es vocal fuerte (a, e, o) usando regex"""
        return self.patron_vocal_fuerte.match(char) is not None
    
    def es_vocal_debil(self, char):
        """Determina si un carácter es vocal débil (i, u) usando regex"""
        return self.patron_vocal_debil.match(char) is not None
    
    def es_vocal(self, char):
        """Determina si un carácter es vocal usando regex"""
        return self.patron_vocal.match(char) is not None
    
    def tiene_acento(self, char):
        """Determina si una vocal tiene acento ortográfico usando regex"""
        return self.patron_vocal_acentuada.match(char) is not None
    
    def es_digrafo(self, char1, char2):
        """Verifica si dos caracteres forman un dígrafo (ch, ll, rr) usando regex"""
        par = char1 + char2
        return self.patron_digrafo.fullmatch(par) is not None
    
    def es_grupo_consonantico(self, char1, char2):
        """
        Verifica si dos consonantes forman un grupo consonántico irrompible
        (pr, tr, cl, bl, etc.) usando regex
        """
        par = char1 + char2
        return self.patron_grupo_consonantico.fullmatch(par) is not None
    
    def es_diptongo(self, char1, char2):
        """
        Determina si dos vocales consecutivas forman un diptongo.
        
        Reglas:
        - VF + VD (sin acento en VD) → Diptongo
        - VD + VF (sin acento en VD) → Diptongo
        - VD + VD → Diptongo
        - VF + VF → Hiato
        - VD acentuada → Hiato
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
    
    def clasificar_caracteres(self, palabra):
        """
        Preprocesamiento: Clasifica cada carácter como VF, VD o C
        
        Args:
            palabra (str): Palabra a clasificar
            
        Returns:
            list: Lista de tuplas (carácter, clasificación)
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
    
    def detectar_digrafos(self, palabra):
        """
        Detecta todos los dígrafos en una palabra usando regex
        
        Args:
            palabra (str): Palabra a analizar
            
        Returns:
            list: Lista de tuplas (posición, dígrafo)
        """
        digrafos = []
        for match in self.patron_digrafo.finditer(palabra.lower()):
            digrafos.append((match.start(), match.group()))
        return digrafos
    
    def detectar_diptongos(self, palabra):
        """
        Detecta todos los diptongos en una palabra usando regex
        
        Args:
            palabra (str): Palabra a analizar
            
        Returns:
            list: Lista de tuplas (posición, diptongo)
        """
        diptongos = []
        for match in self.patron_diptongo.finditer(palabra.lower()):
            # Verificar que sea realmente un diptongo (no un hiato)
            if self.es_diptongo(match.group()[0], match.group()[1]):
                diptongos.append((match.start(), match.group()))
        return diptongos
    
    def extraer_estructura(self, palabra):
        """
        Extrae la estructura silábica (V=vocal, C=consonante)
        
        Args:
            palabra (str): Palabra a analizar
            
        Returns:
            str: Estructura de la palabra (ej: CVCCVC)
        """
        estructura = ""
        for char in palabra.lower():
            if self.es_vocal(char):
                estructura += "V"
            else:
                estructura += "C"
        return estructura
    
    def detectar_hiatos(self, palabra):
        """
        Detecta todos los hiatos en una palabra usando las reglas silábicas
        
        Un hiato ocurre cuando:
        - VF + VF (dos vocales fuertes consecutivas)
        - VD acentuada + cualquier vocal
        - Cualquier vocal + VD acentuada
        
        Args:
            palabra (str): Palabra a analizar
            
        Returns:
            list: Lista de tuplas (posición, hiato)
        """
        hiatos = []
        palabra_lower = palabra.lower()
        
        # Buscar pares de vocales consecutivas
        for i in range(len(palabra_lower) - 1):
            char1 = palabra_lower[i]
            char2 = palabra_lower[i + 1]
            
            # Verificar si ambos caracteres son vocales
            if self.es_vocal(char1) and self.es_vocal(char2):
                # Es un hiato si NO es un diptongo
                if not self.es_diptongo(char1, char2):
                    hiatos.append((i, char1 + char2))
        
        return hiatos
