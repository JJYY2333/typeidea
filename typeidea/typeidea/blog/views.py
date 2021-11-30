from django.shortcuts import render
from django.http import HttpResponse

from .models import Post, Tag, Category

def post_list(request, category_id=None, tag_id = None):
    tag = None
    category = None

    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
            # print("tag: ", tag)
        except Tag.DoesNotExist:
            post_list=[]
        else:
            print(2)
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
            print(post_list)
    else:
        print(1)
        post_list = Post.objects.all()
        # post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                category = None
            else:
                post_list = post_list.filter(category_id=category_id)
    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
    }
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'name': 'post_detail'})

