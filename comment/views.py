from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import messages
from .models import Comment
from .forms import CommentForm
from post.models import Post
from django.contrib.auth.decorators import login_required
import requests
# Create your views here.


def detail_post(request, id):
    
    post = get_object_or_404(Post, id=id)
    comments_from_api = fetch_comments(id)
    comments_from_db = Comment.objects.filter(post=post)
    comments = list(comments_from_db) + comments_from_api  
    
    
    comment_form = CommentForm()

    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post  
            comment.user = request.user  
            comment.save()

            messages.success(request, "Your comment has been posted!")
            return redirect("detail-post", id=post.id) 
        else:
            messages.error(request, "There was an issue with your comment. Please try again.")

    return render(request, "details.html", {
        "data": post, 
        "comments": comments, 
        "comment_form": comment_form
    })



@login_required
def edit_comment(request, id):
    comment  = get_object_or_404(Comment, id = id)
    
    if request.method == "POST" and request.user == comment.user:

        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()

            return redirect("detail-post", id = comment.post.id)
        
    else:
        form = CommentForm(instance=comment)   

    return render(request, "edit_comment.html", {'form': form}) 
    

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id = id)

    if request.user == comment.user:
        comment.delete()

    return redirect("detail-post", id = comment.post.id)       



def fetch_comments(post_id):
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.RequestException as e:
        messages.error(requests, "Error while fetching comment: {e}")    
