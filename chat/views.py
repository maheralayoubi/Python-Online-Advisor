from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from main.models import Instructor, Student, Lesson, User
from django.contrib import messages
from django.core.mail import send_mail
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
import json
from .models import Room, Widget_form
from datetime import datetime
from django.conf import settings as conf_settings

fake = Faker()
Signature = ' \n========== \nふらっと相談オンライン \nhttps://flatsodanonline.com \n《お問い合わせ》\nふらっと相談オンライン事務局 \ninfo@flatsodanonline.com （営業時間：平⽇ 10：00〜19：00）\n※本メールに覚えのない場合は、本メールを破棄して下さい。\n※本メールは⾃動送信のため、このメールへ直接返信は出来ません。'
client_URL = "https://flatsodanonline.com/online-advisor/"

def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})


def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chat/room_detail.html', {'room': room})


def token(request):
    identity = request.session["email"]
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MiniSlackChat:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8'),
        'username': request.session["email"],
    }

    return JsonResponse(response)


def chat(request):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'あなたが最初にログインする必要があります')
        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])

    lessons = Lesson.objects.all()
    user_lessons = []
    for lsn in lessons:
        if lsn.student is not None:
            if lsn.student.Id == logged_user.Id:
                user_lessons.append(lsn)

        if lsn.instructor.Id == logged_user.Id:
            user_lessons.append(lsn)

    return render(request, 'chat/chat.html', {'lessons': lessons, 'user_lessons': user_lessons, 'logged_user': logged_user})


