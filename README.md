# Documentación para el alumnado de Stucom, Barcelona del grado superior en ASIX, DAW y DAM.

Este documento solamente tiene fines educativos.

Herramientas: Prometheus + Grafana + Exporter Open‑Meteo

Distribución: WSL2 + Debian + Docker + Docker Compose

Este sistema de monitorización recogerá datos meteorológicos reales usando Open‑Meteo (sin API key) para así:
  - Exponerlos mediante un Exporter personalizado en Python
  - Monitorizar y almacenar métricas con Prometheus
  - Crear dashboards interactivos de nuestrar métricas con Grafana
  - Ejecutar todo con Docker Compose

Con el objetivo final de diseñar un pipeline de monitorización real al estilo profesional, grandes empresas utilizan sistemas similares para visualizar datos meteorológicos u otras métricas.

## Arquitectura del proyecto

                          ┌───────────────────────────────────────┐
                          │             Open-Meteo API            │
                          │  (datos reales sin token: forecast)   │
                          └───────────────────────────────────────┘
                                            ▲
                                            │ HTTPS (cada 5 min)
                                            │
                          ┌───────────────────────────────────────┐
                          │     Exporter personalizado (Python)   │
                          │  - Llama a Open-Meteo                 │
                          │  - Genera métricas Prometheus         │
                          │  - Exposición en :8000/metrics        │
                          └───────────────────────────────────────┘
                                            │
                                            │ HTTP (scraping)
                                            ▼
                   ┌───────────────────────────────────────────────────────────┐
                   │                          Prometheus                       │
                   │  - Consulta /metrics cada 30s                             │
                   │  - Almacena series temporales                             │
                   │  - Etiquetas: day_name, hourly, forecast                  │
                   └───────────────────────────────────────────────────────────┘
                                            │
                                            │ Consulta PromQL
                                            ▼
                   ┌───────────────────────────────────────────────────────────┐
                   │                           Grafana                         │
                   │  - Dashboards interactivos                                │
                   │  - Iconos meteorológicos                                  │
                   │  - Pronóstico 7 días                                      │
                   │  - Datos horarios                                         │
                   └───────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                        ┌────────────────────────────────────────┐
                        │    Usuario / Alumno (Web Browser)      │
                        │  - http://localhost:3000               │
                        └────────────────────────────────────────┘

## Componentes del sistema

1️. Open‑Meteo API

Proveedor gratuito de datos meteorológicos
No necesita token
Proporciona datos horarios, actuales y pronósticos

https://open-meteo.com/en/docs/geocoding-api
https://geocoding-api.open-meteo.com/v1/search?name=TU_CUIDAD


2. Exporter Python

Se ejecuta en Docker y llama a Open‑Meteo
Convierte los datos a métricas Prometheus
Disponibles: http://localhost:8000/metrics

3️. Prometheus

Se encarga de scrapear las métricas, las almacena y organiza
Disponibles: http://localhost:9090

4️. Grafana

Interfaz visual mediante dashboards meteorológicos avanzados

Disponible: http://localhost:3000


## Comandos básicos

Habilitar WSL en Windows, guía oficial de Microsoft: https://learn.microsoft.com/es-es/windows/wsl/install

Para ver la versión de WSL: wsl --version

Para ver listado de distribuciones disponibles: wsl.exe --list --online

Para instalar distribuciones: wsl.exe --install [Distro] o también podemos instalarlas desde Microsoft Store

Para listar las distribuciones instaladas: wsl -l -v

La elegida para este proyecto ha sido Debian

Una vez virtualizada nuestra distribución actualizamos sistema y paquetes.

Levantar servicios: docker-compose up -d

Apagar el sistema: docker-compose down

Reconstruir: docker-compose build openmeteo-exporter

Ver los contenedores activos: docker ps

Ver logs del exporter: docker logs -f openmeteo-exporter

## Configuración dashboard Grafana

<img width="1466" height="481" alt="image" src="https://github.com/user-attachments/assets/803d914f-c6ca-4aeb-9f31-0f328f299d4b" />

Primer paso es configurar el acceso, cambiar contrase admin en el localhost:3000

Configurar nuestro data source con Prometheus

Podemos contruir nuestro primer dashboard desde 0 con datasource: Prometheus y métricas o utilizar una plantilla, disponible en formato JSON: https://grafana.com/grafana/dashboards/

## Métricas con WeatherFlow

En construcción
