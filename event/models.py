# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils import timezone

import reversion

from base.model_utils import TimeStampedModel


class EventLocation(TimeStampedModel):

    description = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    url_map = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('description',)
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return '{}'.format(self.description)

reversion.register(EventLocation)


class EventStatus(TimeStampedModel):

    description = models.CharField(max_length=200)
    publish = models.BooleanField(default=False)

    class Meta:
        ordering = ('description',)
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return '{}'.format(self.description)

reversion.register(EventStatus)


class EventType(TimeStampedModel):

    description = models.CharField(max_length=200)
    promote = models.BooleanField(default=False)
    routine = models.BooleanField(default=True)
    css_class_name = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ('description',)
        verbose_name = 'Event type'
        verbose_name_plural = 'Event types'

    def __str__(self):
        return '{}'.format(self.description)

reversion.register(EventType)


class EventManager(models.Manager):

    def _eight_months(self):
        today = timezone.now().date()
        return today + relativedelta(months=8)

    def _two_months(self):
        today = timezone.now().date()
        return today + relativedelta(months=2)

    def _published(self):
        return self.model.objects.filter(
            status__publish=True,
        ).exclude(
            deleted=True
        )

    def promoted(self):
        return self._published().filter(
            start_date__gt=self._two_months(),
            start_date__lte=self._eight_months(),
            event_type__promote=True,
        )

    def published(self):
        return self._published().filter(
            start_date__gte=timezone.now().date(),
            start_date__lte=self._two_months(),
        )


class Event(TimeStampedModel):

    event_type = models.ForeignKey(EventType)
    description = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    start_time = models.TimeField(
        blank=True, null=True,
        help_text="Please enter in 24 hour format e.g. 19:00",
    )
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(
        blank=True, null=True,
        help_text="Please enter in 24 hour format e.g. 21:00",
    )
    location = models.ForeignKey(EventLocation)
    notes = models.TextField(blank=True)
    status = models.ForeignKey(EventStatus)
    deleted = models.BooleanField(default=False)
    objects = EventManager()

    class Meta:
        ordering = ('start_date', 'start_time')
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return '{}'.format(self.description)

reversion.register(Event)
