import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

def f_x(x, k, b):
    return k * x + b

def f_y(y, k, b):
    return (y - b) / k

def remove_lines(arr, new_arr, dist_max, dist_min):
    lines = []
    for i in range(len(arr) - 1):
        if (dist_max > distance(new_arr[i][0], new_arr[i][1], new_arr[i + 1][0], new_arr[i + 1][1])) and (
                dist_min < distance(new_arr[i][0], new_arr[i][1], new_arr[i + 1][0], new_arr[i + 1][1])):
            lines.append(arr[i:i + 2])
    lenn = len(list(map(np.unique, lines)))
    if lenn != 0:
        return lines, lenn + 1
    return lines, lenn


def find_length_line(y_min, y_max, x_min, x_max, a, b):

    if (f_x(x_min, a, b)) < y_min:
        y1 = y_min
        if (f_y(y1, a, b)) < x_min:
            x1 = x_min
        elif (f_y(y1, a, b)) > x_max:
            x1 = x_max
        else:
            x1 = f_y(y1, a, b)
    elif (f_x(x_min, a, b)) > y_max:
        y1 = y_max
        if (f_y(y1, a, b)) < x_min:
            x1 = x_min
        elif (f_y(y1, a, b)) > x_max:
            x1 = x_max
        else:
            x1 = f_y(y1, a, b)
    else:
        y1 = f_x(x_min, a, b)
        if (f_y(y1, a, b)) < x_min:
            x1 = x_min
        elif (f_y(y1, a, b)) > x_max:
            x1 = x_max
        else:
            x1 = f_y(y1, a, b)

    if (f_x(x_max, a, b)) < y_min:
        y2 = y_min
        if (f_y(y2, a, b)) < x_min:
            x2 = x_min
        elif (f_y(y2, a, b)) > x_max:
            x2 = x_max
        else:
            x2 = f_y(y2, a, b)
    elif (f_x(x_max, a, b)) > y_max:
        y2 = y_max
        if (f_y(y2, a, b)) < x_min:
            x2 = x_min
        elif (f_y(y2, a, b)) > x_max:
            x2 = x_max
        else:
            x2 = f_y(y2, a, b)
    else:
        y2 = f_x(x_max, a, b)
        if (f_y(y2, a, b)) < x_min:
            x2 = x_min
        elif (f_y(y2, a, b)) > x_max:
            x2 = x_max
        else:
            x2 = f_y(y2, a, b)

    return x1, y1, x2, y2


class MRH:
        
    def fit(self, data):
        
        self.data = data  

    def transform(self, minalph = -90, maxaplh = 90, n = 180, bin_width = 5, limit = 10, length_line_1 = 15, length_line_2 = 15):

        x_min = min(self.data[:,:1])
        x_max = max(self.data[:,:1])
        y_min = min(self.data[:,1:])
        y_max = max(self.data[:,1:])
        
        if (y_max or y_min) < 0:
            delt = int((abs(y_max) + abs(y_min)) / bin_width) 
        else:
            delt = int((y_max - y_min) / bin_width)
        delt = int(delt)

        if (minalph or maxaplh) < 0:
            step = (abs(maxaplh) + abs(minalph)) / n 
        else:
            step = (maxaplh - minalph) / n 

        projections = np.zeros(shape=(len(self.data) + 1, n))

        for i in range(n):       
            tga = np.tan(np.radians(minalph + step * i)) 
            projections[0, i] = tga
            for j in range(len(self.data)):           
                Ypr = self.data[j,1] - self.data[j,0] * tga                    
                projections[j + 1, i] = Ypr  

        plt.ylim(y_min - 5, y_max + 5)
        plt.xlim(x_min - 5, x_max + 5)
        plt.scatter(self.data[:,:1], self.data[:,1:])

        cx = []
        cy = []
        flag = False

        for i in range(projections.shape[1]):
            
            resh_arr = np.reshape(projections[1:,i:i+1], len(projections[1:,i:i+1]))
            a = np.linspace(min(resh_arr), max(resh_arr), delt)
            b = np.zeros_like(a[0:-1])
            c = np.searchsorted(a[0:-1], resh_arr, side= 'right') - 1
            np.add.at(b, c, 1)  

            x_regr = np.array([])
            y_regr = np.array([])
            for j in range(len(b)):
                if b[j] >= limit: 
                    for l in range(len(c)):
                        if c[l] == j:
                            x_regr = np.append(x_regr, self.data[l, 0])
                            y_regr = np.append(y_regr, self.data[l, 1])
                    if len(cx) == 0:  
                        flag = True
                    else:
                        flag = True                    
                        for row in cx:
                            if np.all(x_regr == row):
                                flag = False
                                break        
                    if flag:
                        cx.append(x_regr)
                        cy.append(y_regr)

                    x_regr = np.array([])
                    y_regr = np.array([])

        cx = np.array(cx, dtype='object')
        cy = np.array(cy, dtype='object')

        sum = 0;
        sum2 = 0;
        for i in range(len(cx)):
            reg = linear_model.LinearRegression()
            x = cx[i][:, np.newaxis]
            y = cy[i][:, np.newaxis]

            reg.fit(x, y)
            x1, y1, x2, y2 = find_length_line(16, 80, 110, 165, reg.coef_, reg.intercept_)
            new_proj_arr = new_projections(np.hstack([x,y]), x1, y1, x2, y2)
            lines, lenn = remove_lines(x, new_proj_arr, length_line_1, length_line_2)
            for line in lines:
                plt.plot(line, Fx(line, reg.coef_, reg.intercept_),color="red")  

            x = np.append(x, 100)
            x = np.append(x, 180)
            #print(x)
            #print(Fx(x, reg.coef_, reg.intercept_))
            #print(reg.coef_, reg.intercept_)
            #plt.plot(x, Fx(x, reg.coef_, reg.intercept_)[0],color="red")        
            #plt.plot(x, F(x, np.tan(np.radians(minalph)), reg.intercept_ - reg.intercept_* (np.tan(np.radians(minalph)) - reg.coef_)))
            #sum += lenn # / findLengthLine(16, 80, 110, 165, reg.coef_, reg.intercept_)
            #print(sum)

            #print(findLengthLine(16, 80, 110, 165, reg.coef_, reg.intercept_))

            sum2 += lenn / distance(x1, y1, x2, y2)[0][0]
            #print(sum2)


        plt.xlabel('M1 (u)')
        plt.ylabel('M2 (u)')
        plt.show()
    
    def fit_transform(self, data, minalph = -90, maxaplh = 90, n = 180, bin_width = 5, limit = 10, length_line_1 = 15, length_line_2 = 15):
        
        self.fit(data)
        self.transform(minalph = -90, maxaplh = 90, n = 180, bin_width = 5, limit = 10, length_line_1 = 15, length_line_2 = 15)
        