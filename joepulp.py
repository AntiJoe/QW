# a collection of pulp functions
# Joe Allen
# December 2017


def admtpd(flow, cst):
    """Calcuates Air Dry Metric Tonnes per day from
    Flow in lpm and Consistency in percent"""
    return(1.44*flow*cst/90)


def popupmsg(msg):
    print(msg)