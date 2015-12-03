from django.contrib.gis.db import models
from django.contrib.gis import admin
from django.utils import timezone
from urllib.request import urlopen
from datetime import date, timedelta
import json


import sys



class RegionManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name = name)

class Tag(models.Model):
    #UID 64Bit Unique TID Serial Number
    uniqueTID = models.CharField(max_length=64)
    def __str__(self):
        return str(self.uniqueTID)

    def history(self):
        check_in_set = self.tagchekin_set.all().order_by('date')
        return check_in_set

class Region(models.Model):
    name = models.CharField(max_length=100, default="Unknown", unique=True)
    def __str__(self):
        return self.name

class FieldManager(models.Manager):
    def get_by_natural_key(self, name, date_added):
        return self.get(name = name, date_added = date_added)


class Field(models.Model):
    name = models.CharField(max_length=25)
    date_added = models.DateField(auto_now_add=True) #AKA Delivery Date
    description = models.CharField(max_length=250, blank=True)
    owner = models.CharField(max_length=16, blank=True)
    location = models.PointField() #Latitude & Longitude
    source_region = models.ForeignKey('Region', blank=True, null=True)

    locality = models.CharField(max_length=100, blank=True) # ("locality","political")
    county = models.CharField(max_length=100, blank=True)# (administrative-area_level_2"
    state = models.CharField(max_length=100, blank=True)# (administrative_are_level_1")
    
    #http://stackoverflow.com/questions/20169467/how-to-convert-from-longitude-and-latitude-to-country-or-city
    def __str__(self):
        return self.name + " - " + str(self.date_added.year)

    def save(self, *args, **kwargs):
        if not (self.locality or self.county or self.state):
            self.get_place()
        super(Field,self).save(*args,**kwargs)

    def get_place(self):
        url = "http://maps.googleapis.com/maps/api/geocode/json?"
        url += "latlng=%s,%s" % (self.location.y, self.location.x)
        lat = self.location.x
        long = self.location.y
        v = urlopen(url).read()
        j = json.loads(v.decode())
        components = j['results'][0]['address_components']
        for c in components:
            if "locality" in c['types']:
                self.locality = c['long_name']
            if "administrative_area_level_2" in c['types']:
                self.county = c['long_name']
            if "administrative_area_level_1" in c['types']:
                self.state = c['long_name']

    def pallets(self):
        pallets = self.palletreport_set.all()
        for pallet in pallets:
            if self._pallet_is_present(pallet):
                pass

    #Set the previous field/region that all of the present pallets were at
    #Used to back annotate information that was not collected.
    def set_previous_field(self, region_name):
        pallet_reports = self.palletreport_set.distinct('tag__id')
        for pallet_report in pallet_reports:
            #IF PALLET HAS NO PREVIOUS FIELD, SET IT
            if pallet_report.first_field().id == self.id:
                region, created = Region.objects.get_or_create(name=region_name)
                my_field, created = Field.objects.get_or_create(name=region_name,
                                                    defaults={
                                                        'date_added': self.date_added - timedelta(days=30),
                                                        'location': self.location,
                                                        'locality': 'Backdated Location',
                                                        'source_region': region,
                                                    })
                pr = PalletReport(field=my_field, tag=pallet_report.tag, date=timezone.now() - timedelta(days=30))
                pr.save()

    #Get the previous region this field is associated with
    #
    def previous_region(self):
        pallets = self.palletreport_set.distinct('tag__id')

    class Meta:
        unique_together = (('name', 'date_added'),)

class PalletReport(models.Model):
    field = models.ForeignKey('Field')
    tag = models.ForeignKey('Tag')
    date = models.DateField(default=timezone.now)
    number_alive = models.SmallIntegerField(default=4)

    def __str__(self):
        return "%s, %s, %s, (%s)" % (self.field.name, self.field.locality, self.field.state, self.date)

    def first_report(self):
        return self.tag.palletreport_set.earliest('date')

    def first_field(self):
        return self.first_report().field

class Task(models.Model):
    #Task Name:
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(default=timezone.now)
    def __str__(self):
        return self.name + "-" + str(self.date_added)

class Team(models.Model):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('name',)


class WorkLog(models.Model):
    #TODO: Add a unique_together constraint for Field and Task, and overwrite with the newest one.
    #      This will prevent the analysis from selecting the wrong 'model' if there is a newer 'first' row.
    #
    field = models.ForeignKey('Field')
    task = models.ForeignKey('Task')
    team = models.ForeignKey('Team')
    date_work = models.DateField(default=timezone.now)
    hives_alive = models.IntegerField()

    start_date = None

    def __str__(self):
        return self.field.name + "-" + self.task.name + "-" + self.team.name + "-" + str(self.date_work)

    #Returns the percent alive from the specified start date
    def survival_from_date(self):

        if self.start_date is None:
            start_logs = self.field.worklog_set.all().order_by('date_work')
        else:
            start_logs = self.field.worklog_set.filter(date_work__gte=self.start_date).order_by('date_work')

        # If there is not start_log, either:
        # a. Field has not been set (its a dummy instance)
        #     -FALSE: Field was set when the instance was made... (see the view)
        # b. There were no instances found.
        # -- Don't return empty string.
        if not start_logs:
            return  ""
        else:
            #Find the first instance of a number, if any:
            for log in start_logs:
                try:
                    hives_start = int(log.hives_alive)
                    hives_now = int(self.hives_alive)
                    if hives_start == 0:
                        survival_rate = "{:.0%}".format(0)
                    else:
                        survival_rate = "{:.0%}".format(hives_now/hives_start)

                    break
                except ValueError:
                    survival_rate = ""
                    #survival_rate = "\"" + str(log.hives_alive) + "-" + str(self.hives_alive) +"\""

        return survival_rate

admin.site.register(Team, admin.GeoModelAdmin)
admin.site.register(WorkLog, admin.GeoModelAdmin)
admin.site.register(Task, admin.GeoModelAdmin)
admin.site.register(PalletReport, admin.GeoModelAdmin)
admin.site.register(Region, admin.ModelAdmin)