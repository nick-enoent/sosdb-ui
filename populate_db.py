#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sosgui.settings")

import django
django.setup()

P = os.getenv('PYTHONSTARTUP')
if P:
    execfile(P)

from sosdb_auth.models import SosdbUser
from django.contrib.auth.models import Group
from heatmap.models import Heatmap, HeatmapLayer, HeatmapTag

try:
    admin = SosdbUser.objects.get(username = 'admin')
except:
    admin = SosdbUser.objects.create_superuser('admin', 'admin@localhost',
                                               'admin', user_id = 0)

grp, c = Group.objects.get_or_create(name = 'admin')
grp.user_set.add(admin)

try:
    narate = SosdbUser.objects.get(username = 'narate')
except:
    narate = SosdbUser.objects.create_user('narate', 'narate@localhost',
                                           'narate', user_id=3030,
                                           is_staff=True)

grp, c = Group.objects.get_or_create(name = 'staff')
grp.user_set.add(admin)
grp.user_set.add(narate)

try:
    nobody = SosdbUser.objects.get(username = 'nobody')
except:
    nobody = SosdbUser.objects.create_user('nobody', 'nobody@localhost',
                                           'nobody', user_id=-1)

# Some tags
empty_tag, c = HeatmapTag.objects.get_or_create(
                    username = '$',
                    permission = 0664,
                    tag = 'empty'
               )

metric_tag, c = HeatmapTag.objects.get_or_create(
                    username = '$',
                    permission = 0664,
                    tag = 'metric'
                )

# an empty heatmap for admin
h, c = Heatmap.objects.get_or_create(store = 'store',
                                     username = 'admin',
                                     heatmapname = 'map0')

h.tags.add(empty_tag)

# a few pre-defined heatmaps
h, c = Heatmap.objects.get_or_create(store = 'store',
                                     username = '$',
                                     heatmapname = 'map0',
                                     permission = 0664)

h.update({
    'layers': [
        {
            'layername': 'layer0',
            'hue': 1.0/12.0,
            'ptn_ids': [ 258 ],
        },
        {
            'layername': 'layer1',
            'hue': 1.0/12.0,
            'metric_events': [
                {
                    'schemaname': 'schema0',
                    'metricname': 'metric1',
                    'lower': '-Infinity',
                    'upper': 10010,
                },
            ],
        },
    ]
})

h.tags.add(metric_tag)
h.save()

# a few heatmaps for narate
h0, c = Heatmap.objects.get_or_create(store = 'store',
                                      username = 'narate',
                                      heatmapname = 'map0')
h0.update({
    'layers': [
        {
            'layername': 'layer0',
            'hue': 0.0,
            'ptn_ids': [ 256, 257 ],
        },
        {
            'layername': 'layer1',
            'hue': 2.0/12.0,
            'ptn_ids': [ ],
        },
    ]
})

h1, c = Heatmap.objects.get_or_create(store = 'store',
                                      username = 'narate',
                                      heatmapname = 'map1')
h1.update({
    'layers': [
        {
            'layername': 'layer0',
            'hue': 3.0/12.0,
            'metric_events': [
                {
                    'schemaname': 'schema1',
                    'metricname': 'metric2',
                    'lower': '-Infinity',
                    'upper': 10000,
                },
            ],
        },
    ]
})

h1.tags.add(metric_tag)
h1.save()

# nobody has no map
