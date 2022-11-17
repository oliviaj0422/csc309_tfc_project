from django.urls import path

from classes.views import ShowClassInStudioView,UserEnrolClass,MyClassHistory,MyClassSchedule,UserDeleteClass,SearchByClassNameView,SearchByCoachView,SearchByDateView,SearchByTimeRangeView

app_name = 'classes'

urlpatterns = [
    path('<str:studio>/get_classes/', ShowClassInStudioView.as_view()),
    path('enrol_class/', UserEnrolClass.as_view()),
    path('my_class_history/', MyClassHistory.as_view()),
    path('my_class_schedule/', MyClassSchedule.as_view()),
    path('drop_class/', UserDeleteClass.as_view()),
    path('search1/<str:studio>/<str:class>/', SearchByClassNameView.as_view()),
    path('search2/<str:studio>/<str:coach>/', SearchByCoachView.as_view()),
    path('search3/<str:studio>/<int:year>/<int:month>/<int:day>/',SearchByDateView.as_view()),
    path('search4/<str:studio>/<int:hour1>/<int:minute1>/<int:hour2>/<int:minute2>/',SearchByTimeRangeView.as_view()),
]
