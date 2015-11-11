import django_tables2 as tables
from .models import Field




class FieldTable(tables.Table):


    #name = tables.Column()
    #face = tables.Column()
    class Meta:
        model = Field
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
