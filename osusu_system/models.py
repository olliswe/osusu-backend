from django.db import models
from datetime import datetime, timedelta


class Tricycle(models.Model):
    full_name = models.CharField(verbose_name="Full Name", max_length=100)
    start_date = models.DateField(verbose_name="Start Date")
    maintenance = models.BooleanField(verbose_name="In Maintenance", default=True)

    def waiting_period(self):
        three_months = timedelta(3 * 365 / 12)
        return self.start_date + three_months < datetime.today()

    def payments_up_to_date(self):
        # if they've paid their dues
        # check if there is a payment in the system from this user in the previous month
        # 1st of March
        # number of months
        # x months * 100,000
        # compare
        # true/false
        pass

    def outstanding_payments(self):
        # if they've paid their dues
        # check if there is a payment in the system from this user in the previous month
        # 1st of March
        # number of months
        # x months * 100,000
        # compare
        # amount defecit
        pass

    #####

    def tot_claims(self):
        # total number of claims
        pass

    def total_value_claims(self):
        # sum of value of all claims
        pass

    def total_num_approved_claims(self):
        pass

    def total_val_approved_claims(self):
        pass

    ### ABOVE FUNCTIONS SHOULD BE REPEATED BUT FOR THE LAST 6 MONTHS


class Garage(models.Model):
    name = models.CharField(max_length=500, verbose_name="Garage Name")

    def total_no_claims(self):
        # sum of all claims
        pass

    def total_val_claims(self):
        # monetary sum of all claims
        pass

    def total_val_approved_claims(self):
        # sum of value of all claims that are approved
        pass

    def total_no_open_claims(self):
        pass

    def total_val_open_claims(self):
        pass

    def total_no_approved_not_paid_claims(self):
        pass

    def total_value_approved_not_paid_claims(self):
        pass


class Payment(models.Model):
    tricycle = models.ForeignKey(Tricycle, on_delete=models.CASCADE)
    amount = models.DecimalField(
        verbose_name="amount", decimal_places=2, max_digits=100
    )
    date = models.DateField(verbose_name="payment date")


class Claim(models.Model):
    STATUS_OPTIONS = [
        ("open", "Open"),
        ("approved", "Approved"),
        ("approved_paid", "Approved & Paid"),
        ("rejected", "Rejected"),
    ]
    tricycle = models.ForeignKey(Tricycle, models.CASCADE)
    garage = models.ForeignKey(Garage, models.CASCADE)
    status = models.CharField(choices=STATUS_OPTIONS, max_length=50)

    def total_value(self):
        # sum of all amounts in Parts
        pass


class Part(models.Model):
    name = models.CharField(verbose_name="Part name", max_length=100)
    amount = models.DecimalField(
        verbose_name="Part Amount (SLL)", decimal_places=2, max_digits=100
    )


class PartClaim(models.Model):
    number = models.IntegerField()
    claim = models.ForeignKey(Claim, models.CASCADE)


class Fund(models.Model):
    actual_amount = models.DecimalField(
        verbose_name="Actual Amount (filled by bank)", decimal_places=2, max_digits=100
    )

    def required_amount(self):
        # sum of all payments made - sum of all claims with status 'approved & paid'
        pass

    def total_available_amount_month(self):
        # 60% of all payments in previous month
        pass

    def remaining_available_amount_month(self):
        # total_available_amount_month - sum of all claims of the current month with status 'approved'
        pass
