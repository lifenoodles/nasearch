date
source ../bin/activate
python manage.py rss_update
python manage.py clean_topics
python manage.py update_index --age 1
