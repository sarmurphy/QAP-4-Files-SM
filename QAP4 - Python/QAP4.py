# Description: A program for One Stop Insurance Company to calculate new insurance policy information for its customers.
# Author: Sarah Murphy
# Date: July 16, 2024 - July 21, 2024

# Required libraries.
import datetime
import time
import sys


# Program constants.
f = open('Const.dat', 'r')
POLICY_NUM = int(f.readline())
BASIC_RATE = float(f.readline())
ADD_CAR_DISC = float(f.readline())
EXTRA_LIABILITY = float(f.readline())
GLASS_COVER = float(f.readline())
LOANER_CAR_FEE = float(f.readline())
HST_RATE = float(f.readline())
PROCESS_FEE = float(f.readline())
f.close()


# Program functions.
def ProgressBar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    # Function for Progress Bar.
 
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

def PostCodeVal(PostCode):
    # Function to validate the customer's postal code.
    CodeNum = PostCode[1] + PostCode[3] + PostCode[5]
    CodeNum = CodeNum.isdigit()
    CodeChar = PostCode[0] + PostCode[2] + PostCode[4]
    CodeChar = CodeChar.isalpha()
    CodeVal = False

    if CodeNum == False:
        print("Data Entry Error: Postal Code must contain numbers in positions 2, 4, and 6. Please try again.")
    elif CodeChar == False:
        print("Data Entry Error: Postal Code must contain letters in positions 1, 3, and 5. Please try again.")
    else:
        CodeVal = True

    return CodeVal

def FormatAddress(Street, City, Province, PostalCode):
    # Function to format the customer's address.
    return f"{Street}\n {City}, {Province}, {PostalCode}"


