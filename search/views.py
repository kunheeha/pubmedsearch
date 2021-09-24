from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, DeleteView
from .models import Search, Article, Link
from .utils import obtain_article_links, create_article_object, create_link_object

def demo(request):
    # User Input, store in 'example+search+words' format in var 'search'
    if request.method == 'POST':
        keywords = request.POST['keywords']
        if len(Search.objects.filter(search=keywords)) > 0:
            prev_search = Search.objects.filter(search=keywords).first()
            return redirect('demo-search', search_id=prev_search.id)
        else:
            keyword_list = keywords.split()
            search = ""
            for i in range(len(keyword_list)-1):
                search += keyword_list[i]
                search += '+'
            search += keyword_list[-1]

            # Create Search object
            searchfolder = Search(search=keywords)
            searchfolder.save()
            # Scrape 10 articles
            article_links = obtain_article_links(search)
            # Create Article object for each of 10
            for article_link in article_links:
                scraped_article, pubmedlink = create_article_object(article_link, searchfolder)
                # Create Link object for each Article
                create_link_object(scraped_article, pubmedlink)

            return redirect('demo-search', search_id=searchfolder.id)

    searches = Search.objects.filter(user=None)
    
    context = {
        'searches': searches,
    }

    return render(request, 'search/demo.html', context)

def demo_search(request, *args, **kwargs):
    search_id = kwargs['search_id']
    search_object = get_object_or_404(Search, id=search_id)
    if search_object.user:
        raise PermissionDenied()

    articles = Article.objects.filter(search_folder=search_object)
    context = {
        'search': search_object,
        'articles': articles
    }

    return render(request, 'search/demo_search.html', context)

def demo_article(request, *args, **kwargs):
    article_id = kwargs['article_id']
    article_object = get_object_or_404(Article, id=article_id)
    links = Link.objects.filter(article=article_object)
    context = {
        'article': article_object,
        'links': links
    }

    return render(request, 'search/demo_article.html', context)

def delete_article(request, *args, **kwargs):
    article_object = get_object_or_404(Article, pk=kwargs['article_id'])
    article_object.delete()
    return redirect('demo-search', search_id=kwargs['search_id'])

def delete_search(request, *args, **kwargs):
    search_object = get_object_or_404(Search, pk=kwargs['search_id']) 
    search_object.delete()
    return redirect('demo')

@login_required
def search(request):
    searches = Search.objects.filter(user=request.user)

    # User Input, store in 'example+search+words' format in var 'search'
    if request.method == 'POST':
        keywords = request.POST['keywords']
        if len(searches.filter(search=keywords)) > 0:
            prev_search = searches.filter(search=keywords).first()
            return redirect('demo-search', search_id=prev_search.id)
        else:
            keyword_list = keywords.split()
            search = ""
            for i in range(len(keyword_list)-1):
                search += keyword_list[i]
                search += '+'
            search += keyword_list[-1]

            # Create Search object
            searchfolder = Search(search=keywords, user=request.user)
            searchfolder.save()
            # Scrape 10 articles
            article_links = obtain_article_links(search)
            # Create Article object for each of 10
            for article_link in article_links:
                scraped_article, pubmedlink = create_article_object(article_link, searchfolder)
                # Create Link object for each Article
                create_link_object(scraped_article, pubmedlink)

            return redirect('user-search', search_id=searchfolder.id)

    
    context = {
        'searches': searches,
    }

    return render(request, 'search/search.html', context)

@login_required
def user_search(request, *args, **kwargs):
    search_id = kwargs['search_id']
    search_object = get_object_or_404(Search, id=search_id)
    if not search_object.user == request.user:
        raise PermissionDenied()
    articles = Article.objects.filter(search_folder=search_object)
    context = {
        'search': search_object,
        'articles': articles
    }

    return render(request, 'search/user_search.html', context)

@login_required
def user_article(request, *args, **kwargs):
    article_id = kwargs['article_id']
    article_object = get_object_or_404(Article, id=article_id)
    if not article_object.search_folder.user == request.user:
        raise PermissionDenied()
    links = Link.objects.filter(article=article_object)
    context = {
        'article': article_object,
        'links': links
    }

    return render(request, 'search/user_article.html', context)

@login_required
def delete_user_article(request, *args, **kwargs):
    article_object = get_object_or_404(Article, pk=kwargs['article_id'])
    article_object.delete()
    return redirect('user-search', search_id=kwargs['search_id'])

@login_required
def delete_user_search(request, *args, **kwargs):
    search_object = get_object_or_404(Search, pk=kwargs['search_id']) 
    search_object.delete()
    return redirect('search')

