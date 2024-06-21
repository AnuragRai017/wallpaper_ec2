# images/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Image, Category
from .forms import ImageUploadForm
from PIL import Image as PILImage
import os
from django.conf import settings
from django.http import HttpResponse
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = ImageUploadForm()
    return render(request, 'images/upload_image.html', {'form': form})

def image_list(request):
    category_id = request.GET.get('category')
    query = request.GET.get('q')

    images = Image.objects.all()

    if category_id:
        images = images.filter(categories__id=category_id)

    if query:
        images = images.filter(title__icontains=query)

    categories = Category.objects.all()

    paginator = Paginator(images, 24)  # Show 24 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'images/image_list.html', {'page_obj': page_obj, 'categories': categories})



def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    related_images = Image.objects.filter(categories__in=image.categories.all()).exclude(pk=pk).distinct()[:4]
    resolutions = [
        (1920, 1080),
        (1280, 720),
        (3840, 2160),
        (5120, 2880),
    ]
    return render(request, 'images/image_detail.html', {
        'image': image,
        'related_images': related_images,
        'resolutions': resolutions,
    })

def download_image(request, pk, width, height):
    image = get_object_or_404(Image, pk=pk)
    img_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
    with PILImage.open(img_path) as img:
        img = img.resize((width, height), PILImage.LANCZOS)
        response = HttpResponse(content_type="image/jpeg")
        img.save(response, "JPEG")
        response['Content-Disposition'] = f'attachment; filename="{image.title}_{width}x{height}.jpg"'
        return response
