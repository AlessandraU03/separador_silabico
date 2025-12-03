# Separador Silábico Basado en Autómata Finito Determinista (DFA)

## Descripción

Este proyecto implementa un Autómata Finito Determinista (DFA) para la separación silábica en español, siguiendo las reglas de la Real Academia Española. El programa lee un archivo con palabras y genera como salida la separación silábica junto con las reglas aplicadas.

## Universidad
Universidad Politécnica de Chiapas - Lenguajes y Autómatas (Cuatrimestre 7)

## Estructura del Proyecto

El código ha sido organizado en múltiples módulos para mejorar la mantenibilidad y claridad:

### 📁 Archivos

```
Separador_Silabico_Basico/
├── main.py                    # Punto de entrada del programa
├── reglas_silabicas.py        # Definiciones y reglas silábicas
├── separador_dfa.py          # Implementación del DFA
├── procesador_archivos.py    # Manejo de entrada/salida
├── utilidades.py             # Funciones auxiliares
├── palabras_entrada.txt      # Palabras a procesar
├── tokens_salida.txt         # Resultados de la separación
└── README.md                 # Este archivo
```

### 📄 Descripción de Módulos

#### `main.py`
- **Propósito**: Punto de entrada del programa
- **Responsabilidades**:
  - Coordina la ejecución del programa
  - Maneja el flujo principal
  - Integra los diferentes módulos

#### `reglas_silabicas.py`
- **Propósito**: Define todas las reglas y clasificaciones
- **Clases**: `ReglasSilabicas`
- **Responsabilidades**:
  - Define vocales (fuertes y débiles)
  - Define dígrafos y grupos consonánticos
  - Implementa lógica de clasificación de caracteres
  - Detecta diptongos y hiatos

#### `separador_dfa.py`
- **Propósito**: Implementa el Autómata Finito Determinista
- **Clases**: `SeparadorDFA`
- **Responsabilidades**:
  - Implementa el algoritmo de separación silábica
  - Maneja los diferentes estados del autómata
  - Aplica las reglas de separación
  - Retorna resultados con reglas aplicadas

#### `procesador_archivos.py`
- **Propósito**: Gestiona la entrada y salida de archivos
- **Clases**: `ProcesadorArchivos`
- **Responsabilidades**:
  - Lee palabras del archivo de entrada
  - Procesa palabras usando el DFA
  - Genera archivo de salida formateado
  - Muestra resultados en consola

#### `utilidades.py`
- **Propósito**: Funciones auxiliares y utilitarias
- **Clases**: `Utilidades`
- **Responsabilidades**:
  - Crea archivo de entrada con ejemplos
  - Verifica existencia de archivos
  - Muestra encabezados y mensajes
  - Funciones de soporte general

## Cómo Usar

### 1. Ejecución Básica
```bash
python main.py
```

### 2. Entrada
El programa lee palabras del archivo `palabras_entrada.txt`. Si no existe, se crea automáticamente con ejemplos:
- autonomia
- murcielago
- teatro
- ahorro
- computadora
- ciencia
- cancion

### 3. Salida
Los resultados se guardan en `tokens_salida.txt` con el formato:
```
Palabra Original | Separación Silábica | Reglas Aplicadas
```

## Reglas de Separación Silábica Implementadas

### 1. **Dígrafos** (ch, ll, rr)
- Permanecen unidos en la misma sílaba
- Ejemplo: `mu-rcié-la-go`

### 2. **Diptongos e Hiatos**
- Diptongo: Dos vocales sin acento que se unen en una sílaba
  - Ejemplo: `au-to-no-mia` (au es diptongo)
- Hiato: Dos vocales fuertes que se separan
  - Ejemplo: `te-a-tro`

### 3. **Patrón V-C-V**
- Una vocal seguida de una consonante y otra vocal
- La consonante se une a la siguiente sílaba
- Ejemplo: `co-mpu-ta-do-ra`

### 4. **Patrón V-CC-V**
- Una vocal seguida de dos consonantes y otra vocal
- Se evalúan grupos consonánticos irrompibles (pr, tr, cl, etc.)

### 5. **Grupos Consonánticos Irrompibles**
```
pr, pl, br, bl, fr, fl, tr, dr, cr, cl, gr, gl
```

## Ventajas de la Estructura Modular

✅ **Mantenibilidad**: Cada módulo tiene responsabilidades claras  
✅ **Reutilización**: Los módulos pueden usarse independientemente  
✅ **Legibilidad**: Código más fácil de entender  
✅ **Testabilidad**: Facilita escribir pruebas unitarias  
✅ **Escalabilidad**: Fácil agregar nuevas funcionalidades  

## Ejemplo de Uso Avanzado

```python
from separador_dfa import SeparadorDFA

# Crear instancia del separador
separador = SeparadorDFA()

# Procesar una palabra
palabra = "murcielago"
resultado, reglas = separador.separar_silabas(palabra)

print(f"Palabra: {palabra}")
print(f"Separación: {resultado}")
print(f"Reglas: {', '.join(reglas)}")
```

## Requisitos

- Python 3.6 o superior
- Codificación UTF-8 en los archivos

## Notas Técnicas

- El programa es case-insensitive (funciona con mayúsculas y minúsculas)
- Maneja acentos y caracteres especiales del español
- Implementa un DFA con múltiples estados y transiciones
- Utiliza búsqueda anticipada (lookahead) para tomar decisiones

## Autor

[Tu nombre y matrícula]

## Fecha

Diciembre 2024
