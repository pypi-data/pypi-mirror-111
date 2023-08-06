import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model


def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def f_x(x, k, b):
    return k * x + b

def f_y(y, k, b):
    return (y - b) / k

def new_projections(arr, x1, y1, x2, y2):
    if not isinstance(x1, int):
        x1 = x1[0][0]

    if not isinstance(y1, int):
        y1 = y1[0][0]

    if not isinstance(x2, int):
        x2 = x2[0][0]

    if not isinstance(y2, int):
        y2 = y2[0][0]

    line = []
    line.append([x1, y1])
    line.append([x2, y2])
    new_arr = []

    for i in range(len(arr)):
        point = [arr[i][0], arr[i][1]]
        x = np.array(point)

        u = np.array(line[0])
        v = np.array(line[len(line)-1])


        n = v - u
        n /= np.linalg.norm(n, 2)

        P = u + n*np.dot(x - u, n)
        new_arr.append(P)

    new_arr = np.sort(new_arr, 0)

    return new_arr


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


def line_window(projections, width, threshold):
    dots = projections[:]
    result = []

    left = min(dots)
    line = []

    while len(dots) > 1:
        is_insert = True
        line.append(left)
        try:
            dots.remove(left)
        except ValueError:
            pass
        left = min(dots)
        if abs(left - line[0]) <= width:
            is_insert = False

        elif len(line) > 1 and len(dots) > 1:
            dots.remove(left)
            new_left = min(dots)
            if abs(new_left - line[1]) <= width and abs(line[1] - line[0]) > abs(new_left - left):
                line.remove(line[0])
                is_insert = False

        if abs(left - line[0] > width and len(line) >= threshold):
            result.append(list(set(line)))
            is_insert = True

        if is_insert:
            line.clear()

    return result


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


class MNP:

    def fit(self, data):

        self.data = data

    def transform(self, angle=45, bin_width=1, limit=5, length_line_1=15, length_line_2=0):

        tga = np.tan(np.radians(angle))
        projections = []

        for i in range(len(self.data)):
            projections.append(self.data[i, 1] - self.data[i, 0] * tga)

        plt.ylim(self.data[:, 1:].min() - 5, self.data[:, 1:].max() + 5)
        plt.xlim(self.data[:, :1].min() - 5, self.data[:, :1].max() + 5)
        plt.scatter(self.data[:, :1], self.data[:, 1:], s=5)

        pre_lines = line_window(projections, bin_width, limit)

        cx = []
        cy = []

        for pre_line in pre_lines:
            tmp_x = []
            tmp_y = []
            for i in range(len(pre_line)):
                j = projections.index(pre_line[i])
                tmp_x.append(float(self.data[:, :1][j])), tmp_y.append(float(self.data[:, 1:][j]))
            cx.append(tmp_x), cy.append(tmp_y)

        sum = 0;
        sum2 = 0;
        for i in range(len(cx)):
            reg = linear_model.LinearRegression()
            x = np.array(cx[i])[:, np.newaxis]
            y = np.array(cy[i])[:, np.newaxis]

            reg.fit(x, y)
            x1, y1, x2, y2 = find_length_line(16, 80, 110, 165, reg.coef_, reg.intercept_)
            new_proj_arr = new_projections(np.hstack([x, y]), x1, y1, x2, y2)
            lines, lenn = remove_lines(x, new_proj_arr, length_line_1, length_line_2)
            for line in lines:

                plt.plot(line, f_x(line, reg.coef_, reg.intercept_), color="red")

            sum += lenn  # / findLengthLine(16, 80, 110, 165, reg.coef_, reg.intercept_)

            sum2 += lenn / distance(x1, y1, x2, y2)[0][0]

            #print(sum2)

        plt.xlabel('M1 (u)')
        plt.ylabel('M2 (u)')
        plt.show()

        #return (sum2)

    def fit_transform(self, data, angle=45, bin_width=1, limit=5, length_line_1=15, length_line_2=0):

        self.fit(data)
        self.transform(angle, bin_width, limit, length_line_1, length_line_2)