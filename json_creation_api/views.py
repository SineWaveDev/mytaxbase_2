from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json
import os

class GenerateJSONView(APIView):
    def post(self, request, format=None):
      
            # Extract data directly from the request
            data = request.data

            # Validate required fields (this can be expanded as necessary)
            required_fields = [
                    'SWVersionNo', 'SWCreatedBy', 'JSONCreatedBy', 'JSONCreationDate', 
                    'IntermediaryCity', 'Digest', 'FormName', 'Description', 'AssessmentYear', 
                    'SchemaVer', 'FormVer', 'FirstName', 'SurNameOrOrgName', 'ResidenceNo', 
                    'ResidenceName', 'RoadOrStreet', 'LocalityOrArea', 'CityOrTownOrDistrict', 
                    'StateCode', 'CountryCode', 'PinCode', 'CountryCodeMobile', 'MobileNo', 
                    'EmailAddress', 'PAN', 'DOB', 'EmployerCategory', 'AadhaarCardNo', 'UsrDeductUndChapVIA',
                    'ReturnFileSec', 'OptOutNewTaxRegime', 'SeventhProvisio139', 'clauseiv7provisio139i', 
                    'ItrFilingDueDate', 'GrossSalary', 'Salary', 'PerquisitesValue', 'ProfitsInSalary', 
                    'IncomeNotified89A', 'IncomeNotified89AType', 'IncomeNotifiedOther89A', 'Increliefus89A', 
                    'NetSalary', 'DeductionUs16', 'DeductionUs16ia', 'EntertainmentAlw16ii', 
                    'ProfessionalTaxUs16iii', 'IncomeFromSal', 'GrossRentReceived', 'TaxPaidlocalAuth', 
                    'AnnualValue', 'StandardDeduction', 'InterestPayable', 'ArrearsUnrealizedRentRcvd', 
                    'TotalIncomeOfHP', 'IncomeOthSrc', 'OthersIncDtlsOthSrc', 'OthSrcNatureDesc', 
                    'OthSrcOthNatOfInc', 'DividendInc', 'DeductionUs57iia', 'Increliefus89AOS', 
                    'GrossTotIncome', 'Section80C', 'Section80CCC', 'Section80CCDEmployeeOrSE', 'Section80CCD1B', 
                    'Section80CCDEmployer', 'Section80D', 'Section80DD', 'Section80DDB', 'Section80E', 'Section80EE', 
                    'Section80EEA', 'Section80EEB', 'Section80G', 'Section80GG', 'Section80GGA', 'Section80GGC', 
                    'Section80U', 'Section80TTA', 'Section80TTB', 'AnyOthSec80CCH', 'TotalChapVIADeductions', 
                    'TotalIncome', 'ExemptIncAgriOthUs10Dtls', 'ExemptIncAgriOthUs10Total', 'TotalTaxPayable', 
                    'Rebate87A', 'TaxPayableOnRebate', 'EducationCess', 'GrossTaxLiability', 'Section89', 
                    'NetTaxLiability', 'TotalIntrstPay', 'IntrstPayUs234A', 'IntrstPayUs234B', 'IntrstPayUs234C', 
                    'LateFilingFee234F', 'TotTaxPlusIntrstPay', 'AdvanceTax', 'TDS', 'TCS', 'SelfAssessmentTax', 'Up16Of3To31Of3_DIV',
                    'TotalTaxesPaid', 'BalTaxPayable', 'RefundDue', 'IFSCCode', 'BankName', 'Upto15Of6_DIV', 'Upto15Of9_DIV',
                    'BankAccountNo', 'AccountType', 'SeniorCitizenFlag', 'SelfAndFamily', 'HealthInsPremSlfFam', 'Up16Of12To15Of3_DIV',
                    'PrevHlthChckUpSlfFam', 'SelfAndFamilySeniorCitizen', 'HlthInsPremSlfFamSrCtzn', 'OthSrcOthAmount_DIV',
                    'PrevHlthChckUpSlfFamSrCtzn', 'MedicalExpSlfFamSrCtzn', 'ParentsSeniorCitizenFlag', 'Parents', 'Up16Of9To15Of12_DIV',
                    'HlthInsPremParents', 'PrevHlthChckUpParents', 'ParentsSeniorCitizen', 'HlthInsPremParentsSrCtzn', 'Up16Of3To31Of3_IFD',
                    'PrevHlthChckUpParentsSrCtzn', 'MedicalExpParentsSrCtzn', 'EligibleAmountOfDedn', 'Up16Of12To15Of3_IFD', 'DeductUndChapVIA',
                    'TotalTDSonSalaries', 'TotalTDSonOthThanSals', 'TotalTDS3Details', 'TotalTaxPayments', 'Up16Of9To15Of12_IFD', 
                    'AssesseeVerName', 'FatherName', 'AssesseeVerPAN', 'Capacity', 'Place', 'OthSrcOthAmount_IFD', 'Upto15Of6_IFD', 'Upto15Of9_IFD'
                ]

            
            for field in required_fields:
                if field not in data:
                    return Response({f"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Predefined JSON structure with dynamic values
            json_structure = {
                "ITR": {
                    "ITR1": {
                        "CreationInfo": {
                            "SWVersionNo": data['SWVersionNo'],
                            "SWCreatedBy": data['SWCreatedBy'],
                            "JSONCreatedBy": data['JSONCreatedBy'],
                            "JSONCreationDate": data['JSONCreationDate'],
                            "IntermediaryCity": data['IntermediaryCity'],
                            "Digest": data['Digest']
                        },
                        "Form_ITR1": {
                            "FormName": data['FormName'],
                            "Description": data['Description'],
                            "AssessmentYear": data['AssessmentYear'],
                            "SchemaVer": data['SchemaVer'],
                            "FormVer": data['FormVer']
                        },
                        "PersonalInfo": {
                            "AssesseeName": {
                                "FirstName": data['FirstName'],
                                "SurNameOrOrgName": data['SurNameOrOrgName']
                            },
                            "Address": {
                                "ResidenceNo": data['ResidenceNo'],
                                "ResidenceName": data['ResidenceName'],
                                "RoadOrStreet": data['RoadOrStreet'],
                                "LocalityOrArea": data['LocalityOrArea'],
                                "CityOrTownOrDistrict": data['CityOrTownOrDistrict'],
                                "StateCode": data['StateCode'],
                                "CountryCode": data['CountryCode'],
                                "PinCode": data['PinCode'],
                                "CountryCodeMobile": data['CountryCodeMobile'],
                                "MobileNo": data['MobileNo'],
                                "EmailAddress": data['EmailAddress']
                            },
                            "PAN": data['PAN'],
                            "DOB": data['DOB'],
                            "EmployerCategory": data['EmployerCategory'],
                            "AadhaarCardNo": data['AadhaarCardNo']
                        },
                        "FilingStatus": {
                            "ReturnFileSec": data['ReturnFileSec'],
                            "OptOutNewTaxRegime": data['OptOutNewTaxRegime'],
                            "SeventhProvisio139": data['SeventhProvisio139'],
                            "clauseiv7provisio139i": data['clauseiv7provisio139i'],
                            "ItrFilingDueDate": data['ItrFilingDueDate']
                        },
                        "ITR1_IncomeDeductions": {
                            "GrossSalary": data['GrossSalary'],
                            "Salary": data['Salary'],
                            "PerquisitesValue": data['PerquisitesValue'],
                            "ProfitsInSalary": data['ProfitsInSalary'],
                            "IncomeNotified89A": data['IncomeNotified89A'],
                            "IncomeNotified89AType": data['IncomeNotified89AType'],
                            "IncomeNotifiedOther89A": data['IncomeNotifiedOther89A'],
                            "Increliefus89A": data['Increliefus89A'],
                            "NetSalary": data['NetSalary'],
                            "DeductionUs16": data['DeductionUs16'],
                            "DeductionUs16ia": data['DeductionUs16ia'],
                            "EntertainmentAlw16ii": data['EntertainmentAlw16ii'],
                            "IncomeFromSal": data['IncomeFromSal'],
                            "GrossRentReceived": data['GrossRentReceived'],
                            "TaxPaidlocalAuth": data['TaxPaidlocalAuth'],
                            "AnnualValue": data['AnnualValue'],
                            "StandardDeduction": data['StandardDeduction'],
                            "InterestPayable": data['InterestPayable'],
                            "ArrearsUnrealizedRentRcvd": data['ArrearsUnrealizedRentRcvd'],
                            "TotalIncomeOfHP": data['TotalIncomeOfHP'],
                            "IncomeOthSrc": data['IncomeOthSrc'],
                            "OthersInc": {
                                "OthersIncDtlsOthSrc": [
                                    {
                                        "OthSrcNatureDesc": "IFD",
                                        "OthSrcOthNatOfInc": "Interest from Deposit(Bank/Post Office/Cooperative Society)",
                                        "OthSrcOthAmount": data['OthSrcOthAmount_IFD'],
                                        "DividendInc": {
                                            "DateRange": {
                                                "Upto15Of6": data['Upto15Of6_IFD'],
                                                "Upto15Of9": data['Upto15Of9_IFD'],
                                                "Up16Of9To15Of12": data['Up16Of9To15Of12_IFD'],
                                                "Up16Of12To15Of3": data['Up16Of12To15Of3_IFD'],
                                                "Up16Of3To31Of3": data['Up16Of3To31Of3_IFD']
                                            }
                                        }
                                    },
                                    {
                                        "OthSrcNatureDesc": "DIV",
                                        "OthSrcOthNatOfInc": "Dividend",
                                        "OthSrcOthAmount": data['OthSrcOthAmount_DIV'],
                                        "DividendInc": {
                                            "DateRange": {
                                                "Upto15Of6": data['Upto15Of6_DIV'],
                                                "Upto15Of9": data['Upto15Of9_DIV'],
                                                "Up16Of9To15Of12": data['Up16Of9To15Of12_DIV'],
                                                "Up16Of12To15Of3": data['Up16Of12To15Of3_DIV'],
                                                "Up16Of3To31Of3": data['Up16Of3To31Of3_DIV']
                                            }
                                        }
                                    }
                                ]
                            },
                            "DeductionUs57iia": data['DeductionUs57iia'],
                            "Increliefus89AOS": data['Increliefus89AOS'],
                            "GrossTotIncome": data['GrossTotIncome'],
                            "UsrDeductUndChapVIA": data['UsrDeductUndChapVIA'],
                            "DeductUndChapVIA": data['DeductUndChapVIA'],
                            "TotalIncome": data['TotalIncome'],
                            "ExemptIncAgriOthUs10": {
                                "ExemptIncAgriOthUs10Dtls": data['ExemptIncAgriOthUs10Dtls'],
                                "ExemptIncAgriOthUs10Total": data['ExemptIncAgriOthUs10Total']
                            }
                        },
                        "ITR1_TaxComputation": {
                            "TotalTaxPayable": data['TotalTaxPayable'],
                            "Rebate87A": data['Rebate87A'],
                            "TaxPayableOnRebate": data['TaxPayableOnRebate'],
                            "EducationCess": data['EducationCess'],
                            "GrossTaxLiability": data['GrossTaxLiability'],
                            "Section89": data['Section89'],
                            "NetTaxLiability": data['NetTaxLiability'],
                            "TotalIntrstPay": data['TotalIntrstPay'],
                            "IntrstPay": {
                                "IntrstPayUs234A": data['IntrstPayUs234A'],
                                "IntrstPayUs234B": data['IntrstPayUs234B'],
                                "IntrstPayUs234C": data['IntrstPayUs234C'],
                                "LateFilingFee234F": data['LateFilingFee234F']
                            },
                            "TotTaxPlusIntrstPay": data['TotTaxPlusIntrstPay']
                        },
                        "TaxPaid": {
                            "TaxesPaid": {
                                "AdvanceTax": data['AdvanceTax'],
                                "TDS": data['TDS'],
                                "TCS": data['TCS'],
                                "SelfAssessmentTax": data['SelfAssessmentTax'],
                                "TotalTaxesPaid": data['TotalTaxesPaid']
                            },
                            "BalTaxPayable": data['BalTaxPayable']
                        },
                        "Refund": {
                            "RefundDue": data['RefundDue'],
                            "BankAccountDtls": {
                                "AddtnlBankDetails": [
                                    {
                                        "IFSCCode": data['IFSCCode'],
                                        "BankName": data['BankName'],
                                        "BankAccountNo": data['BankAccountNo'],
                                        "AccountType": data['AccountType']
                                    }
                                ]
                            }
                        },
                        "Schedule80D": {
                            "Sec80DSelfFamSrCtznHealth": {
                                "SeniorCitizenFlag": data['SeniorCitizenFlag'],
                                "SelfAndFamily": data['SelfAndFamily'],
                                "HealthInsPremSlfFam": data['HealthInsPremSlfFam'],
                                "PrevHlthChckUpSlfFam": data['PrevHlthChckUpSlfFam'],
                                "SelfAndFamilySeniorCitizen": data['SelfAndFamilySeniorCitizen'],
                                "HlthInsPremSlfFamSrCtzn": data['HlthInsPremSlfFamSrCtzn'],
                                "PrevHlthChckUpSlfFamSrCtzn": data['PrevHlthChckUpSlfFamSrCtzn'],
                                "MedicalExpSlfFamSrCtzn": data['MedicalExpSlfFamSrCtzn'],
                                "ParentsSeniorCitizenFlag": data['ParentsSeniorCitizenFlag'],
                                "Parents": data['Parents'],
                                "HlthInsPremParents": data['HlthInsPremParents'],
                                "PrevHlthChckUpParents": data['PrevHlthChckUpParents'],
                                "ParentsSeniorCitizen": data['ParentsSeniorCitizen'],
                                "HlthInsPremParentsSrCtzn": data['HlthInsPremParentsSrCtzn'],
                                "PrevHlthChckUpParentsSrCtzn": data['PrevHlthChckUpParentsSrCtzn'],
                                "MedicalExpParentsSrCtzn": data['MedicalExpParentsSrCtzn'],
                                "EligibleAmountOfDedn": data['EligibleAmountOfDedn']
                            }
                        },
                        "TDSonSalaries": {
                            "TotalTDSonSalaries": data['TotalTDSonSalaries']
                        },
                        "TDSonOthThanSals": {
                            "TotalTDSonOthThanSals": data['TotalTDSonOthThanSals']
                        },
                        "ScheduleTDS3Dtls": {
                            "TotalTDS3Details": data['TotalTDS3Details']
                        },
                        "TaxPayments": {
                            "TotalTaxPayments": data['TotalTaxPayments']
                        },
                        "Verification": {
                            "Declaration": {
                                "AssesseeVerName": data['AssesseeVerName'],
                                "FatherName": data['FatherName'],
                                "AssesseeVerPAN": data['AssesseeVerPAN']
                            },
                            "Capacity": data['Capacity'],
                            "Place": data['Place']
                        }
                    }
                }
            }

            output_filename = 'processed_data.json'
            with open(output_filename, 'w') as json_file:
                json.dump(json_structure, json_file, indent=4)

            response = JsonResponse(json_structure, safe=False)
            response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
            return response

 