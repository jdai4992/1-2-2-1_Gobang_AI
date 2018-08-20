from graphics import*

p=[[0 for a in range(16)] for b in range(16)]
black=[[0 for a in range(16)] for b in range(16)]
white=[[0 for a in range(16)] for b in range(16)]
q=[[0 for a in range(15)] for b in range(15)]

list1 = []  # AI
list2 = []  # human
list3 = []  # all

list_all = []  # 整个棋盘的点
next_point = [0, 0]  # AI下一步最应该下的位置

DEPTH = 3  

win=GraphWin('wuziqi',480,600)

shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (50, (0, 1, 0, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (200, (0, 1, 1, 0, 1)),
               (200, (1, 0, 1, 1, 0)),
               (200, (0, 1, 0, 1, 1)),
               (200, (0, 0, 1, 1, 1)),
               (500, (0, 1, 1, 1, 0)),
               (200, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (50000, (1, 1, 0, 1, 1)),
               (50000, (1, 0, 1, 1, 1)),
               (50000, (1, 1, 1, 1, 0)),
               (50000, (0, 1, 1, 1, 1)),
               (500000, (0, 1, 1, 1, 1, 0)),
               (999999999, (1, 1, 1, 1, 1))]
# 评估函数
def evaluation(is_ai):
    total_score = 0

    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    # 算自己的得分
    score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
    global my_score
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    #  算敌人的得分， 并减去
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score

    return total_score

# 每个方向上的分值计算
def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    add_score = 0  # 加分项
    # 在一个方向上， 只取最大的得分项
    max_score_shape = (0, None)

    # 如果此方向上，该点已经有得分形状，不重复计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # 在落子点 左右方向上循环查找得分形状
    for offset in range(-5, 1):
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]

# 负值极大算法搜索 alpha + beta剪枝
def negamax(is_ai, depth, alpha, beta, count):
    Check()
    
    if Check()==1 or Check()==2 or depth == 0:
        return evaluation(is_ai)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list)   # 搜索顺序排序  提高剪枝效率
    # 遍历每一个候选步

    for next_step in blank_list:

        # 如果要评估的位置没有相邻的子， 则不去评估  减少计算
        if not has_neightnor(next_step):
            continue

        if is_ai:
            list1.append(next_step)
        else:
            list2.append(next_step)

        list3.append(next_step)

        testAICount = p[15][15]+count
        
        if testAICount%6==0 or testAICount%6==3 or testAICount%6==4 :
            new_is_ai = False
        if testAICount%6==1 or testAICount%6==2 or testAICount%6==5 :
            new_is_ai = True

        if testAICount%6==2 or testAICount%6==4 :
            value=negamax(new_is_ai,depth-1,alpha,beta,count+1)
        elif testAICount%6==0 or testAICount%6==1 or testAICount%6==3 or testAICount%6==5:
            value = -negamax(new_is_ai, depth - 1, -beta, -alpha, count+1)
            

        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)

        list3.remove(next_step)

        if value > alpha or my_score == 999999999:

            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            # alpha + beta剪枝点
            if value >= beta:
                return beta
            alpha = value

    return alpha

#  离最后落子的邻居位置最有可能是最优点
def order(blank_list):
    last_pt = list3[-1]
    for item in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1]+ j))

def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1]+j) in list3:
                return True
    return False

def ai():
    negamax(True, DEPTH, -999999999, 999999999, 1)
    p=Point(30*(next_point[0])+30, 30+30*(next_point[1]))
    return p

def WinBoard():
    for i in range(15):
       for j in range(15):
            p[i][j]=Point(i*30+30,j*30+30)
            p[i][j].draw(win)
    for r in range(15):
        Line(p[r][0],p[r][14]).draw(win)
    for s in range(15):
        Line(p[0][s],p[14][s]).draw(win)
    center=Circle(p[7][7],3)
    center.draw(win)
    center.setFill('black')

def Click():
    if p[15][15]%6==0 or p[15][15]%6==3 or p[15][15]%6==4 :
        p1=win.getMouse()
        x1=p1.getX()
        y1=p1.getY()
        for i in range(15):
            for j in range(15):
                sqrdis=((x1-p[i][j].getX())*(x1-p[i][j].getX()))+(y1-p[i][j].getY())*(y1-p[i][j].getY())
                if sqrdis<=200 and q[i][j]==0:
                    black[i+1][j+1]=1
                    q[i][j]=Circle(p[i][j],11)
                    q[i][j].draw(win)      
                    q[i][j].setFill('black')
                    list2.append((i,j))
                    list3.append((i,j))
                    p[15][15]+=1

    if p[15][15]%6==1 or p[15][15]%6==2 or p[15][15]%6==5 :
        p2=ai()
        x2=p2.getX()
        y2=p2.getY()
        for i in range(15):
            for j in range(15):
                sqrdis=((x2-p[i][j].getX())*(x2-p[i][j].getX()))+(y2-p[i][j].getY())*(y2-p[i][j].getY())
                if sqrdis<=200 and q[i][j]==0:
                    white[i+1][j+1]=1
                    q[i][j]=Circle(p[i][j],11)
                    q[i][j].draw(win)
                    q[i][j].setFill('white')
                    list1.append((i,j))
                    list3.append((i,j))
                    p[15][15]+=1
        

def Check():
    for i in range(15):
        for j in range(11):
            if black[i+1][j+1] and black[i+1][j+2] and black[i+1][j+3] and black[i+1][j+4] and black[i+1][j+5]:
               return 1
               break
            if white[i+1][j+1] and white[i+1][j+2] and white[i+1][j+3] and white[i+1][j+4] and white[i+1][j+5]:
               return 2
               break
    for i in range(11):
        for j in range(15):
            if black[i+1][j+1] and black[i+2][j+1] and black[i+3][j+1] and black[i+4][j+1] and black[i+5][j+1]:
               return 1
               break
            if white[i+1][j+1] and white[i+2][j+1] and white[i+3][j+1] and white[i+4][j+1] and white[i+5][j+1]:
               return 2
               break
    for i in range(11):
        for j in range(11):
            if black[i+1][j+1] and black[i+2][j+2] and black[i+3][j+3] and black[i+4][j+4] and black[i+5][j+5]:
               return 1
               break
            if white[i+1][j+1] and white[i+2][j+2] and white[i+3][j+3] and white[i+4][j+4] and white[i+5][j+5]:
               return 2
               break
    for i in range(11):
        for j in range(15):
            if black[i+1][j+1] and black[i+2][j] and black[i+3][j-1] and black[i+4][j-2] and black[i+5][j-3]:
               return 1
               break
            if white[i+1][j+1] and white[i+2][j] and white[i+3][j-1] and white[i+4][j-2] and white[i+5][j-3]:
               return 2
               break

def main():
    WinBoard()
    for i in range(16):
        for j in range(16):
            list_all.append((i, j))
    while 1:
        Click()
        Check()
        if Check()==1:
            Text(Point(240,550),'the black wins').draw(win)
            break
        if Check()==2:
            Text(Point(240,550),'the white wins').draw(win)
            break
    win.getMouse()
main()
