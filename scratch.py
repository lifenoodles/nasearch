from shownotes.management.loaders import HtmlLoader
import requests

response = requests.get('http://static.curry.com/nashownotes/554/index.html')
loader = HtmlLoader(response.text, 554)
loader.save()
