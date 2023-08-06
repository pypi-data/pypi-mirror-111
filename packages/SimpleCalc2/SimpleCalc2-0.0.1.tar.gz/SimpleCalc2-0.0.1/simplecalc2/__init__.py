import math
def c_2(angle, hyp):
        angle_a = float(angle)
        hyp = float(hyp)
        while angle_a > 90:
            angle_a = angle_a - 90
        c_1 = round(math.sin(math.radians(angle_a)) * hyp, 4)
        return c_1

def c_1(angle, hyp):
        angle_a = float(angle)
        hyp = float(hyp)
        while angle_a > 90:
            angle_a = angle_a - 90
        c_2 = round(math.cos(math.radians(angle_a)) * hyp, 4)
        return c_2

def area(angle, hyp):
        angle_a = float(angle)
        hyp = float(hyp)
        while angle_a > 90:
            angle_a = angle_a - 90
        c_1 = round(math.sin(math.radians(angle_a)) * hyp, 4)
        c_2 = round(math.cos(math.radians(angle_a)) * hyp, 4)
        area = round(c_1 * c_2 * 0.5, 4)
        return area