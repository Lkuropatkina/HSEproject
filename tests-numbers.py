from DraftParser import parse

if __name__ == '__main__':
    EPS = 0.0000001
    assert abs(parse("3+7*(83-75)/7+(-5)").compute - 6) < EPS
    assert abs(parse("45*pi/e+2").compute - 54.00773074059) < EPS
    assert abs(parse("sin(\pi/2)/cos(pi/3)").compute - 2) < EPS
    assert abs(parse("sin(0) + tg(pi/3) + arccos(sqrt(3/4))").compute - 2.25564958316) < EPS
    assert abs(parse("log(e^arcsin(1))").compute - 1.57079632679) < EPS
    assert abs(parse("lg(\e^tan(sqrt(pi)))").compute - 1.77245385090) < EPS
    assert abs(parse("ctg(pi/3)*cot(pi/6)/cot(7*e/4)").compute - (-22.40453361252)) < EPS
    assert abs(parse("arcsin[-0.5]*{3-pi}").compute - 0.07413774005) < EPS
    assert abs(parse("acos{-0.78}/(76-5*[4+11])").compute - 2.46546214402) < EPS
    assert abs(parse("asin(e/\pi)+arctg(5)").compute - 2.41906151418) < EPS
    assert abs(parse("atg2-atan[5]").compute - (-0.26625204915)) < EPS
    assert abs(parse("7.8-e*ln(2)").compute - 5.91583061463) < EPS
    assert abs(parse("ln(2)").compute - 0.69314718055) < EPS
    assert abs(parse("lg{7*sin(45)}/5*arctan8").compute - 0.20093472417) < EPS
    assert abs(parse("2+3*4^3*5+2^7*3").compute - 1346) < EPS
    assert abs(parse("2*3/5*7/9").compute - 0.93333333333) < EPS
    print("OK")
