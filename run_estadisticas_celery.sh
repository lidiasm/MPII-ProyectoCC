# Cambiamos de directorio al de estadísticas
cd src/estadisticas/
# Ejecutamos otro worker de Celery para generar las estadísticas.
pipenv run celery worker -A estadisticas_celery --beat --loglevel=info --autoscale=20,10