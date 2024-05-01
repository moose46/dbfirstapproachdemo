from django.shortcuts import render

from dbfirstapproachapp.models import Categories

# Create your views here.


# https://www.udemy.com/course/masteringdjango/learn/lecture/41669202#questions
def ShowCategories(request):
    categories = Categories.objects.all()

    return render(request, "dbfa/ShowCategories.html", {"Categories": categories})
