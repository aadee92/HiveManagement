from django.shortcuts import render, get_object_or_404
from .models import Field, WorkLog, Task, Region, Tag, Team, PalletReport
import datetime as dt
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation

#REST API:
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from HiveManagement.serializers import UserSerializer, GroupSerializer#, WorkLogSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# class WorkLogView(generics.ListAPIView):
#     model = WorkLog
#     serializer_class = WorkLogSerializer

# Create your views here.

def index(request, start_date=None, end_date=None):
    #Set the view to specified window, if any.
    #TODO: Add AJAX Updating http://stackoverflow.com/questions/20306981/how-do-i-integrate-ajax-with-django-applications

    if (start_date is None) | (end_date is None):
        fields = Field.objects.all().order_by('date_added').exclude(locality="Backdated Location")
        tasks = Task.objects.all().order_by('date_added')
        work_logs = WorkLog.objects.all()
    else:
        fields = Field.objects.filter(date_added__range=(start_date, end_date)).order_by('date_added').exclude(locality="Backdated Location")
        tasks = Task.objects.filter(date_added__range=(start_date, end_date)).order_by('date_added')
        work_logs = WorkLog.objects.all()

    table_work_log = []
    table_head = []
    for task in tasks:
        table_head.append(task.name)

    for f_idx, field in enumerate(fields):
        table_work_log.append([])
        for t_idx, task in enumerate(tasks):
            try:
                work_log = work_logs.filter(task__id=task.id, field__id=field.id).latest('id')
            except WorkLog.DoesNotExist:
                work_log = WorkLog(field=field, task=task, date_work="", hives_alive="")
            work_log.start_date=start_date
            table_work_log[f_idx].append(work_log)

    return render(request, "hive_management/overview.html",{"table_work_log":table_work_log, "table_head":table_head, "fields":fields})

def field(request, field_id):
    #DONE: List each tag associated with the field (only once)
    #TODO: List previous field (first checkin)
    # |1| Kansas   | SD
    # |-- Brookings
    # |-- Hartfield
    # |2| Sinica   | SD
    # |3| Brookings| SD
    # https://datatables.net/examples/api/row_details.html
    field = get_object_or_404(Field, pk=field_id)

    pallet_reports = field.palletreport_set.distinct('tag__id')
    #TODO: Cannot be checked in at another location more recently...
    #tags = tag_checkins.tag_set.all()
    tags=None
    return render(request, 'hive_management/field.html', {'field': field, 'pallet_reports' : pallet_reports, 'tags': tags})

def analysis_region(request):
    # My New Changes to Analysis
    # Analysis by Region / Manager (As Historic)
    # LET INFORMATION WORK ON THE (WORK_LOG . NUMBER_ALIVE)
    # ->| REGION  | # MANAGED | # ALIVE | # SURVIVAL RATE
    # ->| Region1 |   1254    |   512   |     57%
    # ->| Region2 |   5121    |   121   |     12%
    # ->| Region2 |   2185    |   511   |     98%

    #--|START_OPEN--(Any Field Added)--START_CLOSE|-----|END_OPEN--(Analysis on Any Scan Here)--END_CLOSE|
    #--|05/01/2015---------------------09/01/2015 |-----|TODAY-30 DAYS------------------------------TODAY|
    # Open Period = Previous May 1 - September 1
    # Close Period = Previous Month From Today

    start_open_month = 1
    start_close_month = 12
    close_duration = 60

    today = dt.datetime.now()
    if dt.date(today.year,start_open_month,1) > today.date():
        year = today.year - 1
    else:
        year = today.year

    start_open = request.GET.get('start_close',                 dt.date(year, start_open_month,1).strftime("%Y-%m-%d"))
    start_close = request.GET.get('start_open',                 dt.date(year,start_close_month,1).strftime("%Y-%m-%d"))
    end_open = request.GET.get('end_open',                (today + dt.timedelta(-close_duration)).strftime("%Y-%m-%d"))
    end_close = request.GET.get('end_close',                                                today.strftime("%Y-%m-%d"))

    #GET ALL FIELDS ADDED IN START_PERIOD
    fields = Field.objects.filter(date_added__gte=start_open, date_added__lte=start_close)
    #GET UNIQUE REGIONS ASSOCIATED WITH FIELDS
    region_list = fields.distinct("source_region").values_list("source_region",flat=True)
    regions = Region.objects.filter(id__in=list(region_list))

    # for field in fields:
    #     regions.append(field.source_region)

    # for field in fields:
    #     if regions.__contains__()
    # #GET ALL PALLETS ASSOCIATED WITH FIELDS
    # regions = Region.objects.all()
    # region_table = []
    # for r_idx, region in enumerate(regions):
    #     region_table.append([])
    #     region_table[r_idx].append(region.name)
    #     region_hives_first = 0
    #     region_hives_last = 0
    #
    #     fields = region.field_set.all()
    #     #FOR EACH FIELD OF THAT REGION:
    #     for field in fields:
    #         work_logs = field.worklog_set.all().order_by('date_work')
    #         first_work_log = work_logs.first()
    #         last_work_log = work_logs.last()
    #         if (not last_work_log is None) & (not first_work_log is None):
    #             region_hives_first += first_work_log.hives_alive
    #             region_hives_last  += last_work_log.hives_alive
    #
    #     region_table[r_idx].append(region_hives_first)
    #     region_table[r_idx].append(region_hives_last)
    #     try:
    #         region_table[r_idx].append(region_hives_last/region_hives_first)
    #     except ZeroDivisionError:
    #         region_table[r_idx].append("No Data")

    # return render(request, 'hive_management/analysis.html', {'region_table' : region_table })
    return HttpResponse(regions, content_type='text/plain')

