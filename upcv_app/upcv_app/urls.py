from django.conf.urls.static import static

from django.conf import settings
"""
URL configuration for upcv_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from empleados_app import views as empleados_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('empleados/', include('empleados_app.urls')),
    path('diplomas/', include('diplomas_app.urls', namespace='diplomas')),
    # Alias públicos esperados para autenticación.
    path('login/', empleados_views.signin, name='login'),
    path('signin/', empleados_views.signin, name='signin'),
    path('logout/', empleados_views.signout, name='logout'),
    path('', empleados_views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
