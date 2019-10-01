nohup celery -A pgm.celery worker --loglevel=info &
python3 pgm.py