def analysis_previous_field(request):
    # Analysis by previous field
    # ->| FIELD   | # HIVES  |  #ALIVE | # SURVIVAL RATE |
    # ->| Johnson |    58    |    21   |    51%
    #
    # Analysis by previous field County
    # ->| COUNTRY  | # HIVES  |  #ALIVE | # SURVIVAL RATE |
    # ->| Brookings|  5511    | 5121    |
    #
    # Analysis with MAP (previous date, analysis date) :
    # -> Each point is previous field at a certain date (slider?)
    # -> Point color is determined by %alive at (analysis date)
    pass



def add_previous_field(request, field_id, region_name):
    #TODO: List each tag associated with the field (only once)
    #TODO: List previous field (first checkin)
    # |1| Kansas   | SD
    # |-- Brookings
    # |-- Hartfield
    # |2| Sinica   | SD
    # |3| Brookings| SD
    # https://datatables.net/examples/api/row_details.html
    field = get_object_or_404(Field, pk=field_id)
    field.set_previous_field(region_name)
    #TODO: Cannot be checked in at another location more recently...
    #tags = tag_checkins.tag_set.all()
    #tags=None
    return render(request, 'hive_management/field.html', {'field': field})

def pallet(request, pallet_id):
    #TODO: Add History Filter
    pallet = get_object_or_404(Tag, pk=pallet_id)
    pallet_reports = pallet.palletreport_set.all().order_by('date')
    return render(request, 'hive_management/pallet.html', {'pallet_reports': pallet_reports, "pallet":pallet})



def field_index(request):
    # Returns a JQUERY list of all the fields, along with their GPS locations.
    data = serializers.serialize('json', Field.objects.all())
    return HttpResponse(data, content_type='text/plain')

def pallet_index(request):
    # Returns a JQUERY list of each pallet's location history, for a year.
    end_date = dt.date.today()
    start_date = end_date - dt.timedelta(days=365)
    data = serializers.serialize('json', PalletReport.objects.filter(date__range=(start_date, end_date)))
    return HttpResponse(data, content_type='text/plain')
    pass

def team_index(request):
    # Returns a JQUERY list of each ACTIVE team.
    data = serializers.serialize('json', Team.objects.filter(is_active='True'))
    return HttpResponse(data, content_type='text/plain')

def task_index(request):
    # Returns a JQUERY list of each ACTIVE task available.
    data = serializers.serialize('json', Task.objects.filter(is_active='True'))
    return HttpResponse(data, content_type='text/plain')

def region_index(request):
    # Returns a JQUERY list of each region available.
    data = serializers.serialize('json', Region.objects.all())
    return HttpResponse(data, content_type='text/plain')

@csrf_exempt
def upload_json(request):
    # Accepts a JQUERY list of new
    #  - fields,
    #  - worklogs, or
    #  - pallet_reports to add to the Database
    # Returns the number of items submitted for confirmation.

    #TODO: Verify Data Integrity, and only allow whitelisted models to be uploaded
    #TODO: Use TokenAuthentication (Rest Framework?) http://www.django-rest-framework.org/#example
    #http://stackoverflow.com/questions/25128486/csrf-safe-strategy-to-create-an-android-application-with-also-an-website-interfa

    if request.method == 'POST':
        #print ('Raw Data:', request.body)
        for deserialized_object in serializers.deserialize("json", request.body):
            # if object_should_be_saved(deserialized_object):
            #     deserialized_object.save()
           deserialized_object.save()
    else:
        raise SuspiciousOperation('Invalid JSON')
    return HttpResponse(request.body, content_type='text/plain')

