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


def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()

    context = {
        'review' : review,
        'comments' : review.comment_set.all(),
        'comment_form' : comment_form,
    }
    
    return render(request, 'reviews/detail.html', context)
