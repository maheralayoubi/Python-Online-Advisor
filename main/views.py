from django.shortcuts import render, reverse, redirect
from main.models import Instructor, Student, Lesson, User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.mail import send_mail
import string, random
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from datetime import datetime, timedelta
from chat.models import Widget_form
import pytz
import os.path
from dateutil.relativedelta import *
from django.conf import settings as conf_settings

Signature = ' \n========== \nふらっと相談オンライン \nhttps://flatsodanonline.com \n《お問い合わせ》\nふらっと相談オンライン事務局 \ninfo@flatsodanonline.com （営業時間：平⽇ 10：00〜19：00）\n※本メールに覚えのない場合は、本メールを破棄して下さい。\n※本メールは⾃動送信のため、このメールへ直接返信は出来ません。'
client_URL = "flatsodanonline.com/online-advisor"



def links(request):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    users = User.objects.all()

    return render(request, 'links.html', {'users':users})


def logout(request):
    request.session.clear()
    return redirect('mylogin')

def mylogin(request):
    ADMIN_EMAIL = 'admin@admin.com'
    ADMIN_PASS = 'ba7ra'
    request.session.clear()
    if request.POST:
        email = request.POST['inputemail']
        password = request.POST['inputpassword']

        if email == ADMIN_EMAIL and password == ADMIN_PASS:
            request.session['is_logged'] = True
            request.session['email'] = email
            request.session['user_type']= 'admin'
            request.session['name'] = 'Admin'
            return redirect('admin_page')

        if Student.objects.filter(username__exact=email).count() > 0:
            user = Student.objects.filter(username__exact=email)
            if user.get().password == password and not user.get().blocked:
                request.session['is_logged'] = True
                request.session['email'] = email
                request.session['user_type']= 'student'
                request.session['name'] = user.get().name
                return redirect('advisors_page')
            else:
                if user.get().blocked:
                    messages.success(request, 'You Are Blocked!! contact admin for more info')
                else:
                    messages.success(request,"Password is incorrrect!!")
                return redirect('mylogin')

        elif Instructor.objects.filter(username__exact=email).count() > 0 :
            user = Instructor.objects.filter(username__exact=email)
            if user.get().password == password and not user.get().blocked:
                request.session['is_logged'] = True
                request.session['email'] = email
                request.session['user_type']= 'instructor'
                request.session['name'] = user.get().name
                return redirect('lesson_reservation')
            else:
                if user.get().blocked:
                    messages.success(request, 'You Are Blocked!! contact admin for more info')
                else:
                    messages.success(request,"Password is incorrrect!!")
                return redirect('mylogin')
        else:
            messages.success(request, 'Email pasword combination is incorrect')
            return render(request, 'Log-In.html')

    else:
        return render(request, "Log-In.html")

def signup1(request):
    request.session.clear()
    if request.POST:

        if 'name' in request.POST.keys() and 'email' in request.POST.keys() and 'inputpassword' in request.POST.keys():
            name =  request.POST['name']
            email = request.POST['email']
            passwrd = request.POST['inputpassword']
            user_type = request.POST['user-type']

            num_results = User.objects.filter(username__exact = email).count()
            if num_results > 0:
                messages.success(request, 'Email Exists!!')
                return render(request, 'sign-up-first-step.html')

            if user_type == 'instructor':
                newUser = Instructor()
            elif user_type =='student':
                newUser = Student()
            else:
                return redirect('signup1')
            newUser.name = name
            newUser.password = passwrd
            newUser.email = email
            newUser.username = email
            newUser.blocked = True
            newUser.save()
            if user_type == 'student':
                return redirect('signup2_student', user_id = newUser.Id)
            else:
                return redirect('signup2', user_id = newUser.Id)
    return render(request, 'sign-up-first-step.html')

def signup2(request, user_id):
    if request.POST:
        user = Instructor.objects.get(pk= user_id)
        if 'imgFile' in request.FILES.keys():
            fs = FileSystemStorage(location = conf_settings.MEDIA_ROOT)
            myfile = request.FILES['imgFile']
            filename = fs.save(user_id + '_img', myfile)
            user.img = user_id + '_img'
        if 'profession' in request.POST.keys() and 'catchphrase' in request.POST.keys():
            user.field = request.POST['profession']
            user.catch_phrase = request.POST['catchphrase']
            user.intro_msg = request.POST['self-introduction']
            user.what_you_can_ask_for = request.POST['askfor']
            user.paypal_account = request.POST['paypal_account']
            user.save()
            return redirect('signup3', user_id = user_id)
    return render(request, 'sign-up-second-step.html', context={'user_id':user_id})


