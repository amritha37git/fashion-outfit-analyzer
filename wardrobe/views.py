from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .models import ClothingItem
from .forms import ClothingItemForm

from ai.detector import analyze_image





@login_required
def upload_item(request):


    if request.method == "POST":


        form = ClothingItemForm(
            request.POST,
            request.FILES
        )



        if form.is_valid():


            clothing = form.save(
                commit=False
            )


            clothing.user = request.user


            clothing.save()



            return redirect(
                "wardrobe"
            )



    else:


        form = ClothingItemForm()



    return render(

        request,

        "upload.html",

        {
            "form":form
        }

    )








@login_required
def wardrobe(request):


    items = ClothingItem.objects.filter(
        user=request.user
    )



    search=request.GET.get(
        "search"
    )


    category=request.GET.get(
        "category"
    )


    color=request.GET.get(
        "color"
    )


    season=request.GET.get(
        "season"
    )


    occasion=request.GET.get(
        "occasion"
    )



    if search:

        items=items.filter(
            name__icontains=search
        )



    if category and category!="All":

        items=items.filter(
            category=category
        )



    if color and color!="All":

        items=items.filter(
            color__iexact=color
        )



    if season and season!="All":

        items=items.filter(
            season=season
        )



    if occasion and occasion!="All":

        items=items.filter(
            occasion=occasion
        )



    return render(

        request,

        "wardrobe.html",

        {
            "items":items
        }

    )








@login_required
def ai_upload(request):


    if request.method=="POST":


        image=request.FILES.get(
            "image"
        )



        if image:


            fs=FileSystemStorage()



            filename=fs.save(

                image.name,

                image

            )



            image_path=fs.path(
                filename
            )



            result=analyze_image(
                image_path
            )



            return render(

                request,

                "ai_result.html",

                {


                    "image":filename,


                    "image_url":
                    fs.url(filename),


                    **result

                }

            )



    return render(

        request,

        "ai_upload.html"

    )









@login_required
def save_ai_item(request):


    if request.method=="POST":



        image_path=request.POST.get(
            "image"
        )



        ClothingItem.objects.create(


            user=request.user,


            name=request.POST.get(
                "name",
                "Unknown Item"
            ),



            category=request.POST.get(
                "category",
                "Top"
            ),



            brand=request.POST.get(
                "brand",
                "Unknown"
            ),



            color=request.POST.get(
                "color",
                "Unknown"
            ),



            season=request.POST.get(
                "season",
                "All Season"
            ),



            occasion=request.POST.get(
                "occasion",
                "Casual"
            ),



            description=request.POST.get(
                "description",
                ""
            ),



            image=image_path

        )



        return redirect(
            "wardrobe"
        )



    return redirect(
        "ai_upload"
    )









@login_required
def edit_item(request,item_id):


    item=ClothingItem.objects.get(

        id=item_id,

        user=request.user

    )



    if request.method=="POST":


        item.name=request.POST.get(
            "name"
        )


        item.category=request.POST.get(
            "category"
        )


        item.brand=request.POST.get(
            "brand"
        )


        item.color=request.POST.get(
            "color"
        )


        item.season=request.POST.get(
            "season"
        )


        item.occasion=request.POST.get(
            "occasion"
        )


        item.description=request.POST.get(
            "description"
        )



        item.save()



        return redirect(
            "wardrobe"
        )



    return render(

        request,

        "edit_item.html",

        {
            "item":item
        }

    )








@login_required
def delete_item(request,item_id):


    item=ClothingItem.objects.get(

        id=item_id,

        user=request.user

    )



    item.delete()



    return redirect(
        "wardrobe"
    )