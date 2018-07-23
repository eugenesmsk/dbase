# -*- coding: utf-8 -*-

from django.views.generic import ListView
from description.models import Part, Line, currEff, currEffInLine
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse
from django.contrib import auth
from django.db.models import Count


def PartyNumView(request, page_number = 1):

    all_parties = Part.objects.all()
    current_page = Paginator(all_parties, 20)
    countItems = range(current_page.count)
    eachMeasure = currEff.objects.annotate(number=Count('curreffinline'))


    list1 = list(eachMeasure.values('part_id'))         #создаём список словарей типа {'part_id':value}
    list2 = []
    for object in list1:
        list2.append((object['part_id']))               #достаём из list1 id измеренных партий

    currPage = current_page.page(page_number)           #создание списка партий на текущей странице
    listPage = []
    for object in currPage.object_list:
        listPage.append(object.id)                      #кладём в список listPage id партий на текущей странице
    notMeasure = list(set(listPage) - set(list2))               #создание списка неизмеренных партий

    try:
        context = current_page.page(page_number)
    except PageNotAnInteger:
        context = current_page.page(1)
    except EmptyPage:
        context = current_page.page(current_page.num_pages)

    return render_to_response('part_list.html', {'PartyNum': context, 'eachMeasure': eachMeasure, 'countItems': countItems, 'notMeasure': notMeasure, 'username': auth.get_user(request).username})


def forOne(request, pk, nums=None, fK_id__Party_number=None):
    onePart = get_object_or_404(Part, pk=pk)
    exemplar = Line.objects.filter(fK_id__Party_number=nums)
    crit = currEffInLine.objects.filter(fKey_id__part_id=pk)

    list1 = []
    list2 = []
    for object in exemplar:
        list1.append(object.num)
    for object in crit:
        list2.append(object.num)
    listMeas = list(set(list1) & set(list2))
    listNotMeas = list(set(list1) - set(list2))


    return render_to_response('singlePart.html', {'onePart': onePart, 'exemplar': exemplar, 'crit': crit, 'listMeas': listMeas, 'listNotMeas': listNotMeas, 'username': auth.get_user(request).username}, )

def printing(request, pk, nums=None, fK_id__Party_number=None):
    onePart = get_object_or_404(Part, pk=pk)
    exemplar = Line.objects.filter(fK_id__Party_number=nums)
    return render_to_response('printList.html', {'onePart': onePart, 'exemplar': exemplar, 'username': auth.get_user(request).username})

def measures(request):
    return  render_to_response('IcDesc.html', {'username': auth.get_user(request).username})




