 py manage.py runserver 
 docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
  celery -A myshop worker -l info
