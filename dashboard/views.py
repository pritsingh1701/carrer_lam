# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from home.models import *
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# from .forms import *
import json, random



class indexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        print self.request.POST

        allcompanies = companies.objects.all()
        allcompanies_list = []
        for comps in allcompanies:
            if int(company_interviews.objects.filter(company=comps).count()) > 0:
                allcompanies_list.append(comps)

        paginator = Paginator(allcompanies_list, 30)

        page = self.request.GET.get('page')
        try:
            allcompanies_list = paginator.page(page)
        except PageNotAnInteger:
            allcompanies_list = paginator.page(1)
        except EmptyPage:
            allcompanies_list = paginator.page(paginator.num_pages)

        comps   = []

        for compo in allcompanies_list:
            mydict = {
                "co":compo,
                "count":int(company_interviews.objects.filter(company=compo).count())
            }
            comps.append(mydict)

        context['companySpoof'] = allcompanies_list
        context['companies'] = comps
        return context


class writeAReviewView(TemplateView):
    template_name = "write_feedback.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('admin:index'))
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        allcompanies = companies.objects.all().order_by('company_name')
        allcolleges     = all_colleges.objects.all().order_by('college_name')
        context['companies'] = allcompanies
        context['allcolleges'] = allcolleges
        return context

class writeReviewRest(TemplateView):
    template_name = "write_review_all.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        compid          = self.kwargs['pk']
        interviewinsta      = company_interviews.objects.get(pk=compid)
        allQualifications       = qualifications.objects.all().order_by('qualification_name')


        context['interviewinsta'] =  interviewinsta
        context['allQualifications'] = allQualifications

        return context

class thanks_pageView(TemplateView):
    template_name = "thanks.html"

class companyView(TemplateView):
    template_name = "company_page.html"
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        compid          = self.kwargs['pk']
        cominsta        = companies.objects.get(pk=compid)


        queryObject  = Q(company=cominsta) & Q(show_stat='show')
        allinterview = company_interviews.objects.filter(queryObject).order_by('-id')

        totalCount   = company_interviews.objects.filter(queryObject).count()

        paginator = Paginator(allinterview, 10)

        page = self.request.GET.get('page')
        try:
            allinterview = paginator.page(page)
        except PageNotAnInteger:
            allinterview = paginator.page(1)
        except EmptyPage:
            allinterview = paginator.page(paginator.num_pages)

        companySpoof = allinterview

        interviewcontent = []
        for inter in allinterview:

            profile_image = "https://graph.facebook.com/{0}/picture?type=normal".format(inter.submittedBy.social_auth.get().uid)
            try:
                userSubinfo     = userinformation.objects.get(user=inter.submittedBy)

            except:
                userSubinfo = {
                    "userProfileImage":"",
	                "current_job_profile":"",
	                "current_location":"",
                }
            mydict = {
                "main_data":inter,
                "user":userSubinfo,
                "profile_image":profile_image,
            }
            interviewcontent.append(mydict)


        context['company'] = cominsta
        context['allinterview'] = interviewcontent
        context['companySpoof'] = companySpoof
        context['totalCount'] = totalCount




        return context


class loginView(TemplateView):
    template_name = "login.html"

class registerView(TemplateView):
    template_name = "register.html"


class profileView(TemplateView):
    template_name   = "profile.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        try:
            userinfo = userinformation.objects.get(user=self.request.user)
            context['userinfo'] = userinfo
        except:
            context['userinfo'] = ""


        return context

class all_list_companiesView(TemplateView):
    template_name = "allcompanies.html"

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        search_keyword = self.request.GET.get('q')
        search_results = companies.objects.filter(company_name__icontains=search_keyword).order_by('company_name')
        context['companies'] = search_results
        context['query'] = search_keyword

        return context









index           = indexView.as_view()
writeAReview    = writeAReviewView.as_view()
writeReviewRest     =  writeReviewRest.as_view()
thanks_page         = thanks_pageView.as_view()
company         = companyView.as_view()
login           = loginView.as_view()
register        = registerView.as_view()
profile         = profileView.as_view()
all_list_companies  = all_list_companiesView.as_view()




# DEF FUNCTIONS

def update_user_profile(request):

    if request.method == 'POST':
        job_desing                          = request.POST['jobprofile']
        location                            = request.POST['location']
        try:
            userinsta                           = userinformation.objects.get(user=request.user)
        except:
            userinsta                           = userinformation(user=request.user)
        userinsta.current_job_profile       = job_desing
        userinsta.current_location          = location
        userinsta.save()
        return HttpResponseRedirect(reverse('dashboard:profile'))
    else:
        return HttpResponse('not allowed')

def register_me(request):
    if request.method == 'POST':
        first_name      = request.POST['first_name']
        last_name       = request.POST['last_name']
        email           = request.POST['email']
        password        = request.POST['password']
        username = "{0}{1}_{2}".format(first_name,last_name,random.randint(999,9999))

        try:
            stat    = User.objects.get(email=email)
            print "PRESENT"
            return render(request,"register.html",{"msg":"Email is already registed with us"})
        except:
            pass


        userinsta = User.objects.create_user(username=username,email=email,password=password)
        userinsta.first_name = first_name
        userinsta.last_name  = last_name
        userinsta.save()
        return  HttpResponseRedirect(reverse('dashboard:login'))
    else:
        return HttpResponse('not allowed')



