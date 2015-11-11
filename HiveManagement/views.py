from django.shortcuts import render, get_object_or_404
from .models import Field, WorkLog, Task, Region, Tag
import django_tables2 as tables
from .tables import FieldTable
import datetime as dt

# Create your views here.

def index(request, start_date=None, end_date=None):
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

def analysis(request):
    # Analysis by Region / Manager (As Historic)
    # LET INFORMATION WORK ON THE (WORK_LOG . NUMBER_ALIVE)
    # ->| REGION  | # MANAGED | # ALIVE | # SURVIVAL RATE
    # ->| Region1 |   1254    |   512   |     57%
    # ->| Region2 |   5121    |   121   |     12%
    # ->| Region2 |   2185    |   511   |     98%

    #--|START_OPEN---------START_CLOSE|-----|END_OPEN--------END_CLOSE|
    today = dt.datetime.now()
    start_open = request.GET.get('start_close', today.strftime("%m-%d-%Y")+dt.timedelta(-180))
    start_close = request.GET.get('start_open', today + dt.timedelta(-90))
    end_open = request.GET.get('end_open', today + dt.timedelta(-90))
    end_close = request.GET.get('end_close', today.strftime("%m-%d-%Y"))

    #GET ALL FIELDS ADDED IN END_PERIOD

    #GET ALL
    regions = Region.objects.all()
    region_table = []
    for r_idx, region in enumerate(regions):
        region_table.append([])
        region_table[r_idx].append(region.name)
        region_hives_first = 0
        region_hives_last = 0

        fields = region.field_set.all()
        #FOR EACH FIELD OF THAT REGION:
        for field in fields:
            work_logs = field.worklog_set.all().order_by('date_work')
            first_work_log = work_logs.first()
            last_work_log = work_logs.last()
            if (not last_work_log is None) & (not first_work_log is None):
                region_hives_first += first_work_log.hives_alive
                region_hives_last  += last_work_log.hives_alive

        region_table[r_idx].append(region_hives_first)
        region_table[r_idx].append(region_hives_last)
        try:
            region_table[r_idx].append(region_hives_last/region_hives_first)
        except ZeroDivisionError:
            region_table[r_idx].append("No Data")

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


    return render(request, 'hive_management/analysis.html', {'region_table' : region_table })

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