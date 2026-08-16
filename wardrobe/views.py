from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .models import ClothingItem
from .forms import ClothingItemForm

from ai.detector import analyze_image
from django.db.models import Count





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

    search = request.GET.get("search")
    category = request.GET.get("category")
    color = request.GET.get("color")
    season = request.GET.get("season")
    occasion = request.GET.get("occasion")

    if search:
        items = items.filter(
            name__icontains=search
        )

    # Robust category mapping for both singular (DB format) and plural (Dashboard links)
    if category and category != "All":
        cat_lower = category.lower()
        
        if cat_lower in ["top", "tops", "shirt", "t-shirt", "hoodie", "jacket"]:
            top_categories = ["Top", "Shirt", "T-shirt", "Hoodie", "Jacket"]
            items = items.filter(category__in=top_categories)
        elif cat_lower in ["bottom", "bottoms"]:
            items = items.filter(category__iexact="Bottom")
        elif cat_lower in ["dress", "dresses"]:
            items = items.filter(category__iexact="Dress")
        elif cat_lower in ["shoe", "shoes"]:
            items = items.filter(category__iexact="Shoes")
        elif cat_lower in ["bag", "bags"]:
            items = items.filter(category__iexact="Bag")
        elif cat_lower in ["accessory", "accessories"]:
            items = items.filter(category__iexact="Accessory")
        else:
            items = items.filter(category__iexact=category)

    if color and color != "All":
        items = items.filter(
            color__iexact=color
        )



    if season and season != "All":

        items = items.filter(
            season=season
        )



    if occasion and occasion != "All":

        items = items.filter(
            occasion=occasion
        )



    return render(

        request,

        "wardrobe.html",

        {
            "items": items,
            "selected_category": category,
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

            style=request.POST.get(
                 "style",
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

        item.style = request.POST.get(
            "style",
            item.style or "Casual"
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

@login_required
def dashboard(request):
    # 1. Fetch all items for the current logged-in user
    items = ClothingItem.objects.filter(user=request.user)
    total_items = items.count()

    # 2. Wardrobe Distribution Logic
    # Grouping shirt-types under "Tops" based on your CATEGORY_CHOICES
    top_categories = ["Top", "Shirt", "T-shirt", "Hoodie", "Jacket"]
    
    count_tops = items.filter(category__in=top_categories).count()
    count_bottoms = items.filter(category="Bottom").count()
    count_shoes = items.filter(category="Shoes").count()
    count_accessories = items.filter(category="Accessory").count()
    count_dresses = items.filter(category="Dress").count()
    count_bags = items.filter(category="Bag").count()

    # Helper function to calculate CSS percentages safely
    def calc_pct(count):
        return int((count / total_items) * 100) if total_items > 0 else 0

    # 3. Dynamic Wardrobe Insights Logic
    insights = []
    if total_items > 0:
        # Insight 1: Most common color
        top_color = items.values('color').annotate(color_count=Count('color')).order_by('-color_count').first()
        if top_color and top_color['color'] != "Unknown":
            insights.append(f"Your wardrobe predominantly features {top_color['color'].lower()} outfits.")
        
        # Insight 2: Season check
        summer_count = items.filter(season="Summer").count()
        summer_pct = calc_pct(summer_count)
        if summer_pct > 0:
            insights.append(f"Summer clothing makes up {summer_pct}% of your total collection.")
        
        # Insight 3: Missing items check
        rainy_count = items.filter(season="Rainy").count()
        if rainy_count == 0:
            insights.append("Note: Your digital wardrobe currently has no rainwear logged.")
        
        # Insight 4: Style check
        formal_count = items.filter(style="Formal").count()
        if formal_count > 0:
            insights.append(f"You currently own {formal_count} formal items.")
        else:
            insights.append("Consider adding more accessories or formal wear to expand styling options.")
    else:
        insights.append("Your wardrobe is empty. Start adding items to generate styling insights.")

    # 4. Activity Log Logic (Latest 4 items)
    recent_activity = items.order_by('-created_at')[:4]

    context = {
        'total_items': total_items,
        
        # Categories for the top cards & images
        'latest_top': items.filter(category__in=top_categories).first(),
        'latest_bottom': items.filter(category="Bottom").first(),
        'latest_dress': items.filter(category="Dress").first(),
        'latest_shoes': items.filter(category="Shoes").first(),
        'latest_bag': items.filter(category="Bag").first(),
        'latest_accessory': items.filter(category="Accessory").first(),
        
        'count_tops': count_tops,
        'count_bottoms': count_bottoms,
        'count_dresses': count_dresses,
        'count_shoes': count_shoes,
        'count_bags': count_bags,
        'count_accessories': count_accessories,

        # Distribution Percentages for the progress bars
        'dist_tops': calc_pct(count_tops),
        'dist_bottoms': calc_pct(count_bottoms),
        'dist_dresses': calc_pct(count_dresses),
        'dist_shoes': calc_pct(count_shoes),
        'dist_bags': calc_pct(count_bags),
        'dist_accessories': calc_pct(count_accessories),

        # Insights & Activity Lists
        'insights': insights,
        'recent_activity': recent_activity,
    }

    return render(request, "home.html", context)