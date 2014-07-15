nasearch
========

Search engine for shownotes for the [No Agenda Show](http://www.noagendashow.com/). Live at [search.nashownotes.com](search.nashownotes.com).

If you want to fork and work on some modifications or use this as a template for your own search engine, the following instructions might be of use.

Set up for development
----------------------
nasearch is built on Django with Haystack/Whoosh and MySQL. 
To get a development version up and running, you should first install the dependencies on your local machine.

+ python-pip 
+ libmysqlclient-dev 
+ libxslt1-dev 
+ python-dev

On debian/ubuntu based systems, these are all in the package manager and you can install with `sudo apt-get install python-pip libmysqlclient-dev libxslt1-dev python-dev`. You can then use pip with the requirements.txt file. `pip install -r requirements.txt`. It is recommended that you set up a virtualenv to use for development, there are plenty of guides online that can walk you through that process.

Deployment
------------
For convenience I've included the deploy script as well as some info on the setup on the server. nginx is used as reverse proxy and to serve static files. Requests for the search application are forwarded on to a gunicorn instance.
You can install all dependencies on the server with `sudo apt-get install nginx python-pip libmysqlclient-dev libxslt1-dev python-dev mysql-server`
After this you must configure nginx and mysql-server. Sample nginx configuration file is included in the configs folder.
After that, you should set up a virtualenv and install the python dependencies. The server should be ready to go.

To deploy, you must first configure the settings_cleaned.py file to conform to Django standards. Rename it to settings.py and fill in the secret key and database connection info for your server. You should also modify the deploy.sh script in scripts/ to copy to the correct server. The deploy scripts takes care of running the collectstatic command for Django.

Populating the database
-----------
There are several custom Django management commands included to make maintenance/data population easier. 

+ full_update attempts to perform a full update of the database by iterating through old show notes starting from the most recent one posted in the rss feed.
+ rss_update attempts to update only from the shownotes referenced in the rss feed.
+ clean_topics deletes topics that have no corresponding shownotes in the database.
+ archive_update attempts to update from the archive.opml file. This is ok for pulling old shownotes but it's a little bit flaky right now.

Once the database is full of shownotes, the command `python manage.py rebuild_index` should be run to allow Whoosh to build a full text index. Ideally this should be done once as it is quite expensive, and then future updates can be pulled in and added to the text index as needed.

On the server, a cron job runs at approximately the correct time to pull in most recent shownotes. It runs the fetch_updates.sh script.