def logoutUser(request):
    logout_user(request)
    request.session['userimage'] = ''
    return HttpResponseRedirect(reverse('dashboard:index'))


def login_check(request):
    if request.method == 'POST':
        email            = request.POST['email']
        password         = request.POST['password']
        try:
            getEmail            = User.objects.get(email=email)
            user = authenticate(request,username=getEmail.username, password=password)
            if user is not None:
                login_user(request, user)
                try:
                    userinsta = userinformation.objects.get(user=user)
                    request.session['userimage'] =  str(userinsta.userProfileImage)
                except:
                    pass
                return  HttpResponseRedirect(reverse('dashboard:index'))
            else:
                return render(request,"login.html",{"msg":"Login Failed "})
        except:
            return render(request, "login.html", {"msg": "Login Failed "})

    else:
        return HttpResponse('not allowed')





def get_all_companies(request):
    allcompanies = companies.objects.all()
    comps = []
    for co in allcompanies:
        mydict = {
            "name":co.company_name,
            "id":int(co.id)
        }
        comps.append(mydict)

    mimetype = 'application/json'

    return HttpResponse(json.dumps(comps),mimetype)


@login_required(login_url='/login/')
def submitPhaseOne(request):
    if request.method == 'POST':
        print request.POST
        companyname  = request.POST['company']
        designation = request.POST['job_designation']
        experience = request.POST['experince']
        anonymosStat = request.POST['anonymosStat']
        college_name = request.POST['college_name']



        companyinsta                      = companies.objects.get(pk=companyname)
        collegeInsta                      = all_colleges.objects.get(pk=college_name)

        insInsta                          = company_interviews(company=companyinsta)
        insInsta.job_title_designation    = designation
        insInsta.submittedBy              = request.user
        insInsta.college_name             = collegeInsta
        insInsta.work_experience          = experience
        insInsta.keep_anonymous           = anonymosStat
        insInsta.save()
        submitID        = insInsta.id
        return HttpResponseRedirect(reverse('dashboard:writeReviewRest',args=(submitID,)))
    else:
        return HttpResponse('not allowed')

@login_required(login_url='/login/')
@csrf_exempt
def writeSubProcess(request):
    if request.method == 'POST':
        postVals =  json.loads(request.body)
        reviewid                = postVals['reviewid']
        process                 = postVals['process']
        insInsta                = interviews.objects.get(pk=reviewid)
        askedInsta              = questionsAsked(interview=insInsta)
        askedInsta.questions    = process
        askedInsta.save()
        allInterview            = questionsAsked.objects.filter(interview=reviewid)
        data        = []
        for dd in allInterview:
            mydict = {"id":dd.id,"name":dd.questions}
            data.append(mydict)
        resp = {"status":"true","data":data}
        mimetype = 'application/json'
        return HttpResponse(json.dumps(resp), mimetype)
    else:
        return HttpResponse('not allowed')

@login_required(login_url='/login/')
@csrf_exempt
def deleteSubProcess(request):
    if request.method == 'POST':
        postVals = json.loads(request.body)


        reviewid                = postVals['reviewid']
        mainid                  = postVals['mainid']
        questionsAsked.objects.get(pk=reviewid).delete()

        allInterview            = questionsAsked.objects.filter(interview=mainid)
        data        = []
        for dd in allInterview:
            mydict = {"id":dd.id,"name":dd.questions}
            data.append(mydict)
        resp = {"status":"true","data":data}

        mimetype = 'application/json'
        return HttpResponse(json.dumps(resp), mimetype)

    else:
        return HttpResponse('not allowed')



@login_required(login_url='/login/')
def submitPhaseTwo(request):
    if request.method == 'POST':

        qualification           = request.POST['qualification']
        appearmonth             = request.POST['appearmonth']
        appearyear              = request.POST['appearyear']
        interviewProcess           = request.POST['interviewProcess']
        anything_else               = request.POST['anything_else']

        howFindeasy                 = request.POST['HowFind']
        HowOffer                = request.POST['HowOffer']
        reviewid                = request.POST['reviewid']

        qualification =             qualifications.objects.get(pk=qualification)

        interviewInsta                          = company_interviews.objects.get(pk=reviewid)

        interviewInsta.highest_qualification    = qualification
        interviewInsta.apear_month              = appearmonth
        interviewInsta.apear_year               = appearyear
        interviewInsta.interview_prccess        = interviewProcess
        interviewInsta.anything_else_review     = anything_else
        interviewInsta.how_did_you_get          = howFindeasy
        interviewInsta.did_you_get_offer        = HowOffer

        interviewInsta.show_stat                 = "show"
        interviewInsta.save()


        return HttpResponseRedirect(reverse('dashboard:thanks_page'))
    else:
        return HttpResponse('not allowed')

