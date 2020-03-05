from django.db import models
from datetime import datetime, timedelta
import locale
from django.conf import settings
import calendar
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender="osusu_system.PartClaim")
def set_value(sender, instance=None, created=False, **kwargs):
    if not instance.value:
        instance.value = instance.part.value * instance.number


locale.setlocale(locale.LC_ALL, "")


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


class Tricycle(models.Model):
    full_name = models.CharField(verbose_name="Full Name", max_length=100)
    start_date = models.DateField(verbose_name="Start Date")
    maintenance = models.BooleanField(verbose_name="In Maintenance", default=True)

    @property
    def waiting_period(self):
        three_months = timedelta(3 * 365 / 12)
        return self.start_date + three_months < datetime.today().date()

    @property
    def number_payments_made(self):
        return self.payment_set.count()

    @property
    def total_value_of_payments_made(self):
        result = 0
        for payment in self.payment_set.all():
            result += payment.amount
        return result

    @property
    def payments_up_to_date(self):
        return self.outstanding_payments <= 0

    @property
    def outstanding_payments(self):
        number_of_months = diff_month(datetime.today().date(), self.start_date)
        if number_of_months == 0:
            number_of_months = 1
        amount_owed = number_of_months * settings.PAYMENT_AMOUNT_IN_LE
        if amount_owed > 0:
            return amount_owed - self.total_value_of_payments_made
        else:
            return 0

    #####

    @property
    def tot_claims(self):
        return self.claim_set.all().count()

    @property
    def total_value_claims(self):
        total = 0
        for claim in self.claim_set.all():
            total += claim.total_value
        return total

    @property
    def total_num_approved_claims(self):
        return self.claim_set.filter(status="Approved").count()

    @property
    def total_val_approved_claims(self):
        total = 0
        for claim in self.claim_set.filter(status="Approved"):
            total += claim.total_value
        return total

    ### ABOVE FUNCTIONS SHOULD BE REPEATED BUT FOR THE LAST 6 MONTHS
    @property
    def claims_6_months(self):
        return self.claim_set.filter(
            date__gt=datetime.today().date() - timedelta(days=30 * 6)
        )

    @property
    def tot_claims_6_months(self):
        return self.claims_6_months.count()

    @property
    def total_value_claims_6_months(self):
        total = 0
        for claim in self.claims_6_months:
            total += claim.total_value
        return total

    @property
    def total_num_approved_claims_6_months(self):
        return self.claims_6_months.filter(status="Approved").count()

    @property
    def total_val_approved_claims_6_months(self):
        total = 0
        for claim in self.claims_6_months.filter(status="Approved"):
            total += claim.total_value
        return total


class Garage(models.Model):
    name = models.CharField(max_length=500, verbose_name="Garage Name")

    @property
    def total_no_claims(self):
        return self.claim_set.count()

    @property
    def total_val_claims(self):
        total = 0
        for claim in self.claim_set.all():
            total += claim.total_value
        return total

    @property
    def total_num_approved_claims(self):
        return self.claim_set.filter(status="Approved").count()

    @property
    def total_val_approved_claims(self):
        total = 0
        for claim in self.claim_set.filter(status="Approved"):
            total += claim.total_value
        return total

    @property
    def total_num_open_claims(self):
        return self.claim_set.filter(status="Open").count()

    @property
    def total_val_open_claims(self):
        total = 0
        for claim in self.claim_set.filter(status="Open"):
            total += claim.total_value
        return total

    @property
    def total_num_approved_not_paid_claims(self):
        return self.claim_set.filter(status="Approved & Paid").count()

    @property
    def total_val_approved_not_paid_claims(self):
        total = 0
        for claim in self.claim_set.filter(status="Approved & Paid"):
            total += claim.total_value
        return total


class Payment(models.Model):
    tricycle = models.ForeignKey(Tricycle, on_delete=models.CASCADE)
    amount = models.DecimalField(
        verbose_name="amount", decimal_places=2, max_digits=100
    )
    date = models.DateField(verbose_name="payment date")

    class Meta:
        ordering = ("-date",)


class Claim(models.Model):
    STATUS_OPTIONS = [
        ("Open", "Open"),
        ("Approved", "Approved"),
        ("Approved & Paid", "Approved & Paid"),
        ("Rejected", "Rejected"),
    ]
    tricycle = models.ForeignKey(Tricycle, models.CASCADE)
    garage = models.ForeignKey(Garage, models.CASCADE)
    status = models.CharField(choices=STATUS_OPTIONS, max_length=50, default="Open")
    date = models.DateField()

    @property
    def total_value(self):
        amount = 0
        for partclaim in self.partclaim_set.all():
            amount += partclaim.part.value * partclaim.number
        return amount


class Part(models.Model):
    name = models.CharField(verbose_name="Part name", max_length=100)
    value = models.DecimalField(
        verbose_name="Part Value (SLL)", decimal_places=2, max_digits=100
    )


class PartClaim(models.Model):
    number = models.IntegerField()
    part = models.ForeignKey(Part, verbose_name="Part", on_delete=models.CASCADE)
    claim = models.ForeignKey(Claim, models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)


class Fund(models.Model):
    actual_amount = models.DecimalField(
        verbose_name="Actual Amount (filled by bank)", decimal_places=2, max_digits=100
    )

    @property
    def required_amount(self):
        payments_made = 0
        for payment in Payment.objects.all():
            payments_made += payment.amount

        approved_and_paid_claims = 0
        for claim in Claim.objects.filter(status="Approved & Paid"):
            approved_and_paid_claims += claim.total_value
        # sum of all payments made - sum of all claims with status 'approved & paid'
        return payments_made - approved_and_paid_claims

    @property
    def total_available_amount_month(self):
        current_month = datetime.today().month
        current_year = datetime.today().year
        if current_month == 1:
            previous_month = 12
            year = current_year - 1
        else:
            previous_month = current_month - 1
            year = current_year
        last_day_of_month = calendar.monthrange(year, previous_month)[1]
        first_date_of_month = datetime(year, previous_month, 1)
        last_date_of_month = datetime(year, previous_month, last_day_of_month)
        payments = Payment.objects.filter(
            date__gt=first_date_of_month, date__lt=last_date_of_month
        )
        total_payments = 0
        for payment in payments:
            total_payments += payment.amount
        return 0.6 * float(total_payments)

    @property
    def remaining_available_amount_month(self):
        # total_available_amount_month - sum of all claims of the current month with status 'approved'
        current_month = datetime.today().month
        current_year = datetime.today().year
        first_date_of_month = datetime(current_year, current_month, 1)
        sum_of_claims = 0
        for claim in Claim.objects.filter(date__gt=first_date_of_month):
            sum_of_claims += float(claim.total_value)
        return self.total_available_amount_month - sum_of_claims
