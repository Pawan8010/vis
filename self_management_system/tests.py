from django.urls import path,include
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    # path('api/', include('core.urls')),
    # path('register/', views.register_view, name='register'),
    # path('login/', views.login_view, name='login'),

    # path('data/', views.data_view, name='data'),

    # # BACHAT
    # path('bachat/', views.bachat_view, name='bachat'),
    # path('AddMember/', views.AddMember, name='AddMember'),
    # path('ViewMembers/', views.view_members, name='ViewMembers'),

    # # LOAN
    # path('loanmanagement/', views.loanmanagement, name='loanmanagement'),
    # path('add-loan/', views.add_loan, name='add_loan'),
    # path('reports/', views.reports, name='reports'),
    # path('mark-paid/<int:loan_id>/', views.mark_paid, name='mark_paid'),

    # # PIGMI
    # path('pigmi/', views.pigmi_view, name='pigmi'),
    # path('pigmi_members/', views.add_pigmi_member, name='pigmi_add_member'),
    # path('pigmi_members/view/', views.view_pigmi_members, name='pigmi_view_members'),   
    # path('pigmi/deposit/', views.add_pigmi_collection, name='pigmi_deposit'),
    # path('pigmi/dashboard/', views.pigmi_dashboard, name='pigmi_dashboard'),
    # path('withdraw/<int:member_id>/', views.withdraw_pigmi, name='pigmi_withdraw'),
    # path('pigmi/member/<int:member_id>/', views.pigmi_member_detail, name='pigmi_member_detail'),
]