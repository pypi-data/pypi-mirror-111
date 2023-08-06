import matplotlib.pyplot as plt
import numpy as np
import cv2


def f_hough_x(x, theta, rho):
    return -(np.cos(theta)/np.sin(theta)) * x + (rho / np.sin(theta))

def f_hough_y(y, theta, rho):
    return (rho / np.cos(theta)) - y * (np.sin(theta) / np.cos(theta))

def distance(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def find_length_line_hough(y_min, y_max, x_min, x_max, a, b):
    
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
          
    if (FhoughX(x_min, a, b)) < y_min:
        y1 = y_min
        if (FhoughY(y1, a, b)) < x_min:
            x1 = x_min
        elif (FhoughY(y1, a, b)) > x_max:
            x1 = x_max
        else:
            x1 = FhoughY(y1, a, b)
    elif (FhoughX(x_min, a, b)) > y_max:
        y1 = y_max
        if (FhoughY(y1, a, b)) < x_min:
            x1 = x_min
        elif (FhoughY(y1, a, b)) > x_max:
            x1 = x_max
        else:
            x1 = FhoughY(y1, a, b)
    else:
        y1 = FhoughX(x_min, a, b)
        if (FhoughY(y1, a, b)) < x_min:
            x1 = x_min
        elif (FhoughY(y1, a, b)) > x_max:
            x1 = x_max
        else:
            x1 = FhoughY(y1, a, b)
            
            
    if (FhoughX(x_max, a, b)) < y_min:
        y2 = y_min
        if (FhoughY(y2, a, b)) < x_min:
            x2 = x_min
        elif (FhoughY(y2, a, b)) > x_max:
            x2 = x_max
        else:
            x2 = FhoughY(y2, a, b)
    elif (FhoughX(x_max, a, b)) > y_max:
        y2 = y_max
        if (FhoughY(y2, a, b)) < x_min:
            x2 = x_min
        elif (FhoughY(y2, a, b)) > x_max:
            x2 = x_max
        else:
            x2 = FhoughY(y2, a, b)
    else:
        y2 = FhoughX(x_max, a, b)
        if (FhoughY(y2, a, b)) < x_min:
            x2 = x_min
        elif (FhoughY(y2, a, b)) > x_max:
            x2 = x_max
        else:
            x2 = FhoughY(y2, a, b)
                           
    return x1, y1, x2, y2


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


class OH:
        
    def fit(self, data):
        
        self.data = data
        self.hough_data = np.array(data, np.float32).reshape(-1, 1, 2)

    def transform(self, lines_max, threshold, min_rho, max_rho, rho_step, min_theta, max_theta, theta_step):

        lines = cv2.HoughLinesPointSet(self.hough_data, lines_max, threshold, min_rho, max_rho, rho_step, min_theta, max_theta, theta_step)
        
        plt.scatter(self.data[:,:1], self.data[:,1:], s=5, color = 'blue')
        
        for line in lines:
            for votes,rho,theta in line:
                x1, y1, x2, y2 = find_length_line(20, 85, 114, 158, theta, rho)
                plt.plot([x1, x2], [y1, y2], color = 'red')
                
        plt.show()
    
    def fit_transform(self, data, lines_max, threshold, min_rho, max_rho, rho_step, min_theta, max_theta, theta_step):
        
        self.fit(data)
        self.transform(lines_max, threshold, min_rho, max_rho, rho_step, min_theta, max_theta, theta_step)
        