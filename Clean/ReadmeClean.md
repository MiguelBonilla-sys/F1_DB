# 📊 Módulo Extract - Extracción y Limpieza de Datos F1

## 🎯 Propósito
Este módulo maneja la **extracción** y **limpieza automática** de datos de Fórmula 1, proporcionando datos limpios y listos para análisis.

---

## 📁 Estructura del Módulo

```
Extract/
├── Formula1Extract.py          # Clase principal de extracción
├── Clean/
│   ├── DataClean.py           # Clase de limpieza de datos
│   └── __init__.py
├── __init__.py
└── README.md                  # Este archivo
```

---

## 🔧 Funcionalidades Implementadas

### 1. **Formula1Extract.py**
**Clase principal que maneja la extracción y limpieza integrada:**

#### **Métodos principales:**
- `queries()` - Carga datos desde CSV
- `clean_data()` - Limpia datos automáticamente
- `response()` - Retorna datos limpios por defecto
- `get_cleaned_data()` - Obtiene todos los datos limpios
- `get_original_data()` - Obtiene datos originales
- `compare_data()` - Compara datos antes/después de limpieza

### 2. **Clean/DataClean.py**
**Clase especializada en limpieza de datos:**

#### **Funcionalidades:**
- ✅ **Detección automática** de valores nulos en cualquier número de atributos
- ✅ **Análisis detallado** de calidad de datos
- ✅ **Múltiples estrategias** de limpieza
- ✅ **Reportes estadísticos** del proceso

#### **Estrategias de limpieza disponibles:**
1. `'remove_rows'` - Elimina filas con valores nulos
2. `'fill_mean'` - Rellena con promedio (numéricas) / moda (categóricas)
3. `'fill_zero'` - Rellena con ceros
4. `'fill_forward'` - Rellena con valor anterior
5. `'remove_columns'` - Elimina columnas con muchos nulos

---

## 🚀 Uso Básico

### **Implementación simple (recomendada):**
```python
from Extract.Formula1Extract import Formula1Extract

# Crear extractor
extractor = Formula1Extract("qualifying_results.csv")

# Cargar y limpiar datos
extractor.queries()
extractor.clean_data(strategy='fill_mean')

# Obtener datos limpios
print(extractor.response())
```

### **Uso avanzado con análisis:**
```python
from Extract.Formula1Extract import Formula1Extract

extractor = Formula1Extract("qualifying_results.csv")
extractor.queries()

# Limpieza con información detallada
extractor.clean_data(strategy='fill_mean', verbose=True)

# Comparar datos originales vs limpios
extractor.compare_data()

# Obtener datasets específicos
original_data = extractor.get_original_data()
cleaned_data = extractor.get_cleaned_data()
```

---

## 📈 Resultados del Dataset F1

### **Análisis inicial:**
- **Total filas:** 8,918
- **Total columnas:** 17
- **Valores nulos encontrados:** 244 en columna `Code` (2.74%)

### **Después de limpieza (`fill_mean`):**
- **Filas conservadas:** 8,918 (100%)
- **Valores nulos restantes:** 0
- **Puntuación de calidad:** 100%

### **Columnas del dataset:**
```
Season, Round, CircuitID, Position, DriverID, Code, 
PermanentNumber, GivenName, FamilyName, DateOfBirth, 
Nationality, ConstructorID, ConstructorName, 
ConstructorNationality, Q1, Q2, Q3
```



## 💡 Decisiones de Diseño

### **¿Por qué `fill_mean`?**
- **Conserva todos los datos** (no elimina filas)
- **Estadísticamente apropiado** para análisis
- **Maneja automáticamente** diferentes tipos de datos

### **¿Por qué integración en Formula1Extract?**
- **Simplicidad de uso** - Una sola clase para todo
- **Flujo natural** - Extracción → Limpieza → Uso
- **Mantenimiento fácil** - Todo en un lugar

### **¿Por qué clase DataClean separada?**
- **Reutilización** - Puede usarse con otros extractors
- **Responsabilidad única** - Solo se encarga de limpiar
- **Extensibilidad** - Fácil agregar nuevas estrategias
