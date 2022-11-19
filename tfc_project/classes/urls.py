from django.urls import path

from classes.views import ShowClassInStudioView,UserEnrolClass,MyClassHistory,MyClassSchedule,UserDeleteClass,SearchOrFilterByClassNameView,SearchOrFilterByCoachView,SearchOrFilterByDateView,SearchOrFilterByTimeRangeView

app_name = 'classes'

urlpatterns = [
    path('<str:studio>/get_classes/', ShowClassInStudioView.as_view()),
    path('enrol_class/', UserEnrolClass.as_view()),
    path('my_class_history/', MyClassHistory.as_view()),
    path('my_class_schedule/', MyClassSchedule.as_view()),
    path('drop_class/', UserDeleteClass.as_view()),
    path('search_or_filter_1/<str:studio>/<str:class>/', SearchOrFilterByClassNameView.as_view()),
    path('search_or_filter_2/<str:studio>/<str:coach>/', SearchOrFilterByCoachView.as_view()),
    path('search_or_filter_3/<str:studio>/<int:year>/<int:month>/<int:day>/',SearchOrFilterByDateView.as_view()),
    path('search_or_filter_4/<str:studio>/<int:hour1>/<int:minute1>/<int:hour2>/<int:minute2>/',SearchOrFilterByTimeRangeView.as_view()),
]
