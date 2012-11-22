from django.http import HttpResponse as response
import simplejson as json

def main(request):
	j = json.dumps({'name':'Connect App'})
	return response(j,content_type='application/json')
