from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_home(request):
    return HttpResponse("<h1>Hello.. Welcome to POSTS.<h1>")


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "<a href ='#'>item </a>Successfully Created", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())
    #    else:
    #        messages.error(request, "Fail to create")

    # if request.method == "POST":
    #    print(request.POST.get("content"))
    #    print(request.POST.get("title"))
    #    # Post.object.create(title= title)
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):  # retrive
    # instance = Post.objects.get(id=2)
    instance = get_object_or_404(Post, id=id)
    # instance = get_object_or_404(Post, title="Hello,")
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "post_detail.html", context)


def post_list(request):  # list_iteams
    queryset_list = Post.objects.all() #.order_by("-timestamp")

    paginator = Paginator(queryset_list, 5)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset= paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var
    }
    # if request.user.is_authenticated():
    #    context = {
    #        "title": "List_Authenticated"
    #    }
    # return render(request, "index2.html", context)
    # else:
    #    context = {
    #        "title": "List_UnAuthenticated"
    #    }
    # return render(request, "index3.html", context)
    return render(request, "post_list.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:home")
