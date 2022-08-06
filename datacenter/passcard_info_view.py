import datetime

from django.utils.timezone import localtime

from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404, get_list_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard,passcode=passcode)
    # Программируем здесь
    def get_duration(visit):
        time = visit.leaved_at
        if visit.leaved_at is None:
            time = localtime()
        return (time - visit.entered_at).seconds

    def format_duration(duration):
        return datetime.timedelta(seconds=duration)

    this_passcard_visits = []
    visits = get_list_or_404(Visit,passcard=passcard)
    for i in visits:
        duration = get_duration(i)
        formatted_duration = format_duration(duration)
        is_strange = False
        if duration > 3600:
            is_strange = True
        this_passcard_visits.append({
            'entered_at': i.entered_at,
            'duration': formatted_duration,
            'is_strange': is_strange
        })
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
