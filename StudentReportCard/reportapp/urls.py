from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


urlpatterns = [
    path('', views.get_student, name ="get_student"),
    path('login/', views.login_page, name ="login_page"),
    path('register/', views.register_page, name ="register_page"),
    path('logout/', views.logout_page, name ="logout_page"),
    path('marks-table/<student_id>', views.see_marks, name ="see_marks")
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()