# Main program starts here.
while True:


    # User inputs.
    CustFirst = input("Enter the customer's first name: ").title()
    CustLast = input("Enter the customer's last name: ").title()
    CustStAdd = input("Enter the customer's street address: ").title()
    CustCity = input("Enter the customer's city: ").title()

    CustProvLst = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
    while True:
        CustProv = input("Enter the customer's province (XX): ").upper()
        if CustProv == "":
            print("Data Entry Error: This field cannot be blank. Please try again.")
        elif len(CustProv) != 2:
            print("Data Entry Error: Province field is a 2 character code. Please try again.")
        elif CustProv not in CustProvLst:
            print("Data Entry Error: Not a valid province. Please try again.")
        else:
            break

    while True:        
        CustPostCode = input("Please enter the customer's 6 character postal code: ").upper()
        if PostCodeVal(CustPostCode):
            break
      
    CustPhone = input("Please enter the customer's 10 digit phone number: ")
    InsuredCars = input("Please enter the number of cars being insured: ")
    InsuredCars = int(InsuredCars)
    ExtraLiability = input("Would the customer like to add extra liability up to $1,000,000? (Y / N): ").upper()
    GlassCover = input("Would the customer like to add optional glass coverage? (Y / N): ").upper()
    CarLoan = input("Would the customer like an optional loaner vehicle? (Y / N): ").upper()

    PayPlanLst = ["Full", "Monthly", "Down Pay"]
    while True:
        PayPlan = input("Please enter the customer's payment plan: Full, Monthly, or Down Pay: ").title()
        if PayPlan == "":
            print("Data Entry Error: This field cannot be blank. Please try again.")
        elif PayPlan not in PayPlanLst:
            print("Data Entry Error: Not a valid payment plan option. Please try again.")
        else:
            break

    DownPayAmt = 0
    if PayPlan == "Down Pay":
        while True:
            try:
                DownPayAmt = input("Down Pay selected. Please enter the amount of the down payment: ")
                DownPayAmt = float(DownPayAmt)
            except:
                print("Data Entry Error: Down payment amount must be numerical. Please try again.")
            else:
                break
    
    ClaimNumLst = []
    ClaimDateLst = []
    ClaimAmtLst = []

    f = open('PastClaims.dat', 'r')
    for i in f:
        PrevClaims = i.split(',')
        ClaimNumLst.append(PrevClaims[0].strip())
        ClaimDateLst.append(PrevClaims[1].strip())
        ClaimAmtLst.append(PrevClaims[2].strip())
    f.close()


    # Required calculations.
    InsPremium = BASIC_RATE + (InsuredCars - 1) * BASIC_RATE * (1 - ADD_CAR_DISC)

    LiabilityCost = 0
    if ExtraLiability == "Y":
        LiabilityCost = EXTRA_LIABILITY * InsuredCars
    if ExtraLiability == "Y":
        ExtraLiabilityDsp = "Yes"
    else:
        ExtraLiabilityDsp = "No"

    GlassCost = 0
    if GlassCover == "Y":
        GlassCost = GLASS_COVER * InsuredCars
    if GlassCover == "Y":
        GlassCoverDsp = "Yes"
    else:
        GlassCoverDsp = "No"

    LoanerCost = 0
    if CarLoan == "Y":
        LoanerCost = LOANER_CAR_FEE * InsuredCars
    if CarLoan == "Y":
        CarLoanDsp = "Yes"
    else:
        CarLoanDsp = "No"

    TotalExtraCosts = LiabilityCost + GlassCost + LoanerCost
    TotalInsPremium = InsPremium + TotalExtraCosts
    Tax = TotalInsPremium * HST_RATE
    TotalCost = TotalInsPremium + Tax

    if PayPlan != "Full":
        MonthlyPay = (PROCESS_FEE + TotalCost - DownPayAmt) / 8
        MonthlyPayDsp = "${:,.2f}".format(MonthlyPay)
    else:
        MonthlyPayDsp = "N/A"

    if DownPayAmt == 0:
        DownPayAmtDsp = "N/A"
    else:
        DownPayAmtDsp = "${:,.2f}".format(DownPayAmt)

    CurrDate = datetime.datetime.today()
    if CurrDate.month == "12":
        FirstPayYear = int(CurrDate.year) + 1
        FirstPayMonth = 1
    else:
        FirstPayYear = int(CurrDate.year)
        FirstPayMonth = int(CurrDate.month) + 1

    FirstPayDate = datetime.datetime(FirstPayYear, FirstPayMonth, 1)

    CustAddress = FormatAddress(CustStAdd, CustCity, CustProv, CustPostCode)


    # Displayed results.
    print()
 
    TotalIterations = 30 # The more iterations, the more time is takes.
    Message = "Saving New Claim Data ..."
 
    for i in range(TotalIterations + 1):
        time.sleep(0.1)  # Simulate some work
        ProgressBar(i, TotalIterations, prefix=Message, suffix='Complete', length=50)
 
    print()
    print()
    print(f"           ONE STOP INSURANCE")
    print(f"            CUSTOMER RECEIPT")
    print(f"----------------------------------------")
    print()
    print(f" Invoice Date:{CurrDate.strftime("%B %d, %Y"):>14}")
    print(f" Policy No. {str(POLICY_NUM):<5s}")
    print()
    print(f" Customer Name: {(CustFirst + ' ' + CustLast):<20s}")
    print(f" Home Address: {CustAddress}")
    CustPhoneDsp = "(" + CustPhone[0:3] + ")" + " " + CustPhone[3:6] + "-" + CustPhone[6:]
    print(f" Phone Number: {CustPhoneDsp:<12s}")
    print()
    print(f"----------------------------------------")
    print()
    print(f" Extras:")
    print()
    print(f" Liability up to $1,000,000:        {ExtraLiabilityDsp:>3s}")
    print(f" Glass coverage:                    {GlassCoverDsp:>3s}")
    print(f" Loaner car coverage:               {CarLoanDsp:>3s}")
    print()
    print(f"----------------------------------------")
    print()
    print(f" Extra Charges:")
    print()
    
    LiabilityCostDsp = "${:,.2f}".format(LiabilityCost)
    print(f" Extra Liability:            {LiabilityCostDsp:>10s}")
    GlassCostDsp = "${:,.2f}".format(GlassCost)
    print(f" Glass Coverage:             {GlassCostDsp:>10s}")
    LoanerCostDsp = "${:,.2f}".format(LoanerCost)
    print(f" Loaner Car Charge:          {LoanerCostDsp:>10s}")
    print(f"                             ----------")
    TotalExtraCostsDsp = "${:,.2f}".format(TotalExtraCosts)
    print(f" Total for Extra Charges:    {TotalExtraCostsDsp:>10s}")
    print()
    InsPremiumDsp = "${:,.2f}".format(InsPremium)
    print(f" Insurance Premium:          {InsPremiumDsp:>10s}")
    TotalInsPremiumDsp = "${:,.2f}".format(TotalInsPremium)
    print(f" Total Insurance Premium:    {TotalInsPremiumDsp:>10s}")
    TaxDsp = "${:,.2f}".format(Tax)
    print(f" HST:                        {TaxDsp:>10s}")
    print(f"                             ----------")
    TotalCostDsp = "${:,.2f}".format(TotalCost)
    print(f" Total Cost:                 {TotalCostDsp:>10s}")
    print()
    DownPayAmtDsp = "${:,.2f}".format(DownPayAmt)
    print(f" Down Payment Amount:        {DownPayAmtDsp:>10s}")
    print(f" Monthly Payment:            {MonthlyPayDsp:>10s}")
    print()
    print(f"----------------------------------------")
    print(f" Date of First Payment: {FirstPayDate.strftime("%B %d, %Y"):>14}")
    print(f"----------------------------------------")
    print(f"----------------------------------------")
    print(f" Claim #        Claim Date       Amount")
    print(f"----------------------------------------")
    for i in range(len(ClaimAmtLst)):
        print(f" {ClaimNumLst[i]:>5s}          {ClaimDateLst[i]:>10s}   {ClaimAmtLst[i]:>10s}")
    print()


    # Write processed data to a file for future use.
    f = open('PolicyInfo.dat', 'a')
    f.write('{},'.format(POLICY_NUM))
    f.write('{},'.format(CustFirst))
    f.write('{},'.format(CustLast))
    f.write('{},'.format(CustStAdd))
    f.write('{},'.format(CustCity))
    f.write('{},'.format(CustProv))
    f.write('{},'.format(CustPostCode))
    f.write('{},'.format(CustPhone))
    f.write('{},'.format(InsuredCars))
    f.write('{},'.format(ExtraLiability))
    f.write('{},'.format(GlassCover))
    f.write('{},'.format(CarLoan))
    f.write('{},'.format(PayPlan))
    f.write('{},'.format(DownPayAmtDsp))
    f.write('{}\n'.format(TotalInsPremiumDsp))
    f.close()

    POLICY_NUM += 1


    # Loop to continue program.
    while True:
        ProgramLoop = input("Do you wish to add an additional customer? (Y / N): ").upper()
        if ProgramLoop == "N":
            print("Thank you! Have a great day.")
            break
        elif ProgramLoop == "Y":
            break
 
    if ProgramLoop == "N":
        break


    # Housekeeping duties.

    # Open Const.dat file to continue adding to the policy number.
    f = open('Const.dat', 'w')
    f.write('{}\n'.format(POLICY_NUM))
    f.write('{}\n'.format(BASIC_RATE))
    f.write('{}\n'.format(ADD_CAR_DISC))
    f.write('{}\n'.format(EXTRA_LIABILITY))
    f.write('{}\n'.format(GLASS_COVER))
    f.write('{}\n'.format(LOANER_CAR_FEE))
    f.write('{}\n'.format(HST_RATE))
    f.write('{}\n'.format(PROCESS_FEE))
    f.close()