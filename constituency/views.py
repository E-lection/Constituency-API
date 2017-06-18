# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

# from django.core import serializers

from django.core.serializers.json import Serializer as Builtin_Serializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import Vote
from .api_utils import verify_pin_and_make_ineligible
from .api_key_verification import verify, has_vote_permissions


class VoteSerializer(Builtin_Serializer):
    def get_dump_object(self, obj):
        return self._current


def index(request):
    return HttpResponse("The Constituency API is online.")


@csrf_exempt
@verify(lambda: has_vote_permissions)
def vote_encrypted(request):
    if request.method == 'POST':
        vote_data = json.loads(request.body)

        if all(k in vote_data for k in ('encrypted_vote', 'pin_code', 'station_id')):
            encrpyted_vote = vote_data['encrypted_vote']
            pin_code = vote_data['pin_code']
            station_id = vote_data['station_id']

            if verify_pin_and_make_ineligible(station_id, pin_code):
                if encrpyted_vote:
                    Vote.objects.create(vote=encrpyted_vote)
                    return JsonResponse({'success': True,
                                         'error': None})

            return JsonResponse({'success': False,
                                 'error': 'Voter is ineligible'})

        return JsonResponse({'success': False,
                             'error': 'Missing input data'})

@csrf_exempt
def vote_script(request):
    if request.method == 'POST':
        print 'POST'
        vote_data = json.loads(request.body)
        print vote_data

        if 'encrypted_vote' in vote_data:
            encrypted_vote = vote_data['encrypted_vote']

            vote_object = Vote(vote=encrypted_vote)
            vote_object.save()
            return JsonResponse({'success': True,
                                 'error' : None})

    return JsonResponse({'success': False,
                         'error' : 'Missing input data'})


def get_votes(request):
    try:
        votes = Vote.objects.all()
        serializer = VoteSerializer()
        votes_json = json.loads(serializer.serialize(votes))

        return JsonResponse({'success': votes.count() > 0,
                             'votes': votes_json})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False,
                             'votes': []})
