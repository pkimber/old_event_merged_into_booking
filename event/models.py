# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import reversion

from base.model_utils import TimeStampedModel


class Event(TimeStampedModel):

    event_date = models.DateField()
    description = models.TextField()
    start_time = models.TimeField(
        help_text="Please enter in 24 hour format e.g. 19:00",
    )
    end_time = models.TimeField(
        blank=True, null=True,
        help_text="Please enter in 24 hour format e.g. 21:00",
    )
    location = models.TextField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('event_date', 'start_time')
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return '{}'.format(self.description)

reversion.register(Event)