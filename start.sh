nohup celery -A pgm.celery worker --loglevel=info -f log/celery.logs &
python3 pgm.py
