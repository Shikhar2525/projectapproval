from django.conf.global_settings import MEDIA_ROOT
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.sessions.models import Session

from .models import team, UserProfile, ProjectUpload, Comment
from django.core.files.storage import FileSystemStorage

def error(request):
    return render(request, 'error.html')

def select_cat(request):
    return render(request, 'select_cat.html')


def studentlogin(request):
    return render(request, 'eproject/studentlogin.html')


def facultylogin(request):
    return render(request, 'eproject/facultylogin.html')


def studentsignup(request):
    return render(request, 'eproject/studentsignup.html')


def facultysignup(request):
    return render(request, 'eproject/facultysignup.html')


def handlestudentsignup(request):  # studentsignup
    if request.method == 'POST':
        # Getting Data from html
        username = request.POST.get('enroll').upper().strip()
        fname = request.POST.get('fname').capitalize().strip()
        lname = request.POST.get('lname').capitalize().strip()
        email = request.POST.get('email')
        usertype = request.POST.get('utype').strip()
        contact = request.POST.get('contact')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        image = request.FILES.get('image')

        # Check For data already exists .
        try:
            e = User.objects.get(email=email)
        except User.DoesNotExist:
            e = None

        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            u = None
        # Check For data already exists .

        if e is not None:
            messages.error(request, 'Email is already taken', extra_tags='danger')
            return redirect('/eproject/studentsignup')
        if u is not None:
            value = 'Enrollment Number : ' + u.username + ' ' + 'already taken'
            messages.error(request, value, extra_tags='danger')
            return redirect('/eproject/studentsignup')
        if not username.isalnum():
            messages.error(request, 'Enrollment Number must be alphanumeric', extra_tags='danger')
            return redirect('/eproject/studentsignup')
        if len(username) != 14:
            messages.error(request, 'Wrong ! enrollment number ', extra_tags='danger')
            return redirect('/eproject/studentsignup')

        if pass1 == pass2:
            myuser = User.objects.create_user(username=username, email=email, password=pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.mobile = contact
            myuser.usertype = usertype
            image_extend = UserProfile(image=image, user=myuser)
            myuser.save()
            image_extend.save()
            # mailing
            # mess= ' Username :' + username + '   Password :' + pass1
            # send_mail('Welcome to Online Project Approval application', mess,
            #           'shikhar.mandloi@gmail.com', [email], fail_silently=False)
            parms = {'email': email}
            return render(request, 'accountcreated.html', parms)
        else:
            messages.error(request, 'Passoword Mismatched', extra_tags='danger')
            return redirect('/eproject/studentsignup')
    else:
        return HttpResponse("406 Bad Gateway")


def handlestudentlogin(request):
    if request.method == 'POST':
        username = request.POST.get('enroll').upper().strip()
        pass1 = request.POST.get('pass1')
        user = auth.authenticate(username=username, password=pass1)
        if user is not None:
            # getting team members
            t = team.objects.filter(lead_name=username)

            # getting projects
            try:
                project = ProjectUpload.objects.get(user=user)
            except Exception as ex:
                project= None

            parms = {'user': user, 't': t, 'md': MEDIA_ROOT, 'project': project}
            return render(request, "profile.html", parms)
        else:
            messages.error(request, 'Wrong Enrollment Number or Password', extra_tags='danger')
            return redirect('/eproject/studentlogin')
    else:
        return HttpResponse("406 Bad Gateway")


def studlogout(request):
    auth.logout(request)
    return redirect('/eproject/studentlogin')  # change it to homepage after done


def addteam(request):
    if request.method == 'POST':
        lead_name = request.POST.get('lead_name').strip()
        first_name = request.POST.get('first_name').strip().title()
        last_name = request.POST.get('last_name').strip().title()
        enroll = request.POST.get('enroll').upper().strip()
        email = request.POST.get('email').strip()
        contact = request.POST.get('contact').strip()
        role = request.POST.get('role').strip()

        user = User.objects.filter(username=enroll)
        t = team.objects.filter(enroll_no=enroll)
        t1 = team.objects.filter(lead_name=lead_name)
        # getting number of team members
        c=0
        for i in t1:
            c=c+1
        print(t1)
        if c<2:
            pass
        else:
            messages.error(request, 'Only 2 team members allowed . ', extra_tags='danger')
            return redirect('/eproject/error')

        if user or t:
            messages.error(request, 'User with this enrollment number , already exist', extra_tags='danger')
            return redirect('/eproject/error')
        if not enroll.isalnum():
            messages.error(request, 'Enrollment Number must be alphanumeric', extra_tags='danger')
            return redirect('/eproject/error')
        if len(enroll) != 14:
            messages.error(request, 'Wrong ! enrollment number ', extra_tags='danger')
            return redirect('/eproject/error')
        if len(contact) != 10:
            messages.error(request, 'Wrong ! Contact number', extra_tags='danger')
            return redirect('/eproject/error')
        else:
            t = team(lead_name=lead_name, first_name=first_name, last_name=last_name, enroll_no=enroll, email=email,
                     contact_no=contact, role=role)
            t.save()
            parms = {'lead_name': lead_name, 'first_name': first_name, 'last_name': last_name, 'enroll_no': enroll,
                     'email': email, 'contact_no': contact, 'role': role}
            return render(request, 'team_added.html', parms)
    else:
        return HttpResponse("406 Bad Gateway")


def changepp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        newpp = request.FILES.get('newpp')

        return HttpResponse("Success")
    else:
        return HttpResponse('Bad Gateway')


def upload(request):
    if request.method == 'POST':
        secret_key = request.POST.get('secret_key')
        parms = {'secret_key': secret_key}
        return render(request, 'eproject/upload.html', parms)
    else:
        return HttpResponse("404 Bad Protocol")


def handleproject(request):
    if request.method == 'POST':
        enroll = request.POST.get('secret_key')
        title = request.POST.get('ptitle').upper().strip()
        desc = request.POST.get('desc')
        techused = request.POST.get('techused')
        vlink = request.POST.get('vlink').strip()
        projectfile = request.FILES.get('projectfile')
        preport = request.FILES.get('preport')
        upload_date = request.POST.get('date')
        user = User.objects.get(username=enroll)

        project = ProjectUpload(user=user, title=title, desc=desc, tech=techused, v_link=vlink,
                                project_file=projectfile,p_report=preport)
        project.save()

        parms= {'title': title, 'name': user.first_name}

        return render(request, 'submitted.html', parms)

def view_project(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        t = team.objects.filter(lead_name=username)
        comment = Comment.objects.filter(username=username)
        count=0
        for i in comment:
            count=count+1
        try:
            project = ProjectUpload.objects.get(user=user)
        except Exception as ex:
            project = None
        parms={'user': user, 'project':project, 't':t, 'comment':comment, 'count':count}
        return render(request, 'view_project.html', parms)
    else:
        return HttpResponse('Bad Gateway')

def add_comment(request):
    if request.method == 'POST':
        username = request.POST.get('username').upper().strip()
        content = request.POST.get('content').strip()
        c = Comment(username=username, content=content)
        c.save()
        return render(request,'back.html')
    else:
        return HttpResponse('406 Bad Gateway')

def delete_project(request):
    if request.method =='POST':
        username= request.POST.get('username').strip()
        user = User.objects.get(username=username)
        project = ProjectUpload.objects.get(user=user)
        project.delete()
        return HttpResponse(username)
    else:
        return HttpResponse("406 Bad Gateway")

