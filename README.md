# Documentación para el alumnado de Stucom, Barcelona del grado superior en ASIX, DAW y DAM.

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

2. Exporter Python

Se ejecuta en Docker
Llama a Open‑Meteo
Convierte los datos a métricas Prometheus
Exposición en:
http://localhost:8000/metrics

3️. Prometheus

Se encarga de “rascar” (scrapear) las métricas
Las almacena y organiza
Consulta:
http://localhost:9090

4️. Grafana

Interfaz visual
Dashboards meteorológicos avanzados
Iconos meteorológicos
Interacción alumno-profesor
Acceso:
http://localhost:3000

## Comandos básicos

En progreso:

Levantar servicios: docker-compose up -d

Reconstruir: docker-compose build openmeteo-exporter

Open-meteo API: https://geocoding-api.open-meteo.com/v1/search?name=NOMBRE_CIUDAD

Acceder a métricas:
- Exporter: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Métricas con WeatherFlow

En progreso:
