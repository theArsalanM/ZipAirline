import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from calculator.constants import FUEL_TANK_FIXED_CAPACITY, FUEL_CONSUMPTION_MULTIPLIER, LOG_BASE, \
    PER_PASSENGER_PER_MINUTE_FUEL_MULTIPLIER


class Airplane(models.Model):
    """
    Stores single Airplane entry with its airplane_id and passenger_count,
    also relates it with :model: `auth.User` (optionally)
    """
    # Assuming that this ID is different from Primary Key, and might not be unique
    airplane_id = models.PositiveSmallIntegerField(verbose_name=_('Airplane ID'))

    # By default, we'll calculate with no passenger load
    passengers_count = models.PositiveSmallIntegerField(verbose_name=_('Number of passengers'), default=0)

    # Following 2 field I usually add in my model to track data, this often helps in debugging, analytics & backtracking
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                 help_text='User id saved to track if an authenticated user submits request')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Timestamp added to track record creation date')

    def __str__(self):
        return f'Airplane instance {self.airplane_id} with {self.passengers_count} passengers'

    def _fuel_tank_capacity(self):
        """
        Calculates fuel tank capacity of an Airplane, returns fuel in litres
        :return: integer
        """
        return FUEL_TANK_FIXED_CAPACITY * self.airplane_id

    def fuel_consumption_per_minute(self):
        """
        Calculates fuel consumption per minute, returns fuel consumed per minute in litres
        :return: float
        """
        additional_load = self.passengers_count * PER_PASSENGER_PER_MINUTE_FUEL_MULTIPLIER
        return (math.log(self.airplane_id, LOG_BASE) * FUEL_CONSUMPTION_MULTIPLIER) + additional_load

    def total_flight_time_in_minutes(self):
        """
        Calculates total flight time of an airplane after fetching its fuel capacity and per minute
        fuel consumption, returns total flight time in minutes
        :return: float
        """
        return self._fuel_tank_capacity() / self.fuel_consumption_per_minute()
