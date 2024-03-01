from rest_framework.routers import DefaultRouter

from habits import views
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

router = DefaultRouter()
router.register('habits', views.HabitViewSet, basename='habits')

urlpatterns = router.urls
