def call_BMI(weight,height):
    BMI=height/(weight**2)
    return BMI
def nutrition(weight,height,gender):
    if gender=="F":
        tdee=1.25*(10*weight+6.25*height-5*19-161)
    else:
        tdee=1.25*(10*weight+6.25*height-5*19+5)
    carbon=tdee*0.5/4
    fat=tdee*0.25/9
    protein=tdee*0.25/4
    return round(tdee,0),round(carbon,0),round(fat,0),round(protein,0)
#依次打印推荐热量、碳水、脂肪、蛋白
print(nutrition(65,180,'M'))