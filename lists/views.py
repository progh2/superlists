from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
#def home_page():
#    pass


def home_page(request):
    # TODO: 모든 요청에 대해 비어있는 요청을 저장하지 않는다
    # TODO: 테이블에 아이템 여러 개 표시하기
    # TODO: 하나 이상의 목록 지원하기

    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items':items})