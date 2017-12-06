#-*- coding:utf-8 -*-
# 脚本用途：根据所有用户平均值和单个用户原始数据，得到矩阵后，算出kappa值
# 脚本使用方法：
# getMatrix.py  平均值文件 用户原始文件
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# 这个值代表忽略多少内的误差，例如0.8的话 平均分3.7 用户打分3和4都算做是一致的
baseline = 1

# 平均值文件
avg_file = sys.argv[1]
avglist = []

# 用户原始文件
#user_file = sys.argv[2]
userlist = []

# 二维矩阵
matrix = [[0 for col in range(6)] for i in range(6)]

# 数据读取到list中
def initList(avg_file, user_file):
	#print 'avg file: ' + avg_file + '; user file: ' + user_file
	# 多个一起求值的时候初始化
	global avglist
	global userlist
	avglist = []
	userlist = []
	
	for line in open(avg_file):
		line = line.strip()
		avglist.append(float(line))

	for line in open(user_file):
		line = line.strip()
		userlist.append(float(line))

# 处理平均分为标准分
def avgFormat():
	for i in range(0, len(avglist)):
		num = avglist[i]
		avglist[i] = num
		

# 输出，调试用
def printlist(listname):
	for l in listname:
		print l

# 计算矩阵
def getMatrix():
	# 多个一起求值的时候初始化
	global matrix
	matrix = [[0 for col in range(6)] for i in range(6)]
	num1 = len(avglist)
	num2 = len(userlist)
	if num1 != num2:
		print 'two list num is not same!'
		return
	for i in range(0, num1):
		x = float(avglist[i])
		y = float(userlist[i])
		
		if abs(x-y) < baseline:
			y = int(y)
			matrix[y][y] = matrix[y][y] + 1
		else:
			y = int(y)
			if x < 1.499:
				matrix[1][y] = matrix[1][y] + 1
			elif  x < 2.499:
				matrix[2][y] = matrix[2][y] + 1
			elif  x < 3.499:
				matrix[3][y] = matrix[3][y] + 1
			elif  x < 4.499:
				matrix[4][y] = matrix[4][y] + 1
			elif x > 4.499:
				matrix[5][y] = matrix[5][y] + 1
		
		

# 输出矩阵
def printmatrix():
	print '\nmatrix is:' 
	for num in range(1, 6):
		print matrix[num][1], matrix[num][2],matrix[num][3],matrix[num][4],matrix[num][5]
	print '\n'

# 得到kappa值
def getkappa():
	# 对角线之和
	dsum = 0.0
	# 总数
	allsum = float(len(avglist))
	
	# 计算对角线的和
	for i in range(1, 6):
		dsum = dsum + matrix[i][i]
	# 临时加的一句
	#dsum = dsum + matrix[1][2] + matrix[2][1] + matrix[2][3] + matrix[3][2] + matrix[3][4] + matrix[4][3] + matrix[4][5] + matrix[5][4] 
	
	#print dsum
	#print 'diagonal sum is :', dsum
	p0 = float(dsum)/allsum
	#print 'p0 is :', p0 , '\n'
	
	# 计算a1*b1+a2*b2+...ac*bc的和（a1 等于 matrix[1][x]的和  b1等于matrix[x][1]的和）
	a = 0
	al = []
	b = 0
	bl = []
	for j in range(1, 6):
		a = 0
		b = 0
		for k in range(1, 6):
			a = a + matrix[j][k]
			b = b + matrix[k][j]
		al.append(a)
		bl.append(b)
	
	#print 'a list is ', al
	#print 'b list is ', bl
	
	tmpsum = 0
	for l in range (0, 5):
		tmpsum = tmpsum + al[l]*bl[l]
	#print 'pe fenzi sum is: ', tmpsum 
	
	pe = float(tmpsum)/float(allsum*allsum)
	#print 'pe is: ',pe , '\n'
	
	kappa = (p0-pe)/(1-pe)
	#print 'kappa is : ', kappa
	print  kappa
	return kappa
	
		

def gettwokappa(file_one, file_two):
	initList(file_one, file_two)
	avgFormat()
	#printlist(avglist)
	getMatrix()
	#printmatrix()
	return getkappa()
	
#gettwokappa(sys.argv[1], sys.argv[2])

# 下面调试

file_list= ['user-1.txt','user-2.txt', 'user-3.txt', 
			'user-4.txt', 'user-5.txt', 'user-6.txt', 'user-7.txt',
			'user-8.txt', 'user-9.txt', 'user-10.txt']
for user_file in file_list:
	gettwokappa(sys.argv[1], user_file)
