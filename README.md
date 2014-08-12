nasearch
========

Search engine for shownotes for the [No Agenda Show](http://www.noagendashow.com/). Live at [search.nashownotes.com](http://search.nashownotes.com).

If you want to fork and work on some modifications or use this as a template for your own search engine, the following instructions might be of use.

API
----------------------
You can use the Web API to fetch a list of existing topics, conduct searches, or pull shownotes by episode.
All of the calls support JSON and JSONP.
In order to receive a JSONP response make sure to include the parameter `callback` in your request.
The following calls are supported:

#### /api/topics

Retrieve a list of the topics and associated ids.
No parameters.
Returns a list of objects describing the topics:

+ name: the name of the topic
+ id: the numeric id of the topic (this is used for search requests)

#### /api/search

Perform a search of shownotes and return the results.
Parameters:

 + string: search string, this or topics must contain an entry or you will get 0 results back.
 + topics: a space delimited list of topic ids. If none are included the search will cover all topics. If one or more ids are included the search will be restricted to those ids. The list of topics is capped at 10, only the first 10 topics will be factored in for the search.
 + limit: limit the response to the first `n` results. Default is 50 which for now is also a hard cap.
 + page: specify page of results you require, default is 1.

 Response fields:

 + result_count: number of results total for your search
 + page_result_count: number of results returned for this page
 + page: page number of results returned
 + page_count: total number of pages in this result set
 + notes: a list of shownote objects
   + show_number: the number of the show this note was posted for
   + topic_name: the string name of the topic this note belongs to
   + title: the title of the note
   + urls: a list of urls included with the note
   + text: the full body of text of the note (warning, there will be unescaped html in these notes, so as to preserve formatting or links)
   + id: the numeric id of this note (can be used to request again)

Example Searches:

 + /api/search?string=example&page=22&limit=5
 + /api/search?topics=2200+2201
 + /api/search?string=mac+and+cheese&callback=foo (JSONP example)

#### /api/show

Fetch all shownotes for the given show number
Parameters:

 + number: show number
 + limit: limit the response to the first `n` results. Default is 50 which for now is also a hard cap.
 + page: specify page of results you require, default is 1.

 Response is as described for the /api/search call.

 #### /api/note

 Retrieve details of a specific note by id
 Parameters:

 + id: the numeric id of the shownote requested

Response fields:
 + show_number: the number of the show this note was posted for
 + topic_name: the string name of the topic this note belongs to
 + title: the title of the note
 + urls: a list of urls included with the note
 + text: the full body of text of the note (warning, there will be unescaped html in these notes, so as to preserve formatting or links)
 + id: the numeric id of this note (can be used to request again)

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
