from django.urls import path

from classes.views import CreateClassInstancesView,ShowClassInStudioView

app_name = 'classes'

urlpatterns = [
    path('<str:studio>/<str:class>/create_instances/', CreateClassInstancesView.as_view()),
    path('<str:studio>/get_classes/', ShowClassInStudioView.as_view())
]
