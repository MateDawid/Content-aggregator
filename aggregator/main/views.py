import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from main.models import Headline

def scrape(request):
    url = "https://www.focusnauka.pl/artykuly"

    page = requests.get(url)
    soup = BSoup(page.content, "html.parser")
    news = soup.find_all('a', attrs={"class":"d-flex flex-column box-all-link type-content-"})
    for article in news:
        title = article.find('h2').text.strip()
        link = "https://www.focusnauka.pl"+article['href']
        image_src = article.find("img")['data-src']

        if Headline.objects.filter(title=title).count() >= 1:
            continue
        else:
            new_headline = Headline()
            new_headline.title = title
            new_headline.url = link
            new_headline.image = image_src
            new_headline.save()
    
    return redirect("../")

def news_list(request):
    headlines = Headline.objects.all().order_by('-id')[:20][::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "main/home.html", context)

