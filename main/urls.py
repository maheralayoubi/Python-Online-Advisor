from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.mylogin, name="mylogin"),
    url(r'^links/$', views.links, name="links"),
    url(r'^login/$', views.mylogin, name="mylogin"),
    url(r'^signup1/$', views.signup1, name="signup1"),
    url(r'^signup2/(?P<user_id>.+)$', views.signup2, name="signup2"),
    url(r'^signup2_student/(?P<user_id>.+)$', views.signup2_student, name="signup2_student"),
    url(r'^signup3/(?P<user_id>.+)$', views.signup3, name="signup3"),
    url(r'^resetPass/$', views.resetPass, name="resetPass"),
    url(r'^resetPass1/$', views.resetPass1, name="resetPass1"),
    url(r'^resetPass2/(?P<token>.+)$', views.resetPass2, name="resetPass2"),
    url(r'^admin_page/$', views.admin_page, name="admin_page"),
    url(r'^instructor_page/(?P<ins_id>.+)', views.instructor_page, name="instructor_page"),
    url(r'^student_page/(?P<stu_id>.+)', views.student_page, name="student_page"),
    url(r'^lesson_page/(?P<lesson_id>.+)', views.lesson_page, name="lesson_page"),
    url(r'^small_lesson_page/$', views.small_lesson_page, name="small_lesson_page"),
    url(r'^block_instructor/(?P<user_id>.+)', views.block_instructor, name="block_instructor"),
    url(r'^block_student/(?P<user_id>.+)', views.block_student, name="block_student"),
    url(r'^advisors_page/$', views.advisors_page, name="advisors_page"),
    url(r'^lesson_details/(?P<lesson_id>.*)', views.lesson_details, name="lesson_details"),
    url(r'^lesson_reservation/$', views.lesson_reservation, name="lesson_reservation"),
    url(r'^edit_lesson_reservation/(?P<lesson_id>.+)$', views.edit_lesson_reservation, name="edit_lesson_reservation"),
    url(r'^reserved_lessons/$', views.reserved_lessons, name="reserved_lessons"),
    url(r'^history_lessons/$', views.history_lessons, name="history_lessons"),
    url(r'^delete_lesson/(?P<lesson_id>.+)', views.delete_lesson, name="delete_lesson"),
    url(r'^delete_lesson_admin/(?P<lesson_id>.+)', views.delete_lesson_admin, name="delete_lesson_admin"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^profile/(?P<user_id>.*)', views.profile, name="profile"),
    url(r'^student_profile/(?P<user_id>.*)', views.student_profile, name="student_profile"),
    url(r'^edit_profile/(?P<user_id>.+)', views.edit_profile, name="edit_profile"),
    url(r'^edit_student_profile/(?P<user_id>.+)', views.edit_student_profile, name="edit_student_profile"),
    url(r'^join_lesson/(?P<lesson_id>.+)', views.join_lesson, name="join_lesson"),
    url(r'^stored_chats/(?P<lesson_id>.+)', views.stored_chats, name="stored_chats"),
    
]


urlpatterns += staticfiles_urlpatterns()
