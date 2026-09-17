# Hyper-heuristic Genetic Programming for 1D Bin Packing Problem (BPP)

Este repositorio contiene una implementación en Python de **Programación Genética (Genetic Programming - GP)** orientada a la **generación automática de heurísticas de despacho (hiperheurísticas)** para resolver el problema de optimización combinatoria **1D Bin Packing Problem (BPP)**.

El sistema evoluciona árboles sintácticos que representan reglas matemáticas de prioridad. Estas reglas determinan la asignación dinámica de objetos en contenedores para minimizar el número total de contenedores utilizados ($bins\_used$) sobre las instancias de benchmark de **Falkenauer**.

---
##  Autores y Contexto Académico

Proyecto desarrollado en equipo en el marco de la asignatura **Planificación y Scheduling** del **Grado en Ciencia e Ingeniería de Datos (Universidad de Oviedo)**.

* **Enrique Manteca Sánchez** — [@enriquemanteca](https://github.com/enriquemanteca)
* **[Jaime González-Eguren Álvarez]** 
El trabajo implementa técnicas avanzadas de computación evolutiva aplicadas a problemas de optimización combinatoria (1D BPP) y generación automática de reglas de despacho heuríst
##  Características Principales

* **Representación de Individuos basada en Árboles (Montículo/Heap):**
  * Representación en array compacto para optimizar accesos y evaluación de expresiones.
  * Conjunto de funciones: Operaciones binarias (`+`, `-`, `*`, `/` protegida) y unarias (`neg`).
  * Conjunto de terminales del dominio del problema:
    * `sap`: Capacidad restante en el contenedor (*space after placement*).
    * `obj_size`: Tamaño del objeto actual.
    * `remaining`: Suma total de tamaños de los objetos aún por empaquetar.
    * `dif_obj_avg`: Desviación del tamaño del objeto respecto a la media de elementos restantes.
    * Constantes numéricas (`0.25`, `0.50`, `0.75`).

* **Algoritmos Evolutivos Implementados:**
  * **GP Estándar (v1):** Selección por torneo, cruce de subárboles con comprobación de validez estructural, mutación y elitismo.
  * **GP Memético / Steady-State modificado (v2):** Cruce incondicional, reemplazo competitivo por torneos entre padres e hijos e integración de **Búsqueda Local (LSA - Local Search Algorithm)** con muestreo estocástico de instancias para acelerar la convergencia.

* **Decodificadores / Constructores de Planificación (*Schedule Builders*):**
  * `v1`: Enfoque *Next-Fit / First-Fit* dinámico evaluando factibilidad por capacidad.
  * `v2`: Priorización global de objetos antes de asignación al contenedor activo.
  * `v3`: Evaluación multiknapsack/multicontenedor sobre todos los contenedores abiertos simultáneamente (*Best-Fit* guiado por la regla evolucionada).

* **Soporte para Ensembles:**
  * Combinación cooperativa de múltiples reglas evolucionadas mediante agregación de puntuaciones de prioridad para mejorar la generalización.

* **Validación Experimental:**
  * Entrenamiento y test sobre datasets estándar de la literatura (**Falkenauer $t$ y $u$**).
  * Exportación de trazas de convergencia generacionales y archivos de resumen con la regla matemática resultante en formato infijo y montículo.

---
