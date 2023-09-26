# Parte 3

## Instrucciones:

Crea un proyecto en Django usando DRF

Serán necesarios 3 endpoints:

1. /api/register
2. /api/login
3. /api/payments

### /api/register

El endpoint debe recibir los siguientes datos:
    - Nombre completo
    - Correo Electrónico
    - Username
    - Contraseña

### /api/login

El endpoint debe requerir
    - correo electrónico o username
    - contraseña

Este endpoint debe regresar un token de autenticación que será usado para el siguiente endpoint

### /api/payments
Este endpoint debe ser **privado**
Este endpoint podrá recibir una lista de pagos de los cuales se calcularán los impuestos a pagar de acuerdo a las siguientes reglas:

#### Reglas
- Ningún pago recibido tiene impuestos, a todos los pagos se les debe calcular el IVA
- El IVA es del 16%
- Si los pagos son en dólares, este incluye además una comisión del 3% sobre el monto original/neto
- Los pagos menores de 500 mxn están exentos de IVA
- 1 USD = 20 MXN


### Ejemplos

```python

payments = [ 
    { 
        "amount": 1160, 
        "currency": "MXN" 
    },
    {
        "amount": 400, 
        "currency": "MXN" 
    } 
]

response = {
    "total_before_taxes": 1560, # 1160 + 400
    "total_taxes": 185.6, # 1160 * 0.16 = 185.6 (400 < 500 no se cobra IVA)
    "commissions": 0, # Ningún pago está en USD
}

```


```python

payments = [ 
    { 
        "amount": 60, 
        "currency": "USD" 
    },
    {
        "amount": 20, 
        "currency": "USD" 
    },
    {
        "amount": 1000,
        "currency": "MXN"
    }
]

response = {
    "total_before_taxes": 2600, # 20 * 60 + 20 * 20 + 1000 = 2600
    "total_taxes": 352, # 1200 * 0.16 + 1000 * 0.16 = 352 (20 * 20 = 400 < 500 no se cobra IVA)
    "commissions": 48, # (20 * 60 + 20 * 20) * 0.03 = 48
}

```

### Puntos extra
- _Dockerizar_ el proyecto (incluyendo la base de datos)
- Implementar un endpoint que permita cambiar la contraseña del usuario
