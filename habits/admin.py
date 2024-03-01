from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitClientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'owner', 'place', 'time', 'date', 'action', 'is_public', 'enjoyable_habit', 'is_enjoyable_habit',
        'fee', 'duration', 'periodicity')
    list_editable = (
        'owner', 'place', 'time', 'date', 'action', 'is_public', 'enjoyable_habit', 'is_enjoyable_habit',
        'fee', 'duration', 'periodicity')
    ordering = ('id',)
