from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Tax_Calculation_Mobile.models import Calculation
import json


@csrf_exempt
def calculate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extracting data from JSON for new fields
            assessment_year = data.get('AY', 0)
            tax_regime = data.get('Regime', '')

            # Extracting data from JSON
            salary_data = data.get('Salary', {})
            salary_da = salary_data.get('SalaryDA', 0)
            hra_received = salary_data.get('HRAReceived', 0)
            other_allowances = salary_data.get('OtherAllowances', 0)
            less_allowances_u10 = salary_data.get('LessAllowancesu10', 0)
            standard_deduction = salary_data.get('StandardDeduction', 0)
            Perquisites = salary_data.get('Perquisites', 0)
            Profit_in_liew_of_salary = salary_data.get('Profit_in_liew_of_salary', 0)
            Entertenment_Allowance = salary_data.get('Entertenment_Allowance', 0)
            Income_from_Ret_Benefit = salary_data.get('Income_from_Ret_Benefit', 0)
            # Logic for "Less : Allowances u/s 10, Professional Tax" based on the "Regime"
            if tax_regime.lower() == 'new':
                professional_tax = 0
            else:
                professional_tax = salary_data.get('ProfessionalTax', 0)

            house_property_data = data.get('HouseProperty', {})
            if tax_regime.lower() == 'new':
                self_occupied_interest_on_hou_loan = 0
            else:
                self_occupied_interest_on_hou_loan = house_property_data.get(
                    'SelfOccupiedInterestonHouLoan', 0)
            rent_received = house_property_data.get('RentReceived', 0)
            property_tax = house_property_data.get('PropertyTax', 0)
            rented_house_property_interest_on_hou_loan = house_property_data.get(
                'RentedHousePropertyInterestonHouLoan', 0)
            repair_charges = house_property_data.get('RepairCharges', 0)

            Deemed_Let_Out_Rent_Received = house_property_data.get('Deemed_Let_Out_Rent_Received', 0)
            Deemed_Let_Out_Property_Tax = house_property_data.get('Deemed_Let_Out_Property_Tax', 0)
            Deemed_Let_Out_Interest_on_Hou_Loan = house_property_data.get('Deemed_Let_Out_Interest_on_Hou_Loan', 0)
            Deemed_Let_Out_Repair_Charges = house_property_data.get('Deemed_Let_Out_Repair_Charges', 0)

            business_profession_data = data.get('BusinessProfession', {})
            business = business_profession_data.get('Business', 0)
            profession = business_profession_data.get('Profession', 0)

            other_sources_data = data.get('OtherSources', {})
            saving_interest = other_sources_data.get('SavingInterest', 0)
            fd_interest = other_sources_data.get('FDInterest', 0)
            dividend_income = other_sources_data.get('DividendIncome', 0)



          # Additional fields


            other_income = other_sources_data.get('OtherIncome', 0)
            Family_Pension = other_sources_data.get('Family_Pension', 0)
            Deduction_us_57  = other_sources_data.get('Deduction_us_57', 0)
            Divident = other_sources_data.get('Divident', 0)
            Unit_Trust_Of_India = other_sources_data.get('UnitTrustOfIndia', 0)
            Interest_from_deposits_Bank = other_sources_data.get('InterestFromDepositsBank', 0)
            Interest_on_Saving_Account = other_sources_data.get('InterestOnSavingAccount', 0)
            Post_Office = other_sources_data.get('PostOffice', 0)
            National_Savings_Certificate = other_sources_data.get('NationalSavingsCertificate', 0)
            Kisan_Vikas_Patras = other_sources_data.get('KisanVikasPatras', 0)
            Debentures = other_sources_data.get('Debentures', 0)
            Interests_on_Deposits_With_others = other_sources_data.get('InterestsOnDepositsWithOthers', 0)
            Security_of_Central_State_Government = other_sources_data.get('SecurityOfCentralStateGovernment', 0)
            Brokerage = other_sources_data.get('Brokerage', 0)
            Gift = other_sources_data.get('Gift', 0)
            Income_from_retirement_benefit_account_us_89A = other_sources_data.get('IncomeFromRetirementBenefitAccountUS89A', 0)
            Income_us_58_59 = other_sources_data.get('IncomeUS58_59', 0)
            Life_insurance_Policy = other_sources_data.get('LifeInsurancePolicy', 0)
            Income_due_to_disallowance_of_exemption_under_clauses_of_section_10 = other_sources_data.get('IncomeDueToDisallowanceOfExemptionUnderClausesOfSection10', 0)


            deduction_via_data = data.get('DeductionVIAeighthC', {})

            if tax_regime.lower() == 'new':
                eighth_lic = 0
                eighth_providend_fund = 0
                eighth_ppf = 0
                eighth_housing_loan_repayment = 0
                eighth_nps = 0
                eighth_ells = 0
                eighth_tution_fees = 0
                eighth_others = 0
            else:

                eighth_lic = deduction_via_data.get('eighthLIC', 0)
                eighth_providend_fund = deduction_via_data.get(
                    'eighthProvidendFund', 0)
                eighth_ppf = deduction_via_data.get('eighthPPF', 0)
                eighth_housing_loan_repayment = deduction_via_data.get(
                    'eighthHousingLoanRepayment', 0)
                eighth_nps = deduction_via_data.get('eighthNPS', 0)
                eighth_ells = deduction_via_data.get('eighthELLS', 0)
                eighth_tution_fees = deduction_via_data.get(
                    'eighthTutionFees', 0)
                eighth_others = deduction_via_data.get('eighthOthers', 0)

            AeighthC = data.get('80C', {})
            eighth_ccd_two = AeighthC.get('eighthCCDtwo', 0)
            if tax_regime.lower() == 'new':
                eighth_d_self = 0
                eighth_d_parents = 0
                eighth_dd = 0
                eighth_ddb = 0
                eighth_cc_done_b = 0
                eighth_eea = 0
                eighth_ffb = 0
                eighth_u = 0
                eighth_e = 0
                eighth_g_fifty_percent = 0
                eighth_g_hundred_percent = 0
                eighth_gga = 0
                eighth_ggc = 0
                eighth_tta = 0
                eighth_ttb = 0
            else:

                eighth_d_self = AeighthC.get('eighthDSelf', 0)
                eighth_d_parents = AeighthC.get(
                    'eighthDParents', 0)
                eighth_dd = AeighthC.get('eighthDD', 0)
                eighth_ddb = AeighthC.get('eighthDDB', 0)
                eighth_cc_done_b = AeighthC.get(
                    'eighthCCDoneB', 0)
                eighth_eea = AeighthC.get('eighthEEA', 0)
                eighth_ffb = AeighthC.get('eighthFFB', 0)
                eighth_u = AeighthC.get('eighthU', 0)
                eighth_e = AeighthC.get('eighthE', 0)
                eighth_g_fifty_percent = AeighthC.get(
                    'eighthGfiftypercent', 0)
                eighth_g_hundred_percent = AeighthC.get(
                    'eighthGhundredpercent', 0)
                eighth_gga = AeighthC.get('eighthGGA', 0)
                eighth_ggc = AeighthC.get('eighthGGC', 0)
                eighth_tta = AeighthC.get('eighthTTA', 0)
                eighth_ttb = AeighthC.get('eighthTTB', 0)

            LTCG = data.get('LTCG', {})
            LTCG_10Per_1503 = LTCG.get('LTCG_10Per_1503', 0)
            LTCG_10Per_1506 = LTCG.get('LTCG_10Per_1506', 0)
            LTCG_10Per_1509 = LTCG.get('LTCG_10Per_1509', 0)
            LTCG_10Per_1512 = LTCG.get('LTCG_10Per_1512', 0)
            LTCG_10Per_3103 = LTCG.get('LTCG_10Per_3103', 0)
            LTCG_112A_10Per_1503 = LTCG.get('LTCG_112A_10Per_1503', 0)
            LTCG_112A_10Per_1506 = LTCG.get('LTCG_112A_10Per_1506', 0)
            LTCG_112A_10Per_1509 = LTCG.get('LTCG_112A_10Per_1509', 0)
            LTCG_112A_10Per_1512 = LTCG.get('LTCG_112A_10Per_1512', 0)
            LTCG_112A_10Per_3103 = LTCG.get('LTCG_112A_10Per_3103', 0)
            LTCG_20Per_1503 = LTCG.get('LTCG_20Per_1503', 0)
            LTCG_20Per_1506 = LTCG.get('LTCG_20Per_1506', 0)
            LTCG_20Per_1509 = LTCG.get('LTCG_20Per_1509', 0)
            LTCG_20Per_1512 = LTCG.get('LTCG_20Per_1512', 0)
            LTCG_20Per_3103 = LTCG.get('LTCG_20Per_3103', 0)

            STCG = data.get('STCG', {})
            STCG_15Per_1503 = STCG.get('STCG_15Per_1503', 0)
            STCG_15Per_1506 = STCG.get('STCG_15Per_1506', 0)
            STCG_15Per_1509 = STCG.get('STCG_15Per_1509', 0)
            STCG_15Per_1512 = STCG.get('STCG_15Per_1512', 0)
            STCG_15Per_3103 = STCG.get('STCG_15Per_3103', 0)
            STCG_Normal_1503 = STCG.get('STCG_Normal_1503', 0)
            STCG_Normal_1506 = STCG.get('STCG_Normal_1506', 0)
            STCG_Normal_1509 = STCG.get('STCG_Normal_1509', 0)
            STCG_Normal_1512 = STCG.get('STCG_Normal_1512', 0)
            STCG_Normal_3103 = STCG.get('STCG_Normal_3103', 0)

            # Calculations
            salary = salary_da + hra_received + other_allowances + Perquisites + Profit_in_liew_of_salary - less_allowances_u10 - Entertenment_Allowance - professional_tax + Income_from_Ret_Benefit - standard_deduction

            house_property = rent_received - property_tax - \
                rented_house_property_interest_on_hou_loan
            repair_charges = (rent_received - property_tax) * 30 / 100

            house_property_1 = house_property - repair_charges

            house_property_2 = Deemed_Let_Out_Rent_Received - Deemed_Let_Out_Property_Tax - Deemed_Let_Out_Interest_on_Hou_Loan - Deemed_Let_Out_Repair_Charges

            final_house_property = house_property_1 - self_occupied_interest_on_hou_loan + house_property_2

            business_profession = business + profession

            other_sources = other_income + Family_Pension + Divident + Unit_Trust_Of_India + Interest_from_deposits_Bank + Interest_on_Saving_Account + Post_Office + National_Savings_Certificate + Kisan_Vikas_Patras + Debentures + Interests_on_Deposits_With_others + Security_of_Central_State_Government + Brokerage + Gift + Income_from_retirement_benefit_account_us_89A + Income_us_58_59 + Life_insurance_Policy + Income_due_to_disallowance_of_exemption_under_clauses_of_section_10 - Deduction_us_57

            deduction_via_data = eighth_lic + eighth_providend_fund + eighth_ppf + eighth_housing_loan_repayment + \
                eighth_nps + eighth_ells + eighth_tution_fees + eighth_others

            AeighthC = eighth_d_self + eighth_d_parents + \
                eighth_dd + eighth_ddb + eighth_cc_done_b + eighth_ccd_two + eighth_eea + eighth_ffb + eighth_u + \
                eighth_e + eighth_g_fifty_percent + eighth_g_hundred_percent + eighth_gga + eighth_ggc + eighth_tta + \
                eighth_ttb

            deduction_via_AeighthC_data = deduction_via_data + AeighthC

            LTCG_total = LTCG_10Per_1503 + LTCG_10Per_1506 + LTCG_10Per_1509 + LTCG_10Per_1512 + LTCG_10Per_3103 + \
                LTCG_112A_10Per_1503 + LTCG_112A_10Per_1506 + LTCG_112A_10Per_1509 + \
                LTCG_112A_10Per_1512 + LTCG_112A_10Per_3103 + LTCG_20Per_1503 + \
                LTCG_20Per_1506 + LTCG_20Per_1509 + LTCG_20Per_1512 + LTCG_20Per_3103

            STCG_total = STCG_15Per_1503 + STCG_15Per_1506 + STCG_15Per_1509 + STCG_15Per_1512 + STCG_15Per_3103 + \
                STCG_Normal_1503 + STCG_Normal_1506 + \
                STCG_Normal_1509 + STCG_Normal_1512 + STCG_Normal_3103

            LTCG_and_STCG_Total = LTCG_total + STCG_total

            result = {
                'Salary': salary,
                'HouseProperty': final_house_property,
                'BusinessProfession': business_profession,
                'OtherSources': other_sources,
                'DeductionVI': deduction_via_data,
                'AeighthC': AeighthC,
                'DeductionVI_and_AeighthC_Total': deduction_via_AeighthC_data,
                'LTCG_total': LTCG_total,
                'STCG_total': STCG_total,
                'LTCG_and_STCG_Total': LTCG_and_STCG_Total
            }

            return JsonResponse(result)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
