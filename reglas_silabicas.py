"""
Módulo: Reglas Silábicas
Descripción: Define las reglas y clasificaciones para la separación silábica en español
"""


class ReglasSilabicas:
    """
    Contiene todas las reglas y definiciones para la clasificación de caracteres
    y la separación silábica en español.
    """
    
    def __init__(self):
        """Inicializa las reglas silábicas"""
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
        Verifica si dos consonantes forman un grupo consonántico irrompible
        (pr, tr, cl, bl, etc.)
        """
        par = (char1 + char2).lower()
        return par in self.grupos_consonanticos
    
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
