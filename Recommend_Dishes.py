# -*- coding: utf-8 -*-

import calories
import s
import random

today_menu = s.get_todaymenu()

Dish2nur = dict()
Search_limit = [0.28, 0.32, 0.40] #每一种菜品分配的比例值

for dish in today_menu:
	tmp = list()
	tmp.append(dish)
	nur = s.get_nutrition(tmp).split(":")
	#对应如下list：0:蛋白质 1:脂肪 2:碳水化合物 3:维a 4:维b 5:维c 6:钙 7:铁 8:锌 9:膳食纤维 10:热量
	Dish2nur[dish] = nur

have_choose = set()
	
selected = s.get_selected()
for dish in selected:
	dish = dish.split('*')[0] # 分割菜名和份数
	have_choose.add(dish);
		

def Analyze_current_body_state():
	#分别表示当日推荐摄入的热量，碳水化合物，脂肪，蛋白质指数
	heat_index = carbs_index = fat_index = protein_index = 1 
	
	body_state = s.get_status()
	if(body_state): #当日选择的状态不为空
		
		#共五种状态 牙痛，胃痛，头痛，过敏，生理期
		if(body_state[0] == "牙痛"):
			#牙痛期间少摄入热量和碳水
			heat_index = 0.9
			carbs_index = 0.9
			
		elif(body_state[0] == "胃痛"):
			#胃痛期间少摄入碳水，多摄入蛋白质
			carbs_index = 0.9
			protein_index = 1.1
			
		elif(body_state[0] == "头痛"):
			#头痛期间少摄入热量和碳水
			heat_index = 0.9
			carbs_index = 0.9
			
		elif(body_state[0] == "过敏"):
			#过敏期间少摄入热量
			heat_index = 0.9
			
		elif(body_state[0] == "生理期"):
			#生理期期间少摄入热量，脂肪，多摄入蛋白质
			heat_index = 0.9
			fat_index = 0.9
			protein_index = 1.1
	
	personal_data = s.get_latest_pd()
	normal_intake_tuple = calories.nutrition(personal_data[1], personal_data[0], "F")
	# normal_intake_tuple = calories.nutrition(personal_data[1], personal_data[0], s.get_sex())
	normal_intake = list()
	for ele in normal_intake_tuple:
		normal_intake.append(ele)
	
	normal_intake[0] = normal_intake[0] * heat_index
	normal_intake[1] = normal_intake[1] * carbs_index
	normal_intake[2] = normal_intake[2] * fat_index
	normal_intake[3] = normal_intake[3] * protein_index
	return normal_intake # 0:热量 1:碳水 2:脂肪 3:蛋白
	
def check(a, b, c, d, e, f):
	if (a <= e[0] * f) + (b <= e[1] * f) + (c <= e[2] * f) + (d <= e[3] * f):
		
		if (a <= e[0] * f * 2) + (b <= e[1] * f * 2) + (c <= e[2] * f * 2) + (d <= e[3] * f * 2):
			return 2
		else:
			return 1
			
	return 0

def Recommend_lunch():
	#recommend for lunch
	normal_intake = Analyze_current_body_state()
	recommend_intake = [i * 0.45 for i in normal_intake]
	random.shuffle(today_menu)
	random.shuffle(today_menu)
	random.shuffle(today_menu)
	random.shuffle(Search_limit)
	
	lunch_list = ["米饭*1"]
	Rice = s.get_nutrition(["米饭"]).split(":")
	
	recommend_intake[0] = recommend_intake[0] - eval(Rice[10])
	recommend_intake[1] = recommend_intake[1] - eval(Rice[2])
	recommend_intake[2] = recommend_intake[2] - eval(Rice[1])
	recommend_intake[3] = recommend_intake[3] - eval(Rice[0])
	
	lunch_choose = set("米饭")
	for Cycles in range(0, 1000):
		
		for dish in today_menu:
			
			if len(lunch_list) >= 4: #默认推荐为三种菜品+主食
				break;
				
			if dish in have_choose or dish in lunch_choose:
				continue
				
			dish_heat = eval(Dish2nur[dish][10])
			dish_carbs = eval(Dish2nur[dish][2])
			dish_fat = eval(Dish2nur[dish][1])
			dish_protein = eval(Dish2nur[dish][0]) 
			
			res = check( dish_heat, dish_carbs, dish_fat, dish_protein, recommend_intake, Search_limit[len(lunch_list) - 1]);
			if res == 0:
				continue
			if res == 1: lunch_list.append("*".join([dish, string(random.randint(1,2))]))
			if res == 2: lunch_list.append("*".join([dish, "1"]))
			lunch_choose.add(dish)
				
		random.shuffle(today_menu)
		
	return lunch_list # 字符串列表，例如["馒头*1"]
	
	
def Recoomend_supper():
	#recommend for supper
	normal_intake = Analyze_current_body_state()
	recommend_intake = [i * 0.40 for i in normal_intake]
	random.shuffle(today_menu)
	random.shuffle(today_menu)
	random.shuffle(today_menu)
	random.shuffle(Search_limit)
	
	supper_list = ["米饭*1"]
	Rice = s.get_nutrition(["米饭"]).split(":")
	
	recommend_intake[0] = recommend_intake[0] - eval(Rice[10])
	recommend_intake[1] = recommend_intake[1] - eval(Rice[2])
	recommend_intake[2] = recommend_intake[2] - eval(Rice[1])
	recommend_intake[3] = recommend_intake[3] - eval(Rice[0])
	
	supper_choose = set("米饭")
	for Cycles in range(0, 1000):
		
		for dish in today_menu:
			
			if len(supper_list) >= 4: #默认推荐为三种菜品+主食
				break;
				
			if dish in have_choose or dish in supper_choose:
				continue
				
			dish_heat = eval(Dish2nur[dish][10])
			dish_carbs = eval(Dish2nur[dish][2])
			dish_fat = eval(Dish2nur[dish][1])
			dish_protein = eval(Dish2nur[dish][0]) 
			
			res = check( dish_heat, dish_carbs, dish_fat, dish_protein, recommend_intake, Search_limit[len(supper_list) - 1]);
			if res == 0:
				continue
			if res == 1: supper_list.append("*".join([dish, string(random.randint(1,2))]))
			if res == 2: supper_list.append("*".join([dish, "1"]))
			supper_choose.add(dish)
				
		random.shuffle(today_menu)
		
	return supper_list # 字符串列表，例如["馒头*1"]
	
# if __name__ == '__main__': 调试用
# 	a = Recommend_lunch()
# 	b = Recoomend_supper()
# 	print(a)
# 	print(b)
