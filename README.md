# PRA 1 Tipologia y ciclo de vida de los datos
Dmytro Pravdyvets y Mariona Alberola i Pla

Este repositorio contiene la PRA1 de web-scraping. La practica se ha basade en seleccionar articulos de [Nature Immunology](https://www.nature.com/ni/) ya que los dos somos bioinformaticos y trabajamos en un ambito donde podriamos aprovechar una dataset como este. 

A partir de los articulos, recogemos el titulo, resumen, autores, accesibilidad, fecha, link al titulo entero o abstract y la imagen representativa del estudio. Tambien para poder seleccionar solamente articulos de interes hemos añadido una lista de keywords a partir de la cual añadimos un Boolean si esta el keyword en el abstract del paper o no. Esto nos permitira hacer una limpiaza del dataset mas adelante. 

El inetes de esta dataset es la posibilidad de generar y seleccionar articulso de Nature que nos interesan sin tener que leer miles de abstracts manualmente. Es una buena manera de automatizar y facilitar la vida a los investigadores para que puedan seguir aprendiendo sin tener que perder tiempo en la lectura de cientos de papers.

## Uso 

En el root se encuenrta un _requierements.txt_ donde estan los packages necesarios para que funcione el codigo.

Dentro de _source_ se puede encontrar el *web_scarping.py* que se ejecuta de manera:

```bash
python web_scraping.py
```

Como output tenemos *2020_immuno_articles.csv* que contiene los articulos sacados de todas las paginas disponibles en Nature Immunology 2022. El año es una varaible que seria facil de ajustar, pero para esta pratica nos hemos quedado solo con el año 2022 para simplificar la interpretacion de los resultados.

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)

Usamos la licencia MIT ya que el data viene de un sitio publico y nosotros no tenemos ningun tipo de ownership. Consideramos que el codigo que hemos escrito no es nada groundbreaking para que este bajo una licencia protectora, no obstante si hay algun bug, no somos responsables de las consequencias.
