from django.urls import path

from . import views
from task.charts import DailyTaskAnalyticsView, DailyFreeDiskAnalyticsView

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create),
    path('view/pk:<int:pk>', views.view_pk),
    path('view/uid:<str:uid>', views.view_uid),
    path('view/date:<str:date>', views.view_day_tasks),             #can be today
    path('view/date:<str:date>/count', views.view_day_tasks_count), #can be today
    path('charts/daily', DailyTaskAnalyticsView.as_view()),
    path('charts/disk', DailyFreeDiskAnalyticsView.as_view()),
]