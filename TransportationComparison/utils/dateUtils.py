
def transformHoursFloatIntoTime(hours):
    # Use divmod to get the quotient and remainder
    quotient, remainder = divmod(hours, 1)

    # Convert the remainder to minutes
    minutes = remainder * 60

    # Print the results
    print("Hours: ", quotient)
    print("Minutes: ", int(minutes))
    return  str(int(quotient))  +" hrs "+  str(int(minutes)) + " min"