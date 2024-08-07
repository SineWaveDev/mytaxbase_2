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


            # Correctly assign values from other_sources_data to the variables
            Dividend = other_sources_data.get('Dividend', 0)
            Unit_Trust_Of_India = other_sources_data.get('Unit_Trust_Of_India', 0)
            Dividend_u_s_2_22_e = other_sources_data.get('Dividend_u_s_2_22_e', 0)
            Interest_From_Deposits_Bank = other_sources_data.get('Interest_From_Deposits_Bank', 0)
            Interest_On_Saving_Account = other_sources_data.get('Interest_On_Saving_Account', 0)
            Post_Office = other_sources_data.get('Post_Office', 0)
            National_Savings_Certificate = other_sources_data.get('National_Savings_Certificate', 0)
            Kisan_Vikas_Patras = other_sources_data.get('Kisan_Vikas_Patras', 0)
            Debentures = other_sources_data.get('Debentures', 0)
            Interests_On_Deposits_With_Others = other_sources_data.get('Interests_On_Deposits_With_Others', 0)
            Security_Of_Central_State_Government = other_sources_data.get('Security_Of_Central_State_Government', 0)
            Interest_on_Income_Details = other_sources_data.get('Interest_on_Income_Details', 0)
            Pass_Through_Income_Details = other_sources_data.get('Pass_Through_Income_Details', 0)
            Interest_Accrued_On_Compensation_On_Enhanced_Compensation = other_sources_data.get('Interest_Accrued_On_Compensation_On_Enhanced_Compensation', 0)
            Interest_Accrued_On_Contribution_To_Provident = other_sources_data.get('Interest_Accrued_On_Contribution_To_Provident', 0)
            Income_From_Owning_And_Maintaining_Race_Horses = other_sources_data.get('Income_From_Owning_And_Maintaining_Race_Horses', 0)
            Casual_Income_Lottery = other_sources_data.get('Casual_Income_Lottery', 0)
            Casual_Income_Others = other_sources_data.get('Casual_Income_Others', 0)
            Less_Exemption_10_3 = other_sources_data.get('Less_Exemption_10_3', 0)
            Rental_Income = other_sources_data.get('Rental_Income', 0)
            Brokerage = other_sources_data.get('Brokerage', 0)
            Family_Pension = other_sources_data.get('Family_Pension', 0)
            Gift = other_sources_data.get('Gift', 0)
            Other_Income = other_sources_data.get('Other_Income', 0)
            Income_From_Retirement_Benefit_Account_US_89A = other_sources_data.get('Income_From_Retirement_Benefit_Account_US_89A', 0)
            Deduction_us_57 = other_sources_data.get('Deduction_us_57', 0)
            Income_US_58_59 = other_sources_data.get('Income_US_58_59', 0)
            Life_Insurance_Policy = other_sources_data.get('Life_Insurance_Policy', 0)
            Income_Due_To_Disallowance_Of_Exemption_Under_Clauses_Of_Section_10 = other_sources_data.get('Income_Due_To_Disallowance_Of_Exemption_Under_Clauses_Of_Section_10', 0)
            Specified_Sum_Received_By_Unit_Holder_From_Business_Trust_in_Sec_56_2_xii = other_sources_data.get('Specified_Sum_Received_By_Unit_Holder_From_Business_Trust_in_Sec_56_2_xii', 0)
            Sum_Received_Under_Life_Insurance_Policy_Sec_56_2_xii  = other_sources_data.get('Sum_Received_Under_Life_Insurance_Policy_Sec_56_2_xii', 0)

        


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

             # Compute the total other_sources with deductions
            other_sources = (
                Dividend + Unit_Trust_Of_India + Dividend_u_s_2_22_e + Interest_From_Deposits_Bank + Interest_On_Saving_Account +
                Post_Office + National_Savings_Certificate + Kisan_Vikas_Patras + Debentures + Interests_On_Deposits_With_Others +
                Security_Of_Central_State_Government + Interest_on_Income_Details + Pass_Through_Income_Details +
                Interest_Accrued_On_Compensation_On_Enhanced_Compensation + Interest_Accrued_On_Contribution_To_Provident +
                Income_From_Owning_And_Maintaining_Race_Horses + Casual_Income_Lottery + Casual_Income_Others + Less_Exemption_10_3 +
                Rental_Income + Brokerage + Family_Pension + Gift + Other_Income + Income_From_Retirement_Benefit_Account_US_89A +
                Income_US_58_59 + Life_Insurance_Policy + Income_Due_To_Disallowance_Of_Exemption_Under_Clauses_Of_Section_10 +
                Specified_Sum_Received_By_Unit_Holder_From_Business_Trust_in_Sec_56_2_xii + Sum_Received_Under_Life_Insurance_Policy_Sec_56_2_xii -
                Deduction_us_57
            )


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
