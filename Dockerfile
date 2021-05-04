FROM python:2

ADD . /home/www/html/home/steve/host/crispr_results/

WORKDIR /home/www/html/home/steve/host/crispr_results/

RUN pip install -r requirements-docker.txt

WORKDIR /home/www/html/home/steve/host/crispr_results/crispr

CMD uwsgi --http :80 --module wsgi --callable app --vacuum --master --processes 5 --die-on-term --logger file:/tmp/crispr_results_uwsgi
