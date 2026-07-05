from django.shortcuts import render, redirect
from .models import ClothingItem
from django.contrib.auth.decorators import login_required

@login_required
def upload_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        image = request.FILES['image']

        ClothingItem.objects.create(
            user=request.user,
            name=name,
            category=category,
            image=image
        )
        return redirect('wardrobe')

    return render(request, 'upload.html')

def wardrobe(request):
    items = ClothingItem.objects.filter(user=request.user)
    return render(request, 'wardrobe.html', {'items': items})