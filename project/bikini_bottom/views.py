from django.shortcuts import render
from django.core.serializers import serialize   # untuk membuat API
from .models import Facility   # memanggil model Facility yang tadi dibuat
from django.http import HttpResponse   # untuk menghasilkan response dari API

# Create your views here.
def home(request):
      return render(request, 'pages/home.html')

def home_map_api(request):
  data = serialize('geojson', Facility.objects.all()) 
  return HttpResponse(data, content_type ='json') 