def signup2_student(request, user_id):
    if request.POST:
        user = Student.objects.get(pk= user_id)
        if 'imgFile' in request.FILES.keys():
            fs = FileSystemStorage(location = conf_settings.MEDIA_ROOT)
            myfile = request.FILES['imgFile']
            filename = fs.save(user_id + '_img', myfile)
            user.img = user_id + '_img'
        if 'catchphrase' in request.POST.keys():
            user.catch_phrase = request.POST['catchphrase']
            user.intro_msg = request.POST['self-introduction']
            user.what_I_want_to_talk_about = request.POST['talkabout']
            user.save()
            return redirect('signup3', user_id = 's' + str(user_id))
    return render(request, 'signup2_student.html', context={'user_id':user_id})

def signup3(request, user_id):
    if request.POST:

        typ = user_id[0]
        if typ == 's':
            user_id = int(user_id[1:])
            user = Student.objects.get(pk=user_id)
        else:
            user = Instructor.objects.get(pk= user_id)
        user.blocked = False
        user.save()
        return redirect('mylogin')
    return render(request, 'sign-up-third-step.html', context={'user_id':user_id})

def resetPass(request):
    if request.POST:
        email = request.POST['email']
        exists = User.objects.filter(username__exact=email).exists()
        if exists:
            token = ''
            for i in range( len(str(email))):
                token += email[i] + random.choice(string.ascii_letters)


            send_mail(
                    'Reset Password',
                    'Dear User,\nPlease press on the link below to reset your password  <a href="https://flatsodanonline.com/online-advisor/resetPass2/?token=' + token + '">this is the link</a> ',
                    conf_settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )

            return redirect('resetPass1')
        else:
            messages.success(request, 'Email is Not registered')
            return render(request, 'reset-password.html')

    return render(request, 'reset-password.html')

def resetPass1(request):
    return render(request, 'reset-password1.html')

def extract_email(token):
    if not token: token = 'empty'
    email = ''
    for i in range(len(token)):
        if i % 2 == 0:
            email += token[i]
    return email

def resetPass2(request):

    if request.POST:
        email = request.POST['email']
        user = User.objects.get(username__exact = email)
        user.password = request.POST['password']
        user.save()
        messages.success(request, 'Password has changed successfuly')
        return redirect('mylogin')

    else:
        token = request.GET.get('token')
        email = extract_email(token)
        num_results = User.objects.filter(username__exact = email).count()
        if num_results:
            user = User.objects.filter(username__exact = email)
            messages.success(request, 'Welcome ')
            return render(request, 'reset-password2.html', {'user':user, 'email':user.get().email})

        else:
            messages.success(request, "YOU DON'T HAVE an ACCOUNT, please register first")
            return redirect('signup1')
        return render(request, 'reset-password2.html', {'user':user, 'email':email})


