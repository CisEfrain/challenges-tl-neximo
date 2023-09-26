# Parte 3

Somos una importante empresa inmobiliaria y cada vez tenemos más visitas por mes, así como inventario

Para continuar creciendo y teniendo más visitas hemos desarrollado la funcionalidad de guardar búsquedas

Ahora lo que tenemos que hacer es notificar a nuestros usuarios cuando hay nuevas propiedades que cumplan con su búsqueda

### Nuestras búsquedas permiten guardan los siguientes parámetros:
- Ubicación
    - Estado
    - Ciudad
- Tipo de propiedad (Casa, Departamento, Bodega, etc):
- Precio mínimo
- Precio máximo
- Número de recámaras
- Número de baños
- Tamaño mínimo (m2)
- Tamaño máximo (m2)

#### Formato de las búsquedas
Son cadenas de texto, aquí unos ejemplos:

```
ciudad de méxico/cuauhtémoc
ciudad de méxico/cuauhtémoc/property_type__office,apartment/size__100_200/price__3000000_4000000/bedrooms_2/bathrooms_1
puebla/cholula/property_type__house/price__400000
Chihuahua/Chihuahua/property_type__house,office/size__80
Guerrero/Tulancingo/size__80/price__400000_500000
Baja California Norte/Tijuana/price__400000_500000/size__120/property_type__house,apartment,warehouse
```

### Nuestro Inventario

Guardamos nuestro inventario en formato json, cada propiedad tiene los siguientes campos:
- id: Number
- state: String
- city: String
- property_type: String
- price: Number
- bedrooms: Number
- bathrooms: Number
- size: Number

Ejemplos:

```json
[
  {
    "id": 1,
    "state": "Ciudad de México",
    "city": "Cuauhtémoc",
    "property_type": "APARTMENT",
    "price": 3000000,
    "bedrooms": 2,
    "bathrooms": 1,
    "size": 100
  }, 
  {
    "id": 2,
    "state": "Chihuahua",
    "city": "Chihuahua",
    "property_type": "HOUSE",
    "price": 4000000,
    "bedrooms": 4,
    "bathrooms": 3,
    "size": 2000
  }
]
```

### Restricciones
- Siempre es necesario tener una ubicación y la ubicación **siempre** se compone de estado y ciudad
- La ubicación siempre es el primer parámetro
- Todos los parámetros son opcionales (excepto la ubicación)
- El order de los parámetros puede cambiar (excepto la ubicación)
- En cuanto al **tipo de propiedad**:
    - Puedes tener muchos tipos de propiedades, los siguientes son los valores permitidos:
      - HOUSE
      - APARTMENT
      - WAREHOUSE
      - LAND
      - OFFICE
- En cuanto al **precio**:
  - Puede tener un valor mínimo y un valor máximo, ambos son **inclusivos**
  - Si sólo tuviera un valor, ese valor sería el máximo, ejemplo: price__1000000 -> máximo 1_000_000
  - No es necesario tomar en cuenta monedas, todos son pesos mexicanos
- En cuanto al **tamaño**:
    - Puede tener un valor mínimo y un valor máximo, ambos son **inclusivos**
    - Si sólo tuviera un valor, ese valor sería el mínimo, ejemplo: size__100 -> por lo menos propiedades con de 100 m2 o más

### Objetivos

Tendremos dos entradas
1. Una lista de búsquedas
    - Es un archivo de texto (utf-8) con una búsqueda por línea
2. Una lista de propiedades
   - La lista de propiedades es un archivo json

El objetivo identificar que búsquedas hacen match con las propiedades, ver el siguiente ejemplo:

```python
from services import MatchingService

searches = [
    'ciudad de méxico/cuauhtémoc',
    'ciudad de méxico/cuauhtémoc/property_type__office,apartment/size__100_200/price__3000000_4000000/bedrooms_2/bathrooms_1',
    'puebla/cholula/property_type__house/price__400000',
    'chihuahua/chihuahua/property_type__house,office/size__80/price__2000000',
]

properties = [
    {
        "id": 1,
        "state": "Ciudad de México",
        "city": "Cuauhtémoc",
        "property_type": "APARTMENT",
        "price": 3_000_000,
        "bedrooms": 2,
        "bathrooms": 1,
        "size": 120
    },
    {
        "id": 2,
        "state": "Chihuahua",
        "city": "Chihuahua",
        "property_type": "HOUSE",
        "price": 4_000_000,
        "bedrooms": 4,
        "bathrooms": 3,
        "size": 2_000
    }
]

matched_searches = MatchingService(
    searches=searches,
    properties=properties,
).match()

assert matched_searches == [
    'ciudad de méxico/cuauhtémoc',
    'ciudad de méxico/cuauhtémoc/property_type__office,apartment/size__100_200/price__3000000_4000000/bedrooms_2/bathrooms_1',
]
```

```


Las búsquedas se guardan como una cadena de texto, por ejemplo:

```bash

```python

with_just_state = 'Ciudad de México'
state_and_city = 'Ciudad de México/Cuauhtémoc'
all_parameters = 'Ciudad de México/Cuauhtémoc/property_type__office,APARTMENT/size__100_200/price__3000000_4000000/bedrooms_2/bathrooms_1'

```



```


```bash
cd first
python .
```
