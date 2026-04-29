from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import Sum
from .models import Register, Member, Loan, PigmiMember, PigmiTransaction


# 🏠 Home
def index(request):
    return render(request, "self_management_system/index.html")
def register(request):
    return render(request, 'self_management_system/register.html')


# 🔢 Registration Number Generator
def generate_registration_number(scheme_type):
    prefix = "PG" if scheme_type == "pigmi" else "BG" if scheme_type == "bachat_gat" else "PB"

    last = Register.objects.order_by('-id').first()
    new_id = last.id + 1 if last else 1

    return f"{prefix}-{new_id:04d}"


# 🔐 LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            reg = Register.objects.filter(user=user).first()

            if reg:
                request.session['scheme_type'] = reg.scheme_type
                reg.last_login_time = now()
                reg.save()
            else:
                request.session['scheme_type'] = "both"

            return redirect('data')

        return render(request, "self_management_system/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "self_management_system/login.html")


# 📝 REGISTER
def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        group_name = request.POST.get("group_name")
        phone = request.POST.get("phone")
        city = request.POST.get("city")

        scheme_type = request.POST.get("scheme_type") or "both"

        if User.objects.filter(username=username).exists():
            return render(request, "self_management_system/register.html", {
                "error": "Username already exists"
            })

        registration_number = generate_registration_number(scheme_type)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = name
        user.save()

        Register.objects.create(
            user=user,
            name=name,
            group_name=group_name,
            phone=phone,
            city=city,
            scheme_type=scheme_type,
            registration_number=registration_number
        )

        login(request, user)
        request.session['scheme_type'] = scheme_type

        return redirect('data')

    return render(request, "self_management_system/register.html")


# 📊 DASHBOARD
@login_required
def data_view(request):
    return render(request, "self_management_system/data.html")


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# 💰 BACHAT VIEW
@login_required
def bachat_view(request):
    scheme = request.session.get('scheme_type')

    if scheme not in ['bachat_gat', 'both']:
        return HttpResponse("Access Denied ❌")

    return render(request, "self_management_system/bachat.html")


@login_required
def pigmi_view(request):
    scheme = request.session.get('scheme_type')

    if scheme not in ['pigmi', 'both']:
        return HttpResponse("Access Denied ❌")

    members = PigmiMember.objects.all()

    return render(request, "self_management_system/pigmi.html", {
        "members": members
    })


# 👤 ADD MEMBER
@login_required
def AddMember(request):
    scheme = request.session.get('scheme_type')

    if scheme not in ['bachat_gat', 'both']:
        return HttpResponse("Access Denied ❌")

    register = Register.objects.get(user=request.user)

    if request.method == "POST":
        Member.objects.create(
            register=register,
            name=request.POST.get("name"),
            mobile=request.POST.get("mobile"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            joining_date=request.POST.get("joining_date"),
            gender=request.POST.get("gender") or None,
            deposit=request.POST.get("deposit")
        )

        return redirect('ViewMembers')

    return render(request, "self_management_system/AddMember.html")


# 📋 VIEW MEMBERS
@login_required
def view_members(request):
    try:
        register = Register.objects.get(user=request.user)
        members = Member.objects.filter(register=register)

        return render(request, 'self_management_system/ViewMembers.html', {
            'members': members,
            'group': register
        })

    except Register.DoesNotExist:
        return render(request, 'self_management_system/ViewMembers.html', {
            'error': "Group not found ❌"
        })


# 💸 LOAN MANAGEMENT
@login_required
def loanmanagement(request):
    try:
        register = Register.objects.get(user=request.user)

        members = Member.objects.filter(register=register)
        loans = Loan.objects.all()

        return render(request, "self_management_system/loanmanagement.html", {
            "members": members,
            "loans": loans
        })

    except Register.DoesNotExist:
        return HttpResponse("Group not found ❌")


# ➕ ADD LOAN
@login_required
def add_loan(request):
    if request.method == "POST":
        member_type = request.POST.get("member_type")
        amount = request.POST.get("amount")
        duration = request.POST.get("duration")
        interest = request.POST.get("interest")

        if member_type == "group":
            member_id = request.POST.get("member_id")

            if not member_id:
                return HttpResponse("Please select a member ❌")

            member = Member.objects.get(id=member_id)

            Loan.objects.create(
                member=member,
                amount=amount,
                interest=interest,
                duration=duration
            )

        else:
            # ✅ NON-GROUP FIX
            name = request.POST.get("non_member_name")
            phone = request.POST.get("non_member_phone")

            if not name or not phone:
                return HttpResponse("Name and Phone required ❌")

            Loan.objects.create(
                member=None,
                non_member_name=name,
                non_member_phone=phone,
                amount=amount,
                interest=interest,
                duration=duration
            )

        return redirect('loanmanagement')

    return HttpResponse("Invalid Request ❌")


# 📊 REPORTS
@login_required
def reports(request):
    try:
        register = Register.objects.get(user=request.user)

        members = Member.objects.filter(register=register)
        loans = Loan.objects.all()

        context = {
            "total_members": members.count(),
            "total_loans": loans.count(),
            "total_amount": loans.aggregate(Sum('amount'))['amount__sum'] or 0,
            "pending_loans": loans.filter(is_paid=False).count(),
            "loans": loans
        }

        return render(request, "self_management_system/reports.html", context)

    except Register.DoesNotExist:
        return HttpResponse("Group not found ❌")


# ✅ MARK LOAN AS PAID
@login_required
def mark_paid(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    loan.is_paid = True
    loan.save()
    return redirect('reports')


# ➕ ADD PIGMI MEMBER
@login_required
def add_pigmi_member(request):
    if request.method == "POST":
        PigmiMember.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            address=request.POST['address'],
            start_date=request.POST['start_date'],
            daily_amount=request.POST['daily_amount'],
            monthly_target=request.POST.get('monthly_target') or 0,
            aadhar=request.POST.get('aadhar')
        )
        return redirect('pigmi_view_members')

    return render(request, "self_management_system/pigmi_add_member.html")


# 👥 VIEW PIGMI MEMBERS
@login_required
def view_pigmi_members(request):
    members = PigmiMember.objects.all().order_by('-id')
    return render(request, "self_management_system/pigmi_view_members.html", {'members': members})


# 💰 DASHBOARD
@login_required
def pigmi_dashboard(request):
    members = PigmiMember.objects.all()
    data = []

    for m in members:
        deposits = PigmiTransaction.objects.filter(member=m, transaction_type="DEPOSIT").aggregate(total=Sum('amount'))['total'] or 0
        withdraws = PigmiTransaction.objects.filter(member=m, transaction_type="WITHDRAW").aggregate(total=Sum('amount'))['total'] or 0

        data.append({
            "member": m,
            "deposit": deposits,
            "withdraw": withdraws,
            "balance": deposits - withdraws
        })

    return render(request, "self_management_system/pigmi_dashboard.html", {"data": data})

@login_required
def pigmi_member_detail(request, member_id):
    member = get_object_or_404(PigmiMember, id=member_id)

    deposits = PigmiTransaction.objects.filter(member=member, transaction_type="DEPOSIT")
    withdraws = PigmiTransaction.objects.filter(member=member, transaction_type="WITHDRAW")

    total_deposit = deposits.aggregate(total=Sum('amount'))['total'] or 0
    total_withdraw = withdraws.aggregate(total=Sum('amount'))['total'] or 0
    balance = total_deposit - total_withdraw

    return render(request, "self_management_system/pigmi_member_detail.html", {
        "member": member,
        "deposits": deposits,
        "withdraws": withdraws,
        "balance": balance
    })
@login_required
def add_pigmi_collection(request):
    members = PigmiMember.objects.all()

    if request.method == "POST":
        member_id = request.POST.get("member_id")
        amount = request.POST.get("amount")

        if not member_id:
            return HttpResponse("Member ID required ❌")

        member = PigmiMember.objects.get(id=member_id)

        PigmiTransaction.objects.create(
            member=member,
            transaction_type="DEPOSIT",
            amount=amount
        )

        return redirect('pigmi_view_members')

    return render(request, "self_management_system/pigmi_deposit.html", {
        "members": members
    })
@login_required
def withdraw_pigmi(request, member_id):
    member = get_object_or_404(PigmiMember, id=member_id)

    if request.method == "POST":
        amount = float(request.POST['amount'])

        PigmiTransaction.objects.create(
            member=member,
            transaction_type="WITHDRAW",
            amount=amount
        )

        return redirect('pigmi_view_members')

    return render(request, "self_management_system/pigmi_withdraw.html", {
        "member": member
    })