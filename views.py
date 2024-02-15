from django.shortcuts import render, redirect
from .models import Human
import os


# Create your views here.


def Home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')
        if image:
            human = Human.objects.create(name=name, email=email, age=age, gender=gender, image=image)
            human.save()
            print('done')
        else:
            human = Human.objects.create(name=name, email=email, age=age, gender=gender)
            human.save()
            print('done')
    return render(request, "Time/index.html")


def all_prof(request):
    human = Human.objects.all()
    return render(request, "base_all_prof.html", locals())


def delete_prof(request, id):
    prof = Human.objects.get(id=id)
    if prof.image:
        if prof.image != 'def.jpg':
            os.remove(prof.image.path)
        prof.delete()
        return redirect("all_prof")
    else:
        prof.delete()
        return redirect("all_prof")


def update(request, id):
    human = Human.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')

        if image:
            # New image provided
            human.name = name
            human.email = email
            human.age = age
            human.gender = gender

            # Remove the existing image if it's not the default 'def.jpg'
            if human.image.name != 'def.jpg':
                os.remove(human.image.path)
            human.image = image
            human.save()
            return redirect("all_prof")
        else:
            # No new image provided
            human.name = name
            human.email = email
            human.age = age
            human.gender = gender
            human.save()
            return redirect("all_prof")

    return render(request, "update.html", locals())
