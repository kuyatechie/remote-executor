from django.views.generic import TemplateView
from task.models import Task
from datetime import datetime


class DailyTaskAnalyticsView(TemplateView):
    template_name = 'daily-count.html'

    def get_context_data(self, **kwargs):
        context = super(DailyTaskAnalyticsView, self).get_context_data(**kwargs)
        context['30_day_data'] = self.thirty_day_data()
        return context

    def thirty_day_data(self):
        final_data = []

        today = datetime.now()
        for day in range(1, 30):
            count = Task.objects.filter(created__range=(datetime(today.year, today.month, day, 0, 0, 0),
                                                        datetime(today.year, today.month, day, 23, 59, 59),)).count()
            final_data.append(count)
        return final_data

class DailyFreeDiskAnalyticsView(TemplateView):
    template_name = 'disk-space.html'

    def get_context_data(self, **kwargs):
        context = super(DailyFreeDiskAnalyticsView, self).get_context_data(**kwargs)
        context['day_data'], context['label'] = self.day_to_day_data()

        return context

    def day_to_day_data(self):
        final_data = []
        day_data = []
        today = datetime.now()
        task = Task.objects.filter(created__range=(datetime(today.year, today.month, 1, 0, 0, 0),
                                                        datetime(today.year, today.month, 30, 23, 59, 59),)
                                       ).exclude(diskspace_after=None)
        for item in task:
            final_data.append(item.diskspace_after)
            day_data.append(item.pk)

        return final_data, day_data
