import requests
from datetime import datetime
import random
from django.shortcuts import render ,HttpResponse
from .models import LaunchCountry, Satellite
import csv

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_country(request):
    emps=LaunchCountry.objects.all()
    context={
        'emps':emps
    }
    print(context)
    return render(request, 'allcountry.html',context)



# satellites/utils.py


def download_satellites_csv(request):
    # Query all satellites
    satellites = Satellite.objects.all()

    # Define CSV filename
    filename = "satellites.csv"

    # Set response content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create CSV writer
    writer = csv.writer(response)

    # Write header row
    writer.writerow(['Object Name', 'Object ID', 'Epoch', 'Mean Motion', 'Eccentricity', 
                     'Inclination', 'RA of Ascending Node', 'Argument of Pericenter', 
                     'Mean Anomaly', 'Ephemeris Type', 'Classification Type', 'NORAD Catalog ID',
                     'Element Set Number', 'Revolution at Epoch', 'BStar', 'Mean Motion Dot', 
                     'Mean Motion DDot'])

    # Write satellite data rows
    for satellite in satellites:
        writer.writerow([satellite.object_name, satellite.object_id, satellite.epoch, satellite.mean_motion, 
                         satellite.eccentricity, satellite.inclination, satellite.ra_of_asc_node, 
                         satellite.arg_of_pericenter, satellite.mean_anomaly, satellite.ephemeris_type, 
                         satellite.classification_type, satellite.norad_cat_id, satellite.element_set_no, 
                         satellite.rev_at_epoch, satellite.bstar, satellite.mean_motion_dot, 
                         satellite.mean_motion_ddot])

    return response


def fetch_satellite_data(api_url, max_entries):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data[:max_entries]  # Limit data to max_entries
    return None


def populate_satellites():
    try:
        total_entries = 0
        target_entries = random.randint(600, 601)

        # List of API URLs for different types of satellites
        api_urls = [
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=resource&FORMAT=json",
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=intelsat&FORMAT=json",
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=globalstar&FORMAT=json",
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=radar&FORMAT=json",
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=geodetic&FORMAT=json",
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=molniya&FORMAT=json",
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=military&FORMAT=json",
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=goes&FORMAT=json",
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=x-comm&FORMAT=json",
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=nnss&FORMAT=json",

        ]

        for api_url in api_urls:
            if total_entries >= target_entries:
                break  # Stop if target entries reached
            max_entries_per_api = (target_entries - total_entries) // (len(api_urls) - api_urls.index(api_url))
            data = fetch_satellite_data(api_url, max_entries_per_api)
            if data:
                for satellite_data in data:
                    if total_entries >= target_entries:
                        break  # Stop if target entries reached
                    Satellite.objects.create(
                        object_name=satellite_data.get("OBJECT_NAME", ""),
                        object_id=satellite_data.get("OBJECT_ID", ""),
                        epoch=datetime.strptime(satellite_data.get("EPOCH", ""), "%Y-%m-%dT%H:%M:%S.%f"),
                        mean_motion=satellite_data.get("MEAN_MOTION", ""),
                        eccentricity=satellite_data.get("ECCENTRICITY", ""),
                        inclination=satellite_data.get("INCLINATION", ""),
                        ra_of_asc_node=satellite_data.get("RA_OF_ASC_NODE", ""),
                        arg_of_pericenter=satellite_data.get("ARG_OF_PERICENTER", ""),
                        mean_anomaly=satellite_data.get("MEAN_ANOMALY", ""),
                        ephemeris_type=satellite_data.get("EPHEMERIS_TYPE", ""),
                        classification_type=satellite_data.get("CLASSIFICATION_TYPE", ""),
                        norad_cat_id=satellite_data.get("NORAD_CAT_ID", ""),
                        element_set_no=satellite_data.get("ELEMENT_SET_NO", ""),
                        rev_at_epoch=satellite_data.get("REV_AT_EPOCH", ""),
                        bstar=satellite_data.get("BSTAR", ""),
                        mean_motion_dot=satellite_data.get("MEAN_MOTION_DOT", ""),
                        mean_motion_ddot=satellite_data.get("MEAN_MOTION_DDOT", ""),
                    )
                    total_entries += 1

    except Exception as e:
        print(f"Error populating satellites: {e}")



# View to render all satellites
def all_sat(request):
    try:
        Satellite.objects.all().delete()
        if Satellite.objects.count() < 50:  
            populate_satellites()

        satellites = Satellite.objects.all()
        context = {
            'satellites': satellites
        } 

        return render(request, 'allsat.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {e}")



def remove_country(request):
    emps = LaunchCountry.objects.all()
    context = {
        'emps': emps
    }
    
    if request.method == 'POST':
        country_name = request.POST.get('country_name')
        if country_name:
            try:
                launch_country = LaunchCountry.objects.get(name=country_name)
                launch_country.delete()
                return HttpResponse("Removed successfully")
            except LaunchCountry.DoesNotExist:
                return HttpResponse("Country does not exist")
        else:
            return HttpResponse("No country selected")
    else:
        return render(request, 'removecountry.html', context)
    

def add_country(request):
    if request.method == 'POST':
        country_name=request.POST['country_name']
        new_country=LaunchCountry(name= country_name)
        new_country.save()
        return HttpResponse('country added succesfully')
    
    elif request.method=='GET':
        return render(request, 'addcountry.html')
    
    else:
        return HttpResponse("invalid req")





