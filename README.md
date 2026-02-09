# Weather Monitoring with Open Meteo, Prometheus and Grafana

Sistema completo de monitorización meteorológica usando:
- Exporter personalizado (Open‑Meteo)
- Prometheus
- Grafana (dashboard avanzado + pronóstico 7 días)
- Docker Compose
- WSL2 + Debian

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
