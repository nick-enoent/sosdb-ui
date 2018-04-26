#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sosgui.settings")

import django
django.setup()

from sosdb_auth.models import SosdbUser
from heatmap.models import Heatmap, HeatmapLayer

try:
    admin = SosdbUser.objects.get(username = 'admin')
except:
    admin = SosdbUser.objects.create_superuser('admin', 'admin@localhost',
                                               'admin', user_id = 0)

try:
    narate = SosdbUser.objects.get(username = 'narate')
except:
    narate = SosdbUser.objects.create_user('narate', 'narate@localhost',
                                           'narate', user_id=3030,
                                           is_staff=True)

try:
    nobody = SosdbUser.objects.get(username = 'nobody')
except:
    nobody = SosdbUser.objects.create_user('nobody', 'nobody@localhost',
                                           'nobody', user_id=-1)

# an empty heatmap for admin
admin.heatmaps.get_or_create(store = 'store', name = 'map0')

# a few heatmaps for narate
h0, c = narate.heatmaps.get_or_create(store = 'store', name = 'map0')
h0.update({
    'layers': [
        {
            'name': 'layer0',
            'ptn_ids': [ 256, 257 ],
            'hue': 0.0,
        },
        {
            'name': 'layer1',
            'ptn_ids': [ ],
            'hue': 0.2,
        },
    ]
})

h1, c = narate.heatmaps.get_or_create(store = 'store', name = 'map1')
h1.update({
    'layers': [
        {
            'name': 'layer0',
            'ptn_ids': [],
            'hue': 0.0,
        },
    ]
})

# nobody has no map
