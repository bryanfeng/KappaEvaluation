#-*- coding:utf-8 -*-
# 脚本用途：根据所有用户平均值和单个用户原始数据，得到矩阵后，算出kappa值
# 脚本使用方法：
# getMatrix.py  平均值文件 用户原始文件
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# 平均值文件
avg_file = sys.argv[1]
avglist = []

# 用户原始文件
user_file = sys.argv[2]
userlist = []

# 二维矩阵
matrix = [[0 for col in range(6)] for i in range(6)]

# 数据读取到list中
def initList():
	print 'avg file: ' + avg_file + '; user file: ' + user_file
	
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
		if num < 1.499:
			avglist[i] = 1
		elif num > 1.499 and num < 2.499:
			avglist[i] = 2
		elif num > 2.499 and num < 3.499:
			avglist[i] = 3
		elif num > 3.499 and num < 4.499:
			avglist[i] = 4
		elif num > 4.499:
			avglist[i] = 5
		else:
			print 'num is error! ', num

# 输出，调试用
def printlist(listname):
	for l in listname:
		print l

# 计算矩阵
def getMatrix():
	num1 = len(avglist)
	num2 = len(userlist)
	if num1 != num2:
		print 'two list num is not same!'
		return
	for i in range(0, num1):
		x = int(avglist[i])
		y = int(userlist[i])
		matrix[x][y] = matrix[x][y] + 1

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
	
	print dsum
	print 'diagonal sum is :', dsum
	p0 = float(dsum)/allsum
	print 'p0 is :', p0 , '\n'
	
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
	
	print 'a list is ', al
	print 'b list is ', bl
	
	tmpsum = 0
	for l in range (0, 5):
		tmpsum = tmpsum + al[l]*bl[l]
	print 'pe fenzi sum is: ', tmpsum 
	
	pe = float(tmpsum)/float(allsum*allsum)
	print 'pe is: ',pe , '\n'
	
	kappa = (p0-pe)/(1-pe)
	print 'kappa is : ', kappa
	
		
initList()
avgFormat()
#printlist(avglist)
getMatrix()
printmatrix()
getkappa()
