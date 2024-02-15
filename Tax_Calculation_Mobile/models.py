from django.db import models


class Calculation(models.Model):
    AY = models.IntegerField()  # Add this field for Assessment Year
    Regime = models.CharField(max_length=20)

    SalaryDA = models.DecimalField(max_digits=10, decimal_places=2)
    HRAReceived = models.DecimalField(max_digits=10, decimal_places=2)
    OtherAllowances = models.DecimalField(max_digits=10, decimal_places=2)
    LessAllowancesu10 = models.DecimalField(max_digits=10, decimal_places=2)
    ProfessionalTax = models.DecimalField(max_digits=10, decimal_places=2)
    StandardDeduction = models.DecimalField(max_digits=10, decimal_places=2)

    SelfOccupiedInterestonHouLoan = models.DecimalField(
        max_digits=10, decimal_places=2)
    RentReceived = models.DecimalField(max_digits=10, decimal_places=2)
    PropertyTax = models.DecimalField(max_digits=10, decimal_places=2)
    RentedHousePropertyInterestonHouLoan = models.DecimalField(
        max_digits=10, decimal_places=2)
    RepairCharges = models.DecimalField(max_digits=10, decimal_places=2)

    Business = models.DecimalField(max_digits=10, decimal_places=2)
    Profession = models.DecimalField(max_digits=10, decimal_places=2)

    SavingInterest = models.DecimalField(max_digits=10, decimal_places=2)
    FDInterest = models.DecimalField(max_digits=10, decimal_places=2)
    DividendIncome = models.DecimalField(max_digits=10, decimal_places=2)
    OtherIncome = models.DecimalField(max_digits=10, decimal_places=2)

    eighthLIC = models.DecimalField(max_digits=10, decimal_places=2)
    eighthProvidendFund = models.DecimalField(max_digits=10, decimal_places=2)
    eighthPPF = models.DecimalField(max_digits=10, decimal_places=2)
    eighthHousingLoanRepayment = models.DecimalField(
        max_digits=10, decimal_places=2)
    eighthNPS = models.DecimalField(max_digits=10, decimal_places=2)
    eighthELLS = models.DecimalField(max_digits=10, decimal_places=2)
    eighthTutionFees = models.DecimalField(max_digits=10, decimal_places=2)
    eighthOthers = models.DecimalField(max_digits=10, decimal_places=2)

    eighthDSelf = models.DecimalField(max_digits=10, decimal_places=2)
    eighthDParents = models.DecimalField(max_digits=10, decimal_places=2)
    eighthDD = models.DecimalField(max_digits=10, decimal_places=2)
    eighthDDB = models.DecimalField(max_digits=10, decimal_places=2)
    eighthCCDoneB = models.DecimalField(max_digits=10, decimal_places=2)
    eighthCCDtwo = models.DecimalField(max_digits=10, decimal_places=2)
    eighthEEA = models.DecimalField(max_digits=10, decimal_places=2)
    eighthFFB = models.DecimalField(max_digits=10, decimal_places=2)
    eighthU = models.DecimalField(max_digits=10, decimal_places=2)
    eighthE = models.DecimalField(max_digits=10, decimal_places=2)
    eighthGfiftypercent = models.DecimalField(max_digits=10, decimal_places=2)
    eighthGhundredpercent = models.DecimalField(
        max_digits=10, decimal_places=2)
    eighthGGA = models.DecimalField(max_digits=10, decimal_places=2)
    eighthGGC = models.DecimalField(max_digits=10, decimal_places=2)
    eighthTTA = models.DecimalField(max_digits=10, decimal_places=2)
    eighthTTB = models.DecimalField(max_digits=10, decimal_places=2)
