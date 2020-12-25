from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'token$', views.token, name="token"),
    url(r'rooms/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),
    url(r'^chat/$', views.chat, name="chat"),
    url(r'chat/$', views.token, name="token"),
    url(r'request_session/(?P<lesson_id>.+)', views.request_session, name="request_session"),
    url(r'edit_session_request/(?P<wf_id>.+)', views.edit_session_request, name="edit_session_request"),
    url(r'forward_to_student/(?P<wf_id>.+)', views.forward_to_student, name="forward_to_student"),
    url(r'student_final_confirmation/(?P<wf_id>.+)', views.student_final_confirmation, name="student_final_confirmation"),
    url(r'resubmit/(?P<wf_id>.+)', views.resubmit, name="resubmit"),
    url(r'complete_order/$', views.complete_order, name="complete_order"),
    url(r'rate/$', views.rate, name="rate"),
]
