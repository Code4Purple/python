Python Version : 3.12.2
Djano Version  : 5.0.3


Windows Install :
py -m pip install Django==5.0.3

within in bash terminal:
    source virtual/Scripts/activate
    deactivate
    pip freeze
    django-admin startproject dento
    cd dento
    python manage.py runserver
    python manage.py migrate

    creation of the website app:
        python manage.py startapp website

Within the settings.py file
    Add the just created website into the INSATLLED_APPS array

Within the urls.py file
    put this for the code within the file :
        
        from django.contrib import admin
        from django.urls import path, include

        urlpatterns = [
            path('admin/', admin.site.urls),
            psath('', include('website.urls')),
        ]

close out of the dento directory and go into the website directory 

Under website folder then make another folder called templates

Make a file home.html 
    and add the Hello world with a title tage to the it and save it to test it on the server database
    also we need to add it to the urls page for it appear on the website.

Within the website folder we need to make the urls.py file 
    Then add this code: 
        from django.urls import path

        from . import views

        urlpatterns = [
            path('', views.home, name='home'),
        ]

Then save then open views.py within the webiste folder
    Then add this to the file: 
        def home(request):
            return render(request, 'home.html', {})

SAVE ALL then run python manage.py runsesrver to test it.

Basic Website example setup -- DONE

----------------------------------------------------------------------------------------------------------------
 
We can eaither build our own website from scratch here --->

Or

We can get a webiste template and edit it to our needs --->

    if you are using templates the templates could have static files and a way to make sure your website can use it we need to add it the function of /dento/settings.py

    IN settings.py
        add this to the top: 
            import os
        
        
        add this to the bottom :
            STATIC_URL = 'static/'

            STATICFILES_DIRS = [
                os.path.join(BASE_DIR, 'static')
            ]

On top level of the folders we need to make a folder name : static
then make a folder for the website static files under : website


then u can copy all the static files into the static/website folder

then at the top of the templetes html file we need to add {% load static %} 
then you need to edit all the static tag towards all the imgs , icons, and anything like with this : 
{% static 'website/' % }

this example we put all the static files to the top level folder of website then all you need to after the / is what file is called example : {% static 'website/image_file' %}