def admin_page(request):
    if not 'is_logged' in request.session.keys():
        return redirect('mylogin')
    else:
        if request.session['user_type'] != 'admin':
            messages.success(request, 'You Must Login as an Admin!')
            return redirect('logout')
    instructors = Instructor.objects.all()
    students = Student.objects.all()
    completed_lessons = []
    paid_wfs = Widget_form.objects.filter(paid__exact=True)
    now = datetime.now()

    for x in paid_wfs:
        d_str = "-".join(get_approved_date(x))
        d_obj = datetime.strptime(d_str[2:-1], '%y-%m-%d')
        if (d_obj < now):
            completed_lessons.append(x.lesson)

    tobe_started_lessons = Lesson.objects.filter(Date__gt=datetime.now())
    inprogress_lessons = Lesson.objects.filter(Date=datetime.today())
    monthly_completed_lessons = Lesson.objects.filter(Date__lt = datetime.now(), Date__gt = datetime.now() - relativedelta(months=1))
    total_sales = 1500 * len(completed_lessons)
    monthly_sales = 1500 * (len(monthly_completed_lessons))
    monthly_lessons = {'01': 0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
    months = []
    for lesson in completed_lessons:
        if lesson.Date.strftime('%m') in monthly_lessons.keys():
            monthly_lessons[lesson.Date.strftime('%m')] += 1500
    return render(request, 'admin.html',

                            context={   'completed_lessons':completed_lessons, 'tobe_started_lessons':tobe_started_lessons,
                                        'inprogress_lessons':inprogress_lessons, 'instructors':instructors,
                                        'students':students, 'len_completed_lessons':str(len(completed_lessons)),
                                        'len_inprogress_lessons':str(len(inprogress_lessons)), 'len_tobe_started_lessons':str(len(tobe_started_lessons)),
                                        'total_sales': total_sales, 'monthly_sales':monthly_sales, 'lsn_page':'lesson_page', 'monthly_lessons':monthly_lessons
                                    }
                )

def instructor_page(request, ins_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')

    ins = Instructor.objects.get(pk=ins_id)
    return render(request, 'Instructor_Page.html', {'ins':ins})

def student_page(request, stu_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')

    stu = Student.objects.get(pk=stu_id)
    return render(request, 'student_page.html', {'stu':stu})

def small_lesson_page(request):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])

    return render(request, 'smallLesson_page.html', {'logged_user': logged_user})

def lesson_page(request, lesson_id):

    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])
    lesson = Lesson.objects.get(pk=lesson_id)
    return render(request, 'lesson_page.html', {'logged_user':logged_user, 'lesson':lesson})

def block_instructor(request, user_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')

    user_x = Instructor.objects.get(pk= user_id)
    user_x.blocked = not user_x.blocked
    user_x.save()
    return redirect('admin_page')

def block_student(request, user_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')

    user_x = Student.objects.get(pk= user_id)
    user_x.blocked = not user_x.blocked
    user_x.save()
    return redirect('admin_page')

def advisors_page(request):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])

    instructors = (x for x in Instructor.objects.all() if  not x.instructor.blocked )
    todays_session = get_starting_time(request)
    return render (request, 'advisors.html', context={'instructors':instructors, 'logged_user':logged_user, 'todays_session':todays_session})

def edit_lesson_reservation(request, lesson_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])

    lesson = Lesson.objects.get(pk=lesson_id)
    if request.POST:
        lesson.title = request.POST['lesson-title']
        lesson.starting= request.POST['start-hour']+ ':'+request.POST['start-min']
        lesson.ending=request.POST['end-hour'] +' : '+ request.POST['end-min']
        lesson.Date = datetime.now()
        lesson.day = request.POST['day']
        lesson.save()
        return redirect('lesson_reservation')
    todays_session = get_starting_time(request)
    return render(request, 'edit_lesson_reservation.html', {'lesson_id':lesson_id, 'logged_user':logged_user, 'todays_session':todays_session})

def history_lessons(request):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])
    lessons = Lesson.objects.filter(Date__lt = datetime.now() - timedelta(days = 1))
    todays_session = get_starting_time(request)
    return render(request, 'history_lessons.html', {'logged_user':logged_user, 'lessons':lessons, 'todays_session':todays_session})

def lesson_details(request, lesson_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])
    lesson = Lesson.objects.get(pk=lesson_id)
    todays_session = get_starting_time(request)
    return render(request, 'lesson_details.html', {'logged_user':logged_user, 'lesson':lesson, 'todays_session':todays_session})

def lesson_reservation(request):

    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])
    if request.POST:

        ins = Instructor.objects.get(username__exact=request.session['email'])
        lesson = Lesson(
                        title=request.POST['lesson-title'],
                        starting= request.POST['start-hour']+ ':'+request.POST['start-min'],
                        ending=request.POST['end-hour'] +' : '+ request.POST['end-min'],
                        Date = datetime.now(),
                        day = request.POST['day'],
                        instructor = ins,
                        date_to_display = '('+ request.POST['day'] +') ' + request.POST['start-hour']+ ':'+request.POST['start-min'] + ' ~ ' + request.POST['end-hour'] +' : '+ request.POST['end-min']
                        )
        lesson.save()

    available_lessons = Lesson.objects.filter(student__isnull = True)
    history_lessons = Lesson.objects.filter(Date__lt = datetime.now() - timedelta(days=1), student__isnull = False)
    reserved_lessons = Lesson.objects.filter(student__isnull = False)
    todays_session = get_starting_time(request)

    return render(request, 'lesson_reservation.html', {'available_lessons':available_lessons, 'history_lessons':history_lessons, 'reserved_lessons':reserved_lessons, 'logged_user':logged_user, 'todays_session': todays_session})


