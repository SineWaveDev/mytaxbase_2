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
           # Logic for "Less : Allowances u/s 10, Professional Tax" based on the "Regime"
            if tax_regime.lower() == 'new':
                professional_tax = 0
            else:
                professional_tax = salary_data.get('ProfessionalTax', 0)

            less_allowances_u10 = salary_data.get('LessAllowancesu10', 0)
            standard_deduction = salary_data.get('StandardDeduction', 0)

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

            business_profession_data = data.get('BusinessProfession', {})
            business = business_profession_data.get('Business', 0)
            profession = business_profession_data.get('Profession', 0)

            other_sources_data = data.get('OtherSources', {})
            saving_interest = other_sources_data.get('SavingInterest', 0)
            fd_interest = other_sources_data.get('FDInterest', 0)
            dividend_income = 0
            other_income = other_sources_data.get('OtherIncome', 0)

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
            salary = salary_da + hra_received + other_allowances - \
                less_allowances_u10 - professional_tax - standard_deduction

            house_property = rent_received - property_tax - \
                rented_house_property_interest_on_hou_loan
            repair_charges = (rent_received - property_tax) * 30 / 100

            house_property_1 = house_property - repair_charges
            final_house_property = house_property_1 - self_occupied_interest_on_hou_loan

            business_profession = business + profession

            other_sources = saving_interest + fd_interest + dividend_income + other_income

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
                STCG_Normal_1503 + STCG_Normal_1506 + STCG_Normal_1509 + \
                STCG_Normal_1512 + STCG_Normal_3103

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
