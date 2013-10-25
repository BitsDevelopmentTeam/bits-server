#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from bitsd.persistence.engine import session_scope
from bitsd.persistence.models import Status

from sqlalchemy import asc


class PresenceForecaster:
    class InvalidResolutionError(Exception):
        def __init__(self):
            self.message = "Resolution must be a submultiple of 60 minutes!"

    def __init__(self, resolution=30, samples_cont=5000):
        if self.resolution_is_invalid(resolution):
            raise self.InvalidResolutionError()

        self.samples_count = samples_cont
        self.ticks_per_hour = 60 / resolution
        self.minutes_per_tick = resolution

    def forecast(self):
        #TODO caching
        return self.calculate_frequencies()

    def calculate_frequencies(self):
        samples = self.get_samples()
        buckets = self.count_presence_per_slot(samples)
        return self.normalize(buckets)

    def count_presence_per_slot(self, samples):
        buckets = self.init_buckets()

        # TODO algorithm here

        return buckets

    def init_buckets(self):
        return [[0] * (24 * self.ticks_per_hour) for i in range(7)]

    def get_samples(self):
        with session_scope() as session:
            samples = session \
                .query(Status.timestamp, Status.value) \
                .filter((Status.value == Status.OPEN) | (Status.value == Status.CLOSED)) \
                .order_by(asc(Status.timestamp)) \
                .limit(self.samples_count)

        offset = self.first_open_offset(samples)
        return samples[offset:]

    def first_open_offset(self, samples):
        offset = 0
        while samples[offset].value != Status.OPEN:
            offset += 1
        return offset

    @staticmethod
    def resolution_is_invalid(resolution):
        return (60 % resolution) != 0

    def calculate_coordinates(self, sample):
        timestamp = sample.timestamp
        weekday = timestamp.weekday()
        timeslot = (self.ticks_per_hour * timestamp.hour) + int(1. * timestamp.minute / self.minutes_per_tick)
        return weekday, timeslot

    def normalize(self, buckets):
        for day in buckets:
            for i, slot in enumerate(day):
                day[i] = 1. * slot / self.samples_count
        return buckets