def reserved_lessons(request):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])

    lessons = Lesson.objects.all()
    todays_session = get_starting_time(request)
    return render(request, 'reserved_lessons.html', {'lessons':lessons, 'logged_user':logged_user, 'todays_session': todays_session})

def delete_lesson_admin(request, lesson_id):

    lesson = Lesson.objects.get(pk=lesson_id)
    ins_email = lesson.instructor.email
    lesson.delete()

    emails = [ins_email]
    student_name = 'No student signed up'
    if lesson.student is not None:
        emails.append(lesson.student.email)
        student_name = lesson.student.name
        send_mail(
        '予約がキャンセルされました【ふらっと相談オンライン】',
        student_name + '様, \n' + '下記のご予約がキャンセルされました。\n===\nレッスンタイトル:' + lesson.title + '\n担当: '+ student_name+' \n===\n' + Signature ,
        conf_settings.EMAIL_HOST_USER,
        emails,
        fail_silently=False
          )
    send_mail(
        '予約がキャンセルされました【ふらっと相談オンライン】',
        lesson.instructor.name + '様, \n' + '下記のご予約がキャンセルされました。\n===\nレッスンタイトル:' + lesson.title + '\n担当: '+ student_name+' \n===\n' + Signature ,
        conf_settings.EMAIL_HOST_USER,
        emails,
        fail_silently=False
    )
    return redirect('admin_page')

