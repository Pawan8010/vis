from django.db import models
from django.contrib.auth.models import User


# =========================
# REGISTER
# =========================
class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    group_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)

    scheme_type = models.CharField(
        max_length=20,
        choices=[
            ('pigmi', 'Pigmi'),
            ('bachat_gat', 'Bachat Gat'),
            ('both', 'Both')
        ],
        default='both'
    )

    registration_number = models.CharField(max_length=20, unique=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name


# =========================
# MEMBER (BACHAT GAT)
# =========================
class Member(models.Model):
    register = models.ForeignKey(Register, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    joining_date = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')],
        blank=True,
        null=True
    )

    deposit = models.FloatField()
    is_group_member = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# =========================
# LOAN
# =========================
class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)

    non_member_name = models.CharField(max_length=100, null=True, blank=True)
    non_member_phone = models.CharField(max_length=15, null=True, blank=True)

    amount = models.FloatField()
    interest = models.FloatField()
    duration = models.IntegerField()

    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.name} - {self.amount}"


# =========================
# PIGMI MEMBER
# =========================
class PigmiMember(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()
    start_date = models.DateField()
    daily_amount = models.FloatField()
    monthly_target = models.FloatField(null=True, blank=True)
    aadhar = models.CharField(max_length=12, null=True, blank=True)


class PigmiTransaction(models.Model):
    member = models.ForeignKey(PigmiMember, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20)  # DEPOSIT / WITHDRAW
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)