
from django.urls import path,include
from .sso import urls as sso_urls
from .user import urls as user_urls
from .file import urls as file_urls
from .public import urls as public_urls
from .order import urls as order_urls
from .cp import urls as cp_urls
from .filter import urls as filter_urls

urlpatterns = [
    path('sso/', include(sso_urls)),
    path('user/', include(user_urls)),
    path('file/', include(file_urls)),
    path('order/', include(order_urls)),
    path('public/', include(public_urls)),
    path('cp/', include(cp_urls)),
    path('filter/', include(filter_urls)),
]
