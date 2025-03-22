from django.urls import path
from .views import insert_filed_return


# urls.py
urlpatterns = [
    path('insert-filed-return/', insert_filed_return, name='insert_filed_return'),
]  
