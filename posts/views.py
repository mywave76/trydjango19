from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from urllib import quote_plus

from .forms import PostForm
from .models import Post

def post_create(request):
    #form = PostForm()
    # if request.method == "POST":
    #     print(request.POST.get("title"))
    #     print(request.POST.get("content"))
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Successfully created!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Creation failed!")

    context = {
        "form": form
    }
    return render(request, "post_form.html", context)

def post_detail(request, slug=None):
    #instance = Post.objects.get(id=10)
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string
    }
    return render(request, "post_detail.html", context)

def post_list(request):
	# if request.user.is_authenticated():
	# 	context = {
	# 	    "title": "My user List",
	# 	    "user": request.user
	# 	}
	# 	return render(request, "base.html", context)
	# else:
	# 	context = {
	# 	    "title": "List",
	# 	    "user": request.user
	# 	}
    # 	return render(request, "base.html", context)
    queryset_list = Post.objects.all() #.order_by("-timestamp")
    paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
    page_request_var = 'page'

    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var
    }
    return render(request, "post_list.html", context)

def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "<a href='#'>Item</a> saved!", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)

def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted!")
    return redirect("posts:list")
