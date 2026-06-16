from django.shortcuts import redirect, render, get_object_or_404
from .models import Article
from .forms import ContactForm
from django.contrib import messages
from .tasks import send_email_task
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, "index.html")

def heart_day_view(request):
    return render(request, "heartday.html")

def education_view(request):
    articles = Article.objects.filter(published=True).order_by('-created_at')
    if not articles:
        return render(request, "education.html", {"articles": articles, "message": "No articles available."})
    return render(request, "education.html", {"posts": articles})

def education_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)
    related_articles = Article.objects.exclude(slug=slug, published=True)[:4]  # Get 4 related articles excluding the current one
    if not related_articles:
        related_articles = Article.objects.filter(published=True)[:4]  # Fallback to any 4 articles if none are related
    return render(request, "blog/blog.html", {"article": article, "related_articles": related_articles})



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd['first_name']
            last_name  = cd.get('last_name', '') or ''
            subject    = cd['subject']
            email      = cd.get('email', '')
            phone      = cd.get('phone', '')
            message    = cd['message']

            full_name = f"{first_name} {last_name}".strip()

            contact_lines = []
            if email:
                contact_lines.append(f"Email: {email}")
            if phone:
                contact_lines.append(f"Phone: {phone}")
            contact_info = "\n".join(contact_lines)

            email_subject = f"Website Enquiry - {subject} from {first_name}"
            email_body = (
                f"Enquiry from website:\n\n"
                f"{full_name}\n"
                f"{contact_info}\n\n"
                f"Has the following enquiry\n\n"
                f"{message}"
            )

            send_email_task.delay(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.TO_EMAIL,],
            )

            messages.success(request, "Your message has been sent. We'll be in touch soon!")
            return redirect('clinic_app:contact-us')
    else:
        form = ContactForm()

    return render(request, 'contact-us.html', {'form': form})