import searches
import json
from django.http import HttpResponse


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
        return HttpResponse(json.dumps(searches.topics()),
                            content_type='application/json')


def topics(request):
    """
    return a list of paired topic names and ids
    """
    return wrap_json(request, searches.topics())
