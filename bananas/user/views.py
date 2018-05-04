# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from dal import autocomplete

from django.db.models import Q
from django.http import HttpResponse

from bananas.user.models import User


class CounselorAutocomplete(autocomplete.Select2QuerySetView):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponse('Unauthorized', status=401)
        return super(CounselorAutocomplete, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):

        qs = User.objects.filter(is_counselor=True)

        if self.q:
            for term in self.q.split():
                qs = qs.filter(
                    Q(first_name__icontains=term) |
                    Q(last_name__icontains=term) |
                    Q(email__icontains=term)
                )

        return qs
