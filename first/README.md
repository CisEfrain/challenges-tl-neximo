# Parte 1

Tenemos una función llamada api_call, esta función representa una API externa, puedes pensarlo como una llamada http a otro servicio o una función de algún SDK, esto implica que la función api_call, DATA y PAGE_SIZE NO pueden ser modificadas.

Ahora nuestros desarrolladores llaman directamente la función api_call, esta función retorna la información en páginas, siempre va a regresar 5 elementos (PAGE_SIZE), la primera página es 0.

Queremos generar un wrapper sobre esta función, este wrapper nos permitirá traer tantos elementos como queramos, este wrapper es la clase ApiConsumer.

La tarea es implementar ApiConsumer, es necesario que sea código válido y funcional

Se puede ejecutar de la siguiente forma

## Como ejecutar

- Python 3.11 recomendado
- El siguiente comando ejecuta el programa

```bash
cd first
python .
```
