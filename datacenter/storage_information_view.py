import datetime
from django.utils.timezone import localtime

from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    # Программируем здесь
    def get_duration(visit):
        now = localtime()
        return (now - visit.entered_at).seconds

    def format_duration(duration):
        return datetime.timedelta(seconds=duration)


    non_closed_visits = []
    not_leaved = Visit.objects.filter(leaved_at=None)
    for i in not_leaved:
        duration = get_duration(i)
        formatted_duration = format_duration(duration)
        non_closed_visits.append({
            'who_entered': i.passcard.owner_name,
            'entered_at': i.entered_at,
            'duration': formatted_duration
        })

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
