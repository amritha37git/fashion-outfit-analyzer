from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

from .models import ClothingItem
from .forms import ClothingItemForm
from ai.detector import analyze_image


# ==========================================
# Manual Upload
# ==========================================

@login_required
def upload_item(request):

    if request.method == "POST":

        form = ClothingItemForm(request.POST, request.FILES)

        if form.is_valid():

            clothing = form.save(commit=False)
            clothing.user = request.user
            clothing.save()

            messages.success(
                request,
                "✅ Clothing item added successfully."
            )

            return redirect("wardrobe")

    else:

        form = ClothingItemForm()

    return render(
        request,
        "upload.html",
        {
            "form": form
        }
    )


# ==========================================
# Wardrobe
# ==========================================

@login_required
def wardrobe(request):

    items = ClothingItem.objects.filter(
        user=request.user
    ).order_by("-created_at")

    search = request.GET.get("search", "")
    category = request.GET.get("category", "")
    color = request.GET.get("color", "")
    season = request.GET.get("season", "")
    occasion = request.GET.get("occasion", "")

    if search:

        items = items.filter(

            Q(name__icontains=search) |
            Q(color__icontains=search) |
            Q(brand__icontains=search)

        )

    if category and category != "All":

        items = items.filter(
            category=category
        )

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

            "search": search,
            "selected_category": category,
            "selected_color": color,
            "selected_season": season,
            "selected_occasion": occasion,

            "total_items": items.count()
        }
    )


# ==========================================
# AI Upload
# ==========================================

@login_required
def ai_upload(request):

    if request.method == "POST":

        image = request.FILES.get("image")

        if not image:

            messages.error(
                request,
                "Please choose an image."
            )

            return redirect("ai_upload")

        fs = FileSystemStorage()

        filename = fs.save(
            image.name,
            image
        )

        image_path = fs.path(filename)

        try:

            result = analyze_image(
                image_path
            )

        except Exception:

            result = {

                "name": "Unknown Item",

                "category": "Top",

                "brand": "Unknown",

                "color": "Unknown",

                "season": "All Season",

                "occasion": "Casual",

                "description":
                "AI analysis is currently unavailable. Please edit the details before saving."

            }

        context = {

            "image": filename,

            "image_url": fs.url(filename),

            **result

        }

        return render(
            request,
            "ai_result.html",
            context
        )

    return render(
        request,
        "ai_upload.html"
    )


# ==========================================
# Save AI Item
# ==========================================

@login_required
def save_ai_item(request):

    if request.method != "POST":

        return redirect("ai_upload")

    ClothingItem.objects.create(

        user=request.user,

        name=request.POST.get("name"),

        category=request.POST.get("category"),

        brand=request.POST.get("brand"),

        color=request.POST.get("color"),

        season=request.POST.get("season"),

        occasion=request.POST.get("occasion"),

        description=request.POST.get("description"),

        image=request.POST.get("image"),

        ai_generated=True,

        ai_confidence=90

    )

    messages.success(
        request,
        "✅ Item saved successfully."
    )

    return redirect("wardrobe")


# ==========================================
# Edit Item
# ==========================================

@login_required
def edit_item(request, item_id):

    item = get_object_or_404(

        ClothingItem,

        id=item_id,

        user=request.user

    )

    if request.method == "POST":

        item.name = request.POST.get("name")
        item.category = request.POST.get("category")
        item.brand = request.POST.get("brand")
        item.color = request.POST.get("color")
        item.season = request.POST.get("season")
        item.occasion = request.POST.get("occasion")
        item.description = request.POST.get("description")

        item.manually_edited = True

        item.save()

        messages.success(
            request,
            "✅ Item updated."
        )

        return redirect("wardrobe")

    return render(

        request,

        "edit_item.html",

        {

            "item": item

        }

    )


# ==========================================
# Delete Item
# ==========================================

@login_required
def delete_item(request, item_id):

    item = get_object_or_404(

        ClothingItem,

        id=item_id,

        user=request.user

    )

    item.delete()

    messages.success(

        request,

        "🗑 Item deleted."

    )

    return redirect("wardrobe")