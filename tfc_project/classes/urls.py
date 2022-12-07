from django.urls import path

from classes.views import ShowClassInStudioView,UserEnrolClass,MyClassHistory,MyClassSchedule,UserDeleteClass,SearchOrFilterByClassNameView,SearchOrFilterByCoachView,SearchOrFilterByDateView,SearchOrFilterByTimeRangeView,UserEnrolAllFutureClasses,DropAllFutureClasses

app_name = 'classes'

urlpatterns = [
    path('<str:studio>/get_classes/', ShowClassInStudioView.as_view()),
    path('enrol_class/<int:class_id>/', UserEnrolClass.as_view()),
    path('enrol_all_future_classes/<int:class_id>/', UserEnrolAllFutureClasses.as_view()),
    path('my_class_history/', MyClassHistory.as_view()),
    path('my_class_schedule/', MyClassSchedule.as_view()),
    path('drop_class/<int:class_id>/', UserDeleteClass.as_view()),
    path('drop_all_future_classes/<int:class_id>/', DropAllFutureClasses.as_view()),
    path('search_or_filter_1/<str:studio>/<str:class>/', SearchOrFilterByClassNameView.as_view()),
    path('search_or_filter_2/<str:studio>/<str:coach>/', SearchOrFilterByCoachView.as_view()),
    path('search_or_filter_3/<str:studio>/<int:year>/<int:month>/<int:day>/',SearchOrFilterByDateView.as_view()),
    path('search_or_filter_4/<str:studio>/<int:hour1>/<int:minute1>/<int:hour2>/<int:minute2>/',SearchOrFilterByTimeRangeView.as_view()),
]
