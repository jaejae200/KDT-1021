from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review 

# Create your views here.

def index(request):
    reviews = Review.objects.order_by('-pk')

    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/index.html', context)


def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return redirect('reviews:index')
    else:
        form = ReviewForm()
    
    context = {
        'form' : form
    }

    return render(request, 'reviews/create.html', context)
