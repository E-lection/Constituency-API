# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import Vote
from .api_utils import verify_pin_and_make_ineligible
from .api_key_verification import verify, has_vote_permissions

def index(request):
    return HttpResponse("The Constituency API is online.")

@csrf_exempt
@verify(lambda: has_vote_permissions)
def vote_encrypted(request):
    if request.method == 'POST':
        vote_data = json.loads(request.body)

        if all (k in vote_data for k in ('encrpyted_vote', 'pin_code', 'station_id')):
            encrpyted_vote = vote_data['encrpyted_vote']
            pin_code = vote_data['pin_code']
            station_id = vote_data['station_id']

            if verify_pin_and_make_ineligible(station_id, pin_code):
                if encrpyted_vote:
                    Vote.objects.create(vote=encrpyted_vote)
                    return JsonResponse({'success': True,
                                         'error' : None})

            return JsonResponse({'success': False,
                                 'error' : 'Voter is ineligible'})


        return JsonResponse({'success': False,
                         'error' : 'Missing input data'})


def get_votes(request):
    try:
        votes = Vote.objects.all()
        votes_json = json.loads(serializers.serialize(
            "json", votes))

        return JsonResponse({'success': votes.count() > 0,
                             'votes': votes_json})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False,
                             'votes': []})
