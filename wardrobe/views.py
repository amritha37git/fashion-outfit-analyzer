from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ClothingItem
from .forms import ClothingItemForm
from django.core.files.storage import FileSystemStorage


@login_required
def upload_item(request):

    if request.method == 'POST':

        form = ClothingItemForm(request.POST, request.FILES)

        if form.is_valid():

            clothing = form.save(commit=False)
            clothing.user = request.user
            clothing.save()

            return redirect('wardrobe')

    else:

        form = ClothingItemForm()

    return render(request, 'upload.html', {'form': form})


@login_required
def wardrobe(request):

    items = ClothingItem.objects.filter(user=request.user)

    return render(request, 'wardrobe.html', {'items': items})


@login_required
def ai_upload(request):

    if request.method == "POST":

        image = request.FILES.get("image")

        if image:

            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)

            context = {
                "image_url": image_url,

                # Temporary AI results
                "category": "Top",
                "color": "White",
                "season": "Summer",
                "occasion": "Casual",
                "description": "White cotton t-shirt"
            }

            return render(request, "ai_result.html", context)

    return render(request, "ai_upload.html")