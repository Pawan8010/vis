from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Home
    path('', views.index, name='index'),

    # 🔐 Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # 📊 Dashboard
    path('dashboard/', views.data_view, name='data'),

    # 💰 Bachat & Pigmi
    path('bachat/', views.bachat_view, name='bachat'),

    # ❗ REMOVE DUPLICATE pigmi route
    path('pigmi/', views.pigmi_view, name='pigmi'),

    # 👤 Members
    path('add-member/', views.AddMember, name='add_member'),
    path('members/', views.view_members, name='view_members'),

    # 💸 Loans
    path('loan/', views.loanmanagement, name='loanmanagement'),
    path('add-loan/', views.add_loan, name='add_loan'),
    path('mark-paid/<int:loan_id>/', views.mark_paid, name='mark_paid'),

    # 📊 Reports
    path('reports/', views.reports, name='reports'),

    # 🐖 Pigmi System
    path('pigmi/add-member/', views.add_pigmi_member, name='pigmi_add_member'),
    path('pigmi/members/', views.view_pigmi_members, name='pigmi_view_members'),
    path('pigmi/dashboard/', views.pigmi_dashboard, name='pigmi_dashboard'),

    # 💰 Pigmi transactions
    path('pigmi/deposit/', views.add_pigmi_collection, name='pigmi_deposit'),
    path('pigmi/withdraw/<int:member_id>/', views.withdraw_pigmi, name='pigmi_withdraw'),
    path('pigmi/member/<int:member_id>/', views.pigmi_member_detail, name='pigmi_member_detail'),
]