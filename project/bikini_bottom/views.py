from django.shortcuts import render
from django.core.serializers import serialize   # untuk membuat API
from .models import Facility   # memanggil model Facility yang tadi dibuat
from django.http import HttpResponse, JsonResponse   # untuk menghasilkan response dari API
import ast

# Create your views here.
def home(request):
      return render(request, 'pages/home.html')

def home_map_api(request):
  data = serialize('geojson', Facility.objects.all()) 
  return HttpResponse(data, content_type ='json') 

def custom_map_api(request):
  features = {
    'type': 'FeatureCollection',
    'crs': {
      'type': 'name',
      'properties': {
        'name': 'EPSG:4326'
      }
    },
    'features': []
  }

  model = Facility.objects.all()
  for item in model:
    feature = {
      'type': 'Feature',
      'geometry': ast.literal_eval(item.location.json),
      'properties': {
        'nama': item.name,
        'tipe': item.types,
        'harga': item.price,
        'satuan_harga': item.price_unit
      }
    }
    features['features'].append(feature)
  return JsonResponse(features, safe=False)

def facility_form_add(request):
  if request.method == 'POST':
    form = FacilityForm(request.POST, request.FILES)
    if form.is_valid():
      data = form.save(commit=False)
      data.operator = request.user
      data.save()
      return redirect('home')
    
  else:
    form = FacilityForm()
  
  context = {
    'form': form
  }
  return render(request, 'pages/facility_add.html', context=)