from django.shortcuts import render, redirect
from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from django.contrib.auth.decorators import login_required

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
            review.user = request.user
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

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('reviews:detail', review.pk)
        else: 
            form = ReviewForm(instance=review)
        
        context = {
            'form' : form
        }

        return render(request, 'reviews/update.html', context)
    
    else:
        return redirect('reviews:detail', review.pk)

def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        review.delete()
        return redirect('reivews:index')
    else:
        return redirect('reviews:detail', review.pk)

@login_required
def comments(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect('reviews:detail', review.pk)


def comments_del(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('reviews:detail', review_pk)