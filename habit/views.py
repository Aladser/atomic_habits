import datetime

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from authen_drf.permissions import IsSuperUserPermission
from habit.models import Location, Action, Reward, Habit, PleasantHabit, UsefulHabit, Periodicity
from habit.paginators import ManualPagination
from habit.serializers import LocationSerializer, ActionSerializer, RewardSerializer, HabitSerializer, \
    PleasantHabitSerializer, UsefulHabitSerializer, PeriodicitySerializer, HabitCreateSerializer, \
    PleasantHabitCreateSerializer, UsefulCreateHabitSerializer
from libs.spec_habit_mixin import SpecHabitMixin


# ---Периодичность---
class PeriodicityListAPIView(generics.ListAPIView):
    serializer_class = PeriodicitySerializer
    queryset = Periodicity.objects.all()
    permission_classes = (IsSuperUserPermission,)


class PeriodicityCreateAPIView(generics.CreateAPIView):
    serializer_class = PeriodicitySerializer
    permission_classes = (IsSuperUserPermission,)


class PeriodicityDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PeriodicitySerializer
    queryset = Periodicity.objects.all()
    permission_classes = (IsSuperUserPermission,)


# ---Место---
class LocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = (IsSuperUserPermission,)


class LocationCreateAPIView(generics.CreateAPIView):
    serializer_class = LocationSerializer
    permission_classes = (IsSuperUserPermission,)


class LocationDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = (IsSuperUserPermission,)


# ---Действие---
class ActionListAPIView(generics.ListAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()
    permission_classes = (IsSuperUserPermission,)


class ActionCreateAPIView(generics.CreateAPIView):
    serializer_class = ActionSerializer
    permission_classes = (IsSuperUserPermission,)


class ActionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()
    permission_classes = (IsSuperUserPermission,)


# ---Вознаграждение---
class RewardListAPIView(generics.ListAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()
    permission_classes = (IsSuperUserPermission,)


class RewardCreateAPIView(generics.CreateAPIView):
    serializer_class = RewardSerializer
    permission_classes = (IsSuperUserPermission,)


class RewardDestroyAPIView(generics.DestroyAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()
    permission_classes = (IsSuperUserPermission,)


# --- Публичные привычки ---
class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_publiс=True)
    permission_classes = (AllowAny,)


# --- Привычка ---
class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = ManualPagination

    def get_serializer_class(self):
        return HabitCreateSerializer if self.action == 'create' else HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.time = datetime.time(habit.time.hour, habit.time.minute)
        habit.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset if self.request.user.is_superuser else queryset.filter(author=self.request.user)


# --- Приятная привычка ---
class PleasantHabitViewSet(ModelViewSet, SpecHabitMixin):
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    pagination_class = ManualPagination

    def get_serializer_class(self):
        return PleasantHabitCreateSerializer if self.action == 'create' else PleasantHabitSerializer


# --- Полезная привычка ---
class UsefulHabitViewSet(ModelViewSet, SpecHabitMixin):
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()
    pagination_class = ManualPagination

    def get_serializer_class(self):
        return UsefulCreateHabitSerializer if self.action == 'create' else UsefulHabitSerializer
