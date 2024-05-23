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
                'first_name', 'surname', 'email', 'gross_salary', 'salary', 'perquisites_value', 
                'profits_in_salary', 'income_notified_89A', 'income_notified_89A_type', 
                'income_notified_other_89A', 'increliefus_89A', 'net_salary', 'deduction_us_16', 
                'deduction_us_16ia', 'entertainment_alw_16ii'
            ]
            
            for field in required_fields:
                if field not in data:
                    return Response({f"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Predefined JSON structure with dynamic values
            json_structure = {
                "ITR": {
                    "ITR1": {
                        "CreationInfo": {
                            "SWVersionNo": "P1.43.2.3",
                            "SWCreatedBy": "SW20000053",
                            "JSONCreatedBy": "SW20000053",
                            "JSONCreationDate": "2024-04-03",
                            "IntermediaryCity": "Pune",
                            "Digest": "8atsmLhD0VTb11QhPl9aNSxU2fz+I4V/zcP4lAod86c="
                        },
                        "Form_ITR1": {
                            "FormName": "ITR-1",
                            "Description": "For Indls having Income from Salary, Pension, family pension and Interest",
                            "AssessmentYear": "2024",
                            "SchemaVer": "Ver1.0",
                            "FormVer": "Ver1.0"
                        },
                        "PersonalInfo": {
                            "AssesseeName": {
                                "FirstName": data['first_name'],
                                "SurNameOrOrgName": data['surname']
                            },
                            "Address": {
                                "ResidenceNo": "T 22",
                                "ResidenceName": "3RD FLOOR",
                                "RoadOrStreet": "SUPER MALL",
                                "LocalityOrArea": "WANOWRIE",
                                "CityOrTownOrDistrict": "PUNE",
                                "StateCode": "19",
                                "CountryCode": "91",
                                "PinCode": 411040,
                                "CountryCodeMobile": 91,
                                "MobileNo": 9880123456,
                                "EmailAddress": data['email']
                            },
                            "PAN": "SINPT2024A",
                            "DOB": "1995-01-01",
                            "EmployerCategory": "OTH",
                            "AadhaarCardNo": "293277010339"
                        },
                        "FilingStatus": {
                            "ReturnFileSec": 11,
                            "OptOutNewTaxRegime": "N",
                            "SeventhProvisio139": "N",
                            "clauseiv7provisio139i": "N",
                            "ItrFilingDueDate": "2024-07-31"
                        },
                        "ITR1_IncomeDeductions": {
                            "GrossSalary": data['gross_salary'],
                            "Salary": data['salary'],
                            "PerquisitesValue": data['perquisites_value'],
                            "ProfitsInSalary": data['profits_in_salary'],
                            "IncomeNotified89A": data['income_notified_89A'],
                            "IncomeNotified89AType": data['income_notified_89A_type'],
                            "IncomeNotifiedOther89A": data['income_notified_other_89A'],
                            "Increliefus89A": data['increliefus_89A'],
                            "NetSalary": data['net_salary'],
                            "DeductionUs16": data['deduction_us_16'],
                            "DeductionUs16ia": data['deduction_us_16ia'],
                            "EntertainmentAlw16ii": data['entertainment_alw_16ii'],
                            "IncomeFromSal": data['net_salary'] - data['deduction_us_16'],  # Example calculation
                            "GrossRentReceived": 0,
                            "TaxPaidlocalAuth": 0,
                            "AnnualValue": 0,
                            "StandardDeduction": 0,
                            "InterestPayable": 0,
                            "ArrearsUnrealizedRentRcvd": 0,
                            "TotalIncomeOfHP": 0,
                            "IncomeOthSrc": 10000,
                            "OthersInc": {
                                "OthersIncDtlsOthSrc": [
                                    {
                                        "OthSrcNatureDesc": "IFD",
                                        "OthSrcOthNatOfInc": "Interest from Deposit(Bank/Post Office/Cooperative Society)",
                                        "OthSrcOthAmount": 10000,
                                        "DividendInc": {
                                            "DateRange": {
                                                "Upto15Of6": 0,
                                                "Upto15Of9": 0,
                                                "Up16Of9To15Of12": 0,
                                                "Up16Of12To15Of3": 0,
                                                "Up16Of3To31Of3": 0
                                            }
                                        }
                                    },
                                    {
                                        "OthSrcNatureDesc": "DIV",
                                        "OthSrcOthNatOfInc": "Dividend",
                                        "OthSrcOthAmount": 0,
                                        "DividendInc": {
                                            "DateRange": {
                                                "Upto15Of6": 0,
                                                "Upto15Of9": 0,
                                                "Up16Of9To15Of12": 0,
                                                "Up16Of12To15Of3": 0,
                                                "Up16Of3To31Of3": 0
                                            }
                                        }
                                    }
                                ]
                            },
                            "DeductionUs57iia": 0,
                            "Increliefus89AOS": 0,
                            "GrossTotIncome": 160000,
                            "UsrDeductUndChapVIA": {
                                "Section80C": 0,
                                "Section80CCC": 0,
                                "Section80CCDEmployeeOrSE": 0,
                                "Section80CCD1B": 0,
                                "Section80CCDEmployer": 0,
                                "Section80D": 0,
                                "Section80DD": 0,
                                "Section80DDB": 0,
                                "Section80E": 0,
                                "Section80EE": 0,
                                "Section80EEA": 0,
                                "Section80EEB": 0,
                                "Section80G": 0,
                                "Section80GG": 0,
                                "Section80GGA": 0,
                                "Section80GGC": 0,
                                "Section80U": 0,
                                "Section80TTA": 0,
                                "Section80TTB": 0,
                                "AnyOthSec80CCH": 0,
                                "TotalChapVIADeductions": 0
                            },
                            "DeductUndChapVIA": {
                                "Section80C": 0,
                                "Section80CCC": 0,
                                "Section80CCDEmployeeOrSE": 0,
                                "Section80CCD1B": 0,
                                "Section80CCDEmployer": 0,
                                "Section80D": 0,
                                "Section80DD": 0,
                                "Section80DDB": 0,
                                "Section80E": 0,
                                "Section80EE": 0,
                                "Section80EEA": 0,
                                "Section80EEB": 0,
                                "Section80G": 0,
                                "Section80GG": 0,
                                "Section80GGA": 0,
                                "Section80GGC": 0,
                                "Section80U": 0,
                                "Section80TTA": 0,
                                "Section80TTB": 0,
                                "AnyOthSec80CCH": 0,
                                "TotalChapVIADeductions": 0
                            },
                            "TotalIncome": 160000,
                            "ExemptIncAgriOthUs10": {
                                "ExemptIncAgriOthUs10Dtls": [],
                                "ExemptIncAgriOthUs10Total": 0
                            }
                        },
                        "ITR1_TaxComputation": {
                            "TotalTaxPayable": 0,
                            "Rebate87A": 0,
                            "TaxPayableOnRebate": 0,
                            "EducationCess": 0,
                            "GrossTaxLiability": 0,
                            "Section89": 0,
                            "NetTaxLiability": 0,
                            "TotalIntrstPay": 0,
                            "IntrstPay": {
                                "IntrstPayUs234A": 0,
                                "IntrstPayUs234B": 0,
                                "IntrstPayUs234C": 0,
                                "LateFilingFee234F": 0
                            },
                            "TotTaxPlusIntrstPay": 0
                        },
                        "TaxPaid": {
                            "TaxesPaid": {
                                "AdvanceTax": 0,
                                "TDS": 0,
                                "TCS": 0,
                                "SelfAssessmentTax": 0,
                                "TotalTaxesPaid": 0
                            },
                            "BalTaxPayable": 0
                        },
                        "Refund": {
                            "RefundDue": 0,
                            "BankAccountDtls": {
                                "AddtnlBankDetails": [
                                    {
                                        "IFSCCode": "SBIN0000001",
                                        "BankName": "State Bank of India",
                                        "BankAccountNo": "55555222222222222222",
                                        "AccountType": "SB"
                                    }
                                ]
                            }
                        },
                        "Schedule80D": {
                            "Sec80DSelfFamSrCtznHealth": {
                                "SeniorCitizenFlag": "S",
                                "SelfAndFamily": 0,
                                "HealthInsPremSlfFam": 0,
                                "PrevHlthChckUpSlfFam": 0,
                                "SelfAndFamilySeniorCitizen": 0,
                                "HlthInsPremSlfFamSrCtzn": 0,
                                "PrevHlthChckUpSlfFamSrCtzn": 0,
                                "MedicalExpSlfFamSrCtzn": 0,
                                "ParentsSeniorCitizenFlag": "P",
                                "Parents": 0,
                                "HlthInsPremParents": 0,
                                "PrevHlthChckUpParents": 0,
                                "ParentsSeniorCitizen": 0,
                                "HlthInsPremParentsSrCtzn": 0,
                                "PrevHlthChckUpParentsSrCtzn": 0,
                                "MedicalExpParentsSrCtzn": 0,
                                "EligibleAmountOfDedn": 0
                            }
                        },
                        "TDSonSalaries": {
                            "TotalTDSonSalaries": 0
                        },
                        "TDSonOthThanSals": {
                            "TotalTDSonOthThanSals": 0
                        },
                        "ScheduleTDS3Dtls": {
                            "TotalTDS3Details": 0
                        },
                        "TaxPayments": {
                            "TotalTaxPayments": 0
                        },
                        "Verification": {
                            "Declaration": {
                                "AssesseeVerName": "Sourav Gupta",
                                "FatherName": "Gupta",
                                "AssesseeVerPAN": "SINPT2024A"
                            },
                            "Capacity": "S",
                            "Place": "PUNE"
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

 