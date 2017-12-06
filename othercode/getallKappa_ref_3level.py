#-*- coding:utf-8 -*-
# 脚本用途：算出所有人的kappa 和 第一个人和所有人的kappa默认第一个人是 优质用户
# 脚本使用方法：
# get**.py  优秀用户文件 其他用户文件。。。。
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# 要处理的文件
#file_list= ['1.txt','2.txt', '5.txt', '6.txt', '8.txt', '9.txt', '12.txt', '15.txt', '16.txt', '18.txt', '19.txt', '22.txt', '23.txt', '26.txt', '27.txt', '29.txt', '31.txt', '34.txt', '36.txt', '37.txt', '47.txt', '49.txt', '60.txt', '61.txt', '63.txt', '68.txt', '73.txt', '75.txt', '76.txt', '78.txt', '79.txt', '82.txt', '84.txt', '87.txt', '88.txt', '89.txt', '92.txt', '95.txt','a12.txt', 'a34.txt','a42.txt', 'a44.txt', 'a45.txt','a61.txt', 'a67.txt','97.txt', '103.txt', '105.txt', '106.txt', '112.txt', '117.txt', '124.txt', '127.txt', '129.txt', '136.txt', '137.txt', '139.txt', '142.txt', '145.txt']


# 平均值文件(用户1)
#avg_file = sys.argv[1]
avglist = []

# 用户原始文件（用户2）
#user_file = sys.argv[2]
userlist = []

# 二维矩阵
matrix = [[0 for col in range(4)] for i in range(4)]

# 数据读取到list中
def initList(file1, file2):
	#print 'avg file: ' + file1 + '; user file: ' + file2
	global avglist
	global userlist
	avglist = []
	userlist = []
	
	for line in open(file1):
		line = line.strip()
		avglist.append(float(line))

	for line in open(file2):
		line = line.strip()
		userlist.append(float(line))
	#print avglist, userlist

# 处理平均分为标准分
def avgFormat():
	global avglist
	global userlist
	for i in range(0, len(avglist)):
		num = avglist[i]
		if num < 2.499:
			avglist[i] = 1
		elif num > 2.499 and num < 3.499:
			avglist[i] = 2
		elif num > 3.499 :
			avglist[i] = 3
		else:
			print 'num is error! ', num
			
	for i in range(0, len(userlist)):
		num = userlist[i]
		if num < 2.499:
			userlist[i] = 1
		elif num > 2.499 and num < 3.499:
			userlist[i] = 2
		elif num > 3.499 :
			userlist[i] = 3
		else:
			print 'num is error! ', num
	#print avglist, userlist

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
	
	global matrix
	matrix = [[0 for col in range(4)] for i in range(4)]
	
	for i in range(0, num1):
		x = int(avglist[i])
		y = int(userlist[i])
		matrix[x][y] = matrix[x][y] + 1

# 输出矩阵
def printmatrix():
	#print '\nmatrix is:' 
	for num in range(1, 4):
		print matrix[num][1], matrix[num][2],matrix[num][3]
	#print '\n'

# 得到kappa值
def getkappa():
	# 对角线之和
	dsum = 0.0
	# 总数
	allsum = float(len(avglist))
	
	global matrix
	
	# 计算对角线的和
	for i in range(1, 4):
		dsum = dsum + matrix[i][i]
 
	
	#print dsum
	#print 'diagonal sum is :', dsum
	p0 = float(dsum)/allsum
	#print 'p0 is :', p0 , '\n'
	
	# 计算a1*b1+a2*b2+...ac*bc的和（a1 等于 matrix[1][x]的和  b1等于matrix[x][1]的和）
	a = 0
	al = []
	b = 0
	bl = []
	for j in range(1, 4):
		a = 0
		b = 0
		for k in range(1, 4):
			a = a + matrix[j][k]
			b = b + matrix[k][j]
		al.append(a)
		bl.append(b)
	
	#print 'a list is ', al
	#print 'b list is ', bl
	
	tmpsum = 0
	for l in range (0, 3):
		tmpsum = tmpsum + al[l]*bl[l]
	#print 'pe fenzi sum is: ', tmpsum 
	
	pe = float(tmpsum)/float(allsum*allsum)
	#print 'pe is: ',pe , '\n'
	
	kappa = (p0-pe)/(1-pe)
	#print 'kappa is : ', kappa
	return kappa
	
def gettwokappa(file_one, file_two):
	initList(file_one, file_two)
	avgFormat()
	#printlist(avglist)
	getMatrix()
	#printmatrix()
	return getkappa()


file_list = sys.argv[1:]


i = 0
for user_file in file_list:
	allkappa = 0
	for other_file in file_list:
		if user_file != other_file:
			#print user_file, other_file,':'
			kapp = gettwokappa(user_file, other_file)
			allkappa = allkappa + kapp
			# 第一个优质用户 需要输出一下别人和她的kappa
			if i == 0:
				print user_file, other_file, ':', kapp
	i= i+1
	
	print user_file, ' avg kappa: ', allkappa/(len(file_list)-1)