def request_session(request, lesson_id):
    if not 'is_logged' in request.session.keys():
        messages.success(request, 'あなたが最初にログインする必要があります')

        return redirect('mylogin')
    logged_user = User.objects.get(username__exact=request.session['email'])

    lesson = Lesson.objects.get(pk=lesson_id)
    if request.POST:
        wf = Widget_form()
        if len(request.POST['date1']) > 5:
            wf.option1 = request.POST['date1'] + ' | ' + \
                request.POST['start-hour1'] + ' | ' + request.POST['start-min1']
        if len(request.POST['date2']) > 5:

            wf.option2 = request.POST['date2'] + ' | ' + \
                request.POST['start-hour2'] + ' | ' + request.POST['start-min2']
        if len(request.POST['date3']) > 5:
            wf.option3 = request.POST['date3'] + ' | ' + \
                request.POST['start-hour3'] + ' | ' + request.POST['start-min3']
        wf.lesson = Lesson.objects.get(pk=lesson_id)
        wf.instructor = wf.lesson.instructor
        wf.student = Student.objects.get(
            username__exact=request.session['email'])
        wf.save()
        messages.success(request, "レッスンリクエストの送信が完了しました。プロフィールページからリクエスト状況を確認出来ます。")
        email = wf.instructor.email
        send_mail(
                '予約リクエストがきています【ふらっと相談オンライン】',
                wf.instructor.name + ' 様, \n' + '「ふらっと相談オンライン」で予約リクエストがきています。\n=== \n候補⽇ 1：'+ wf.option1 +' \n候補⽇ 2：'+ wf.option2 +' \n候補⽇ 3：'+ wf.option3 +' \n=== \nこちら'+client_URL +'からログインして、候補⽇をお選びください。\n候補⽇の中に予約可能な⽇程がない場合は、ユーザーに再リクエストを申請してください。'+ Signature ,
                conf_settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

    return render(request, 'request_session.html', {'lesson': lesson, 'logged_user': logged_user})


def forward_to_student(request, wf_id):
    if request.POST:
        wf = Widget_form.objects.get(pk=wf_id)
        if 'choice' in request.POST.keys():
            choice = request.POST['choice']
            wf.status = 'Instructor Approved'
            wf.instructor_approved = True

            if choice == wf.option1:
                wf.option1_approved = True
            elif choice == wf.option2:
                wf.option2_approved = True
            elif choice == wf.option3:
                wf.option3_approved = True
        else:
            messages.success(
                request, '承認する日を選択するか、再提出を依頼する必要があります')
            return redirect('profile', user_id=wf.instructor.Id)
        wf.save()
        email = wf.student.email
        send_mail(
                '予約の候補日がきています【ふらっと相談オンライン】',
                wf.student.name + ' 様, \n' +'「ふらっと相談オンライン」でアドバイザーから予約の候補⽇がきています。\n=== \n候補⽇ 1：'+ choice +'\n予約を確定する場合は、こちら '+ client_URL +' からログインして「同意する」ボタンを送信してください。\n予約をキャンセルする場合は、「お名前」「メールアドレス」「ご予約⽇時」を記載の上、ふらっと相談オンライン事務局（info@flatsodanonline.com）までご連絡ください。'  + Signature,
                conf_settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
        
        return redirect('profile', user_id=wf.instructor.Id)

    return redirect('profile', user_id=wf.instructor.Id)


def student_final_confirmation(request, wf_id):
    if request.POST:
        logged_student = Student.objects.get(
            username__exact=request.session['email'])

        wf = Widget_form.objects.get(pk=wf_id)
        if 'submit' in request.POST.keys():
            wf.student_approved = True
            wf.status = 'Both Approved'
            wf.save()
            chosen = ''
            if wf.option1_approved:
                chosen = wf.option1
            elif wf.option2_approved:
                chosen = wf.option2
            elif wf.option3_approved:
                chosen = wf.option3
            email = wf.instructor.email

            send_mail(
                    '予約が確定しました【ふらっと相談オンライン】',
                    wf.instructor.name + ' 様, \n'+ '下記の内容でご予約が確定しました。\n===  \nレッスンタイトル：'+ wf.lesson.title +' \n⽇程： '+ chosen +' \n担当：'+ wf.instructor.name +'\n=== \nこちら '+ client_URL +' からログインしていただき、ユーザーに使⽤する WEB ツールに \nついてご連絡してください。'+Signature ,
                    conf_settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )

    return redirect('student_profile', user_id=wf.student.Id)


def resubmit(request, wf_id):
    wf = Widget_form.objects.get(pk=wf_id)
    wf.status = 'Student Should Resubmit'
    wf.save()
    email = wf.student.email
    send_mail(
            '予約の再リクエスト申請がきています【ふらっと相談オンライン】',
            wf.student.name + ' 様, \n' +'「ふらっと相談オンライン」でご希望の⽇程が合わなかったため、アドバイザーから予約の \n再リクエスト申請がきています。\n恐れ⼊りますが、こちら '+ client_URL +' からログインしていただき、別の⽇程で再度予 \n約リクエストを送信してください。' + Signature,
            conf_settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

    messages.success(request, '再リクエストの送信が完了しました')
    return redirect('profile', user_id=wf.instructor.Id)


def edit_session_request(request, wf_id):
    logged_user = User.objects.get(username__exact=request.session['email'])

    wf = Widget_form.objects.get(pk=wf_id)
    lesson = Lesson.objects.get(pk=wf.lesson.id)
    if request.POST:
        if len(request.POST['date1']) > 5:
            wf.option1 = request.POST['date1'] + ' | ' + \
                request.POST['start-hour1'] + ' | ' + request.POST['start-min1']
        if len(request.POST['date2']) > 5:
            wf.option2 = request.POST['date2'] + ' | ' + \
                request.POST['start-hour2'] + ' | ' + request.POST['start-min2']
        if len(request.POST['date3']) > 5:
            wf.option3 = request.POST['date3'] + ' | ' + \
                request.POST['start-hour3'] + ' | ' + request.POST['start-min3']
        wf.lesson = Lesson.objects.get(pk=wf.lesson.id)
        wf.instructor = wf.lesson.instructor
        wf.student = Student.objects.get(
            username__exact=request.session['email'])
        wf.student_ask_to_resubmit = False
        wf.status = "Pending"
        wf.save()
        messages.success(
            request, "リクエストが編集されました。プロフィールに移動してステータスを確認してください")
        
        email = wf.instructor.email
        send_mail(
                '予約リクエストがきています【ふらっと相談オンライン】',
                wf.instructor.name + ' 様, \n' + '「ふらっと相談オンライン」で予約リクエストがきています。\n=== \n候補⽇ 1：'+ wf.option1 +' \n候補⽇ 2：'+ wf.option2 +' \n候補⽇ 3：'+ wf.option3 +' \n=== \nこちら'+client_URL +'からログインして、候補⽇をお選びください。\n候補⽇の中に予約可能な⽇程がない場合は、ユーザーに再リクエストを申請してください。'+ Signature ,
                conf_settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
    return render(request, 'edit_session_request.html', {'lesson': lesson, 'logged_user': logged_user, 'wf': wf})

def complete_order(request):
    body = json.loads(request.body)
    wf = Widget_form.objects.get(pk=int(body['wf_id']))
    wf.paid = True
    wf.save()
    lesson = Lesson.objects.get(pk=wf.lesson.id)
    logged_student = Student.objects.get(username__exact=request.session['email'])
    lesson.student = logged_student
    lesson.save()
    new_lesson = Lesson(
                        title=wf.lesson.title,
                        starting= wf.lesson.starting,
                        ending=wf.lesson.ending,
                        Date = datetime.now(),
                        instructor = wf.lesson.instructor,
                        date_to_display = wf.lesson.date_to_display
                        )
    new_lesson.save()
    return JsonResponse('Payment completed', safe=False)



def rate(request):
    page = 'mylogin'
    if request.session['user_type'] == 'student':
        page = 'advisors_page'
    elif request.session['user_type'] == 'instructor':
        page = 'lesson_reservation'

    if request.POST:
        rate = ''
        if '1' in request.POST.keys():
            rate = 1
        elif '2' in request.POST.keys():
            rate = 2
        elif '3' in request.POST.keys():
            rate = 3
        elif '4' in request.POST.keys():
            rate = 4
        elif '5' in request.POST.keys():
            rate = 5


        if 'lesson_id' in request.POST.keys():
            lsn_id = request.POST['lesson_id']
            if lsn_id != '':
                lesson = Lesson.objects.get(pk = int(lsn_id))
                lesson.instructor.number_of_ratings += 1
                lesson.instructor.total_ratings += rate
                lesson.instructor.rating =  lesson.instructor.total_ratings / lesson.instructor.number_of_ratings
                lesson.instructor.save()

    return redirect(page)
