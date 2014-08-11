import searches
import json
from django.http import HttpResponse
from shownotes.models import Note, UrlEntry, TextEntry, Topic


def json_result(result):
    return {'show_number': result.show_number,
            'topic_name': result.topic_name,
            'title': result.text,
            'urls': [url for url in result.url_entries],
            'text': result.text_entry,
            'id': result.note_id}


def wrap_json(request, payload):
    """
    return HttpResponse with data correctly formatted for json or jsonp
    depending on the request
    """
    if 'callback' in request.GET:
        return HttpResponse('{}({})'.format(
            request.GET['callback'],
            json.dumps(payload)), content_type='text/javascript')
    else:
        return HttpResponse(json.dumps(payload),
                            content_type='application/json')


def topics(request):
    """
    return a list of paired topic names and ids
    """
    return wrap_json(
        [{'text': t.name, 'id': t.id} for t in Topic.objects.all()],
        request, payload())


def search(request):
    """
    perform a search and return the matches
    recognised parameters are: topics, results_limit, page, string
    """
    RESULTS_LIMIT = 50
    TOPIC_LIMIT = 10
    topics = []
    if 'topics' in parameters:
        topics = [int(t) for t in parameters['topics'].split() if t.isdigit()]
    topics = topics[:TOPIC_LIMIT]
    limit = RESULTS_LIMIT
    if 'limit' in parameters and parameters['limit'].isdigit():
        limit = min(RESULTS_LIMIT, int(parameters['limit']))
    page = 1
    if 'page' in parameters and parameters['page'].isdigit():
        page = int(parameters['page'])
    string = ''
    if 'string' in parameters:
        string = parameters['string']

    response_dict = {'results': [], 'page': 0, 'page_count': 0,
                     'result_count': 0, 'page_result_count': 0}
    if string == '' and topics == []:
        return response_dict

    results = searches.search(string, topics)
    response_dict['result_count'] = results.count()
    paginator = Paginator(results, limit)
    response_dict['page_count'] = paginator.num_pages
    try:
        paged_results = paginator.page(page)
        response_dict['page'] = page
    except EmptyPage:
        paged_results = []
        response_dict['page'] = 0
    response_dict['results'] = [json_result(x) for x in paged_results]
    response_dict['page_result_count'] = len(paged_results)
    return wrap_json(request, response_dict)


def show(request):
    """
    fetch all shownotes belonging to a specific show number
    """
    payload = []
    if 'number' in request.GET and request.GET['number'].isdigit():
        payload = [json_result(r) for r in
                   searches.topics_in_show(int(request.GET['number']))]
    return wrap_json(request, payload)


def note(request):
    """
    retrieve details of a specific note by id
    """
    if 'id' in request.GET and request.GET['id'].isdigit():
        try:
            note = Note.objects.get(id=int(request.GET['id']))
            urls = UrlEntry.get_by_note(note)
            text_entry = TextEntry.get_by_note(note)[0]
            payload = {'show_number': note.show.id,
                       'topic_name': note.topic.name,
                       'title': note.title,
                       'urls': [url.url for url in urls],
                       'text': text_entry.text,
                       'id': note.id}
        except Exception as e:
            print e
            payload = {}
    return wrap_json(request, payload)
