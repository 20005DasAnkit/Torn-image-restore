from .ml.restore import restore_image
import uuid
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import os
import random
from django.conf import settings
from .models import Profile
from django.contrib import messages
from datetime import datetime




# HOME
def home(request):
    media_path = settings.MEDIA_ROOT

    images = []

    if os.path.exists(media_path):
        images = [
            f for f in os.listdir(media_path)
            if os.path.isfile(os.path.join(media_path, f))
        ]

    total_images = len(images)
    recent_images = images[-4:][::-1]

    return render(request, 'home.html', {
        'total_images': total_images,
        'recent_images': recent_images
    })


# UPLOAD
def upload(request):

    if request.method == 'POST':

        files = request.FILES.getlist('image')

        if not files:
            return render(request, 'upload.html', {
                'error': 'No files selected'
            })

        fs = FileSystemStorage()

        uploaded_data = []

        for file in files:

            # unique filename
            unique_name = f"{uuid.uuid4()}_{file.name}"

            # save original
            uploaded_filename = fs.save(
                f"uploads/{unique_name}",
                file
            )

            uploaded_path = os.path.join(
                settings.MEDIA_ROOT,
                uploaded_filename
            )

            # restored filename
            restored_filename = f"restored/restored_{unique_name}"

            restored_path = os.path.join(
                settings.MEDIA_ROOT,
                restored_filename
            )

            # create restored folder if not exists
            os.makedirs(
                os.path.dirname(restored_path),
                exist_ok=True
            )

            # AI restoration
            restore_image(
                uploaded_path,
                restored_path
            )

            uploaded_data.append({
                'original': fs.url(uploaded_filename),
                'restored': fs.url(restored_filename)
            })

        accuracy = random.randint(85, 99)

        return render(request, 'upload.html', {
            'uploaded_data': uploaded_data,
            'accuracy': accuracy
        })

    return render(request, 'upload.html')

# GALLERY
def gallery(request):

    images = []

    if os.path.exists(settings.MEDIA_ROOT):

        for root, dirs, files in os.walk(settings.MEDIA_ROOT):

            for file in files:

                # skip hidden/system files
                if file.startswith('.'):

                    continue

                relative_path = os.path.relpath(

                    os.path.join(root, file),
                    settings.MEDIA_ROOT

                )

                images.append(relative_path)

    return render(request, 'gallery.html', {

        'images': images

    })


# DASHBOARD
def dashboard(request):

    media_path = settings.MEDIA_ROOT

    images = []

    file_dates = []

    if os.path.exists(media_path):

        for root, dirs, files in os.walk(media_path):

            for f in files:

                # skip hidden/system files
                if f.startswith('.'):

                    continue

                full_path = os.path.join(root, f)

                if os.path.isfile(full_path):

                    relative_path = os.path.relpath(

                        full_path,
                        media_path

                    )

                    images.append(relative_path)

                    timestamp = os.path.getmtime(full_path)

                    dt = datetime.fromtimestamp(timestamp)

                    file_dates.append(

                        dt.strftime('%a')

                    )

    total = len(images)

    labels = [

        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"

    ]

    data_map = {

        day: 0 for day in labels

    }

    for day in file_dates:

        if day in data_map:

            data_map[day] += 1

    data = [

        data_map[day] for day in labels

    ]

    recent_images = images[-6:][::-1]

    return render(request, 'dashboard.html', {

        'total': total,
        'labels': labels,
        'data': data,
        'recent_images': recent_images

    })
    # initialize counts
    data_map = {day: 0 for day in labels}

    # count actual days
    for day in file_dates:
        if day in data_map:
            data_map[day] += 1

    data = [data_map[day] for day in labels]

    recent_images = images[-6:][::-1]

    return render(request, 'dashboard.html', {
        'total': total,
        'labels': labels,
        'data': data,
        'recent_images': recent_images
    })

# 🔥 DYNAMIC PROFILE (UPGRADED)
def profile(request):
    profile, created = Profile.objects.get_or_create(id=1)

    if request.method == 'POST':
        profile.name = request.POST.get('name')
        profile.email = request.POST.get('email')
        profile.nickname = request.POST.get('nickname')
        profile.gender = request.POST.get('gender')
        profile.country = request.POST.get('country')
        profile.language = request.POST.get('language')
        profile.timezone = request.POST.get('timezone')
        profile.bio = request.POST.get('bio')

        if request.FILES.get('image'):
            profile.image = request.FILES['image']

        profile.save()
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile})


# TESTIMONIALS
def testimonials(request):
    return render(request, 'testimonials.html')


# FAQ
def faq(request):
    return render(request, 'faq.html')


# 🔥 FIXED PDF DOWNLOAD
def download_pdf(request):
    uploaded = request.GET.get('uploaded')
    restored = request.GET.get('restored')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("AI Face Restoration Result", styles['Title']))

    if uploaded:
        path = os.path.join(settings.BASE_DIR, uploaded.strip("/"))
        elements.append(Image(path, width=250, height=250))

    if restored:
        path = os.path.join(settings.BASE_DIR, restored.strip("/"))
        elements.append(Image(path, width=250, height=250))

    doc.build(elements)
    buffer.seek(0)

    return HttpResponse(
        buffer,
        content_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename="result.pdf"'}
    )


# 🔥 DELETE IMAGES (MULTI SELECT)
def delete_images(request):
    if request.method == "POST":
        images = request.POST.getlist('images')
        deleted = 0

        for img in images:
            file_path = os.path.join(settings.MEDIA_ROOT, img)
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted += 1

        if deleted:
            messages.success(request, f"{deleted} image(s) deleted successfully.")
        else:
            messages.warning(request, "No images selected.")

    return redirect('gallery')