def delete_lesson(request, lesson_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    lesson = Lesson.objects.get(pk=lesson_id)
    lesson.delete()
    return redirect('lesson_reservation')

def profile(request, user_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    utc=pytz.UTC
    logged_user = User.objects.get(username__exact=request.session['email'])
    user = Instructor.objects.get(pk=user_id)

    pending_wfs = (x for x in Widget_form.objects.all() if (x.instructor.Id == logged_user.Id and x.status=="Pending"))
    approved_wfs = (x for x in Widget_form.objects.all() if (x.instructor.Id == logged_user.Id and x.status == "Both Approved"))

    user_lessons = (x for x in Lesson.objects.all() if (x.instructor.Id == user.Id))
    available_lessons = (x for x in Lesson.objects.all() if (x.instructor.Id == user.Id and not x.student))
    history_lessons = (x for x in Lesson.objects.filter(Date__lt = datetime.now() - timedelta(days=1)) if (x.instructor.Id == user.Id))
    todays_session = get_starting_time(request)
    return render(request, 'profile.html', {
        'available_lessons':available_lessons,'user_lessons':user_lessons,'user':user,
        'logged_user':logged_user, 'approved_wfs':approved_wfs, 'pending_wfs':pending_wfs, 'history_lessons':history_lessons, 'todays_session': todays_session})

def edit_profile(request, user_id):
    print('url is : ', conf_settings.BASE_DIR)
    print('media:  ', conf_settings.MEDIA_ROOT)
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    if request.POST:
        user = Instructor.objects.get(pk= user_id)
        if 'imgFile' in request.FILES.keys():
            fs = FileSystemStorage(location = conf_settings.MEDIA_ROOT)
            if os.path.isfile(conf_settings.MEDIA_ROOT + '\\' + user_id+ '_img'):
                fs.delete(user_id+ '_img')

            myfile = request.FILES['imgFile']
            filename = fs.save(user_id + '_img', myfile)
            user.img = user_id + '_img'

        if 'profession' in request.POST.keys() and 'catch_phrase' in request.POST.keys():
            user.email = request.POST['email']
            user.name = request.POST['name']
            user.password = request.POST['inputpassword']
            user.field = request.POST['profession']
            user.catch_phrase = request.POST['catch_phrase']
            user.intro_msg = request.POST['self-introduction']
            user.what_you_can_ask_for = request.POST['what_you_can_ask_for']
            user.paypal_account = request.POST['paypal_account']
            user.save()
            messages.success(request, 'Profile has been updated')
            return redirect('profile', user_id = int(user_id))

    logged_user = User.objects.get(username__exact=request.session['email'])
    user = Instructor.objects.get(pk=user_id)
    todays_session = get_starting_time(request)
    return render(request, 'edit_profile.html', {'user':user, 'logged_user':logged_user, 'todays_session': todays_session})


def join_lesson(request, lesson_id):
    CREATED_BY = 20031996
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')

    logged_user = Student.objects.get(username__exact=request.session['email'])
    lesson = Lesson.objects.get(pk=lesson_id)
    if lesson.student is not None:
        if lesson.student.Id != logged_user.Id:
            messages.success(request, 'Session is full, sorry you can not join')
            return redirect('lesson_reservation')
    student = Student.objects.get(username = request.session['email'])
    lesson.student = student
    lesson.save()
    CREATED_BY += 1
    return redirect('chat')


def student_profile(request, user_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])
    if not(int(user_id) == logged_user.Id):
        messages.success(request, 'You are not logged in using Your account!')
        return redirect('mylogin')
    user = Student.objects.get(pk=user_id)
    wfs = (x for x in Widget_form.objects.all() if (x.student.Id == logged_user.Id ))
    todays_session = get_starting_time(request)
    return render(request, 'student_profile.html', {'wfs':wfs, 'logged_user':logged_user, 'user':user, 'todays_session': todays_session})


def edit_student_profile(request, user_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'You Must Login First!')
        return redirect('mylogin')
    if request.POST:
        user = Student.objects.get(pk= user_id)
        if 'imgFile' in request.FILES.keys():
            fs = FileSystemStorage(location = conf_settings.MEDIA_ROOT)
            if os.path.isfile(conf_settings.MEDIA_ROOT + '\\' +user_id+ '_img'):
                fs.delete(user_id+ '_img')
            myfile = request.FILES['imgFile']
            filename = fs.save(user_id + '_img', myfile)
            user.img = user_id + '_img'
            user.save()

        if 'catch_phrase' in request.POST.keys():
            user.email = request.POST['email']
            user.name = request.POST['name']
            user.password = request.POST['inputpassword']
            user.catch_phrase = request.POST['catch_phrase']
            user.intro_msg = request.POST['self-introduction']
            user.what_I_want_to_talk_about = request.POST['what_I_want_to_talk_about']
            user.save()
            return redirect('student_profile', user_id = int(user_id))

    logged_user = User.objects.get(username__exact=request.session['email'])
    user = Student.objects.get(pk=user_id)
    todays_session = get_starting_time(request)
    return render(request, 'edit_student_profile.html', {'user':user, 'logged_user':logged_user, 'todays_session': todays_session})


def get_approved_date(wf):
    if wf.option1_approved:
        return wf.option1.split("|")[0].split("-")
    elif wf.option2_approved:
        return wf.option2.split("|")[0].split("-")
    elif wf.option3_approved:
        return wf.option3.split("|")[0].split("-")


def get_starting_time(request):
    now = datetime.now()
    logged_user = User.objects.get(username__exact=request.session['email'])
    wfs = (x for x in Widget_form.objects.all() if ((x.student.Id == logged_user.Id or x.instructor.Id == logged_user.Id) and x.status == "Both Approved" and x.paid))
    todays_wfs = []

    for x in wfs:
        d_str = "-".join(get_approved_date(x))
        d_obj = datetime.strptime(d_str[2:-1], '%y-%m-%d')
        if (d_obj <= now):
            todays_wfs.append(x)

    list_of_times = []
    for wf in todays_wfs:
        day = 0
        month = 0
        year = 0
        h = 0
        m = 0
        if wf:
            date_arr = []
            if wf.option1_approved:
                date_arr = wf.option1.split("|")
            elif wf.option2_approved:
                date_arr = wf.option2.split("|")
            elif wf.option3_approved:
                date_arr = wf.option3.split("|")
            day = int(date_arr[0].split('-')[2])
            month = int(date_arr[0].split('-')[1])
            year = int(date_arr[0].split('-')[0])
            h = int(date_arr[1])
            m = int(date_arr[2])
        list_of_times.append([year, month, day, h, m, wf.id])
    return list_of_times


def stored_chats(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    return render(request, 'stored_chats.html', {'lesson_id': lesson_id, 'lesson':lesson})
