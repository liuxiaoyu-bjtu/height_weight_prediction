import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import os

global_dataset_url = '小学四年级学生身高体重数据.csv'


# 读取原始数据集并划分数据
def read_data(gender, dataset_url = global_dataset_url):
    df_stu = pd.read_csv(dataset_url) # 读取数据
    gender_data = df_stu[df_stu['性别'] == gender] # 根据性别列进行筛选
    X = gender_data[['体重（千克）', '身高（厘米）']] #提取特征列
    y = gender_data['水平']  #提取标签列
    return X, y


# 可视化数据集中的数据，为学生自测数据描点做准备
def read_visualize_data(gender):
    X, y = read_data(gender) # 读取数据
    
    # 可视化训练数据
    plt.figure(figsize=(16,10), dpi=60)
    # 设置显示格式
    custom_font = FontProperties(fname='SimHei.ttf', size=16) # 设置支持中文字符的字体
    plt.rc('axes',unicode_minus=False) #解决坐标轴负号显示问题

    colors = {'偏低': 'green', '正常':'blue' , '偏高': 'red'} 
    markers = {'偏低': 'o', '正常':'s' , '偏高': '^'} 

    # 创建散点图，根据等级区分颜色和形状
    for level in y.unique():
        level_data = X[y == level]
        # plt.scatter(level_data['体重（千克）'], level_data['身高（厘米）'], c=colors[level], marker=markers[level], label=level, s=90)
        plt.scatter(level_data['体重（千克）'], level_data['身高（厘米）'], marker=markers[level], facecolors='none', edgecolors=colors[level], linewidth=2, label=level, s=90)
    
    plt.legend(prop=custom_font) # 添加图例
    plt.xlabel(X.columns[0],fontsize=20,loc='center', fontproperties=custom_font)
    plt.ylabel(X.columns[1],fontsize=20,loc='center', fontproperties=custom_font)
    plt.title('散点图',fontsize=20,loc='center', fontproperties=custom_font)
    plt.show()
    # 保存图像到文件
    plt.savefig('scatter_plot_1.png')

# def read_visualize_data(gender):
#     X, y = read_data(gender) # 读取数据

#     # 可视化训练数据
#     plt.figure(figsize=(16,10), dpi=60)
#     custom_font = FontProperties(fname='SimHei.ttf') # 设置支持中文字符的字体
#     plt.rc('axes',unicode_minus=False) #解决坐标轴负号显示问题
#     colors = {'偏低': 'green', '正常':'blue' , '偏高': 'red'} 
    
#     y = y.values.tolist()
#     c = []
#     for i in y:
#         c.append(colors[str(i)])
#     plt.scatter(X.iloc[:,0], X.iloc[:,1], color=c, s=100, cmap='cool') # 画出样本散点图
#     plt.xlabel(X.columns[0],fontsize=20,loc='center', fontproperties=custom_font)
#     plt.ylabel(X.columns[1],fontsize=20,loc='center', fontproperties=custom_font)
#     plt.title('散点图',fontsize=20,loc='center', fontproperties=custom_font)
#     # plt.show()
#     # 保存图像到文件
#     plt.savefig('scatter_plot_1.png')

# 定义KNN模型
def create_KNN(n_neighbors, X, y):
    model = KNeighborsClassifier(n_neighbors)
    model.fit(X, y)
    return model

def predict_data_visualize(gender, height, weight, K=5):
    X, y = read_data(gender)
    model = create_KNN(5, X, y) # 创建KNN模型
    input_data = pd.DataFrame({'体重（千克）': [weight], '身高（厘米）': [height]}) # 输入的待预测数据
    prediction = model.predict(input_data) # 使用模型预测数据

    # 输出预测结果
    # print("预测结果：该同学水平分类:", prediction[0])

    neighbors = model.kneighbors(input_data, return_distance=False) # 默认是5个最近邻，返回的是训练集中的index
    
    plt.figure(figsize=(16,10), dpi=60)
    custom_font = FontProperties(fname='SimHei.ttf', size=16) # 设置支持中文字符的字体

    colors = {'偏低': 'green', '正常':'blue' , '偏高': 'red'} 
    # 使用字典的get方法根据prediction[0]获取颜色值，如果键存在的话
    color = colors.get(prediction[0], 'black')

    markers = {'偏低': 'o', '正常':'s' , '偏高': '^'} 

    # 创建散点图，根据等级区分颜色和形状
    for level in y.unique():
        level_data = X[y == level]
        # plt.scatter(level_data['体重（千克）'], level_data['身高（厘米）'], c=colors[level], marker=markers[level], label=level, s=90)
        plt.scatter(level_data['体重（千克）'], level_data['身高（厘米）'], marker=markers[level], facecolors='none', edgecolors=colors[level], linewidth=2, label=level, s=90)
    
    plt.legend(prop=custom_font) # 添加图例
    # y = y.values.tolist()
    # c = []
    # for i in y:
    #     c.append(colors[str(i)])
    # plt.scatter(X.iloc[:,0], X.iloc[:,1], color=c, s=100, cmap='cool')        #绘制训练集散点图
    plt.scatter(input_data.iloc[0][0], input_data.iloc[0][1], marker="x",c=color, s=200, cmap='cool')     #待预测的点,**这里可以改变

    for i in neighbors[0]:
        plt.plot([X.iloc[i][0], input_data.iloc[0][0]], [X.iloc[i][1], input_data.iloc[0][1]], 
                    '-.', linewidth=0.6);    # 预测点与距离最近的 k 个样本的连线
        
    plt.xlabel(X.columns[0],fontsize=20,loc='center', fontproperties=custom_font)
    plt.ylabel(X.columns[1],fontsize=20,loc='center', fontproperties=custom_font)
    plt.title('knn分类模型',fontsize=20,loc='center', fontproperties=custom_font)
    # plt.show()
    image_path = 'scatter_plot_2.png'
    # 保存图像到文件
    plt.savefig(image_path)
    # 返回图像文件路径
    return image_path, prediction[0]


# 根据输入对*两个*数据集的KNN模型进行预测结果可视化
def predict_less_data_visualize(gender, height, weight, K=5):
# 更少的数据
    X_1, y_1 = read_data(gender, dataset_url = '小四学生部分身高体重数据.csv')
    model_1 = create_KNN(5, X_1, y_1) # 创建KNN模型
    input_data_1 = pd.DataFrame({'体重（千克）': [weight], '身高（厘米）': [height]}) # 输入的待预测数据
    prediction_1 = model_1.predict(input_data_1) # 使用模型预测数据

    neighbors_1 = model_1.kneighbors(input_data_1, return_distance=False) # 默认是5个最近邻，返回的是训练集中的index
    plt.figure(figsize=(16,10), dpi=60)
    custom_font = FontProperties(fname='SimHei.ttf', size=16) # 设置支持中文字符的字体
    colors = {'偏低': 'green', '正常':'blue' , '偏高': 'red'} 
    # 使用字典的get方法根据prediction[0]获取颜色值，如果键存在的话
    color = colors.get(prediction_1[0], 'black')
    markers = {'偏低': 'o', '正常':'s' , '偏高': '^'} 
    # 创建散点图，根据等级区分颜色和形状
    for level in y_1.unique():
        level_data = X_1[y_1 == level]
        # plt.scatter(level_data['体重（千克）'], level_data['身高（厘米）'], c=colors[level], marker=markers[level], label=level, s=90)
        plt.scatter(level_data['体重（千克）'], level_data['身高（厘米）'], marker=markers[level], facecolors='none', edgecolors=colors[level], linewidth=2, label=level, s=90)
    plt.legend(prop=custom_font) # 添加图例
    plt.scatter(input_data_1.iloc[0][0], input_data_1.iloc[0][1], marker="x",c=color, s=200, cmap='cool')     #待预测的点,**这里可以改变
    for i in neighbors_1[0]:
        plt.plot([X_1.iloc[i][0], input_data_1.iloc[0][0]], [X_1.iloc[i][1], input_data_1.iloc[0][1]], 
                    '-.', linewidth=0.6);    # 预测点与距离最近的 k 个样本的连线
    plt.xlabel(X_1.columns[0],fontsize=20,loc='center', fontproperties=custom_font)
    plt.ylabel(X_1.columns[1],fontsize=20,loc='center', fontproperties=custom_font)
    plt.title('knn分类模型',fontsize=20,loc='center', fontproperties=custom_font)
    # plt.show()
    image_path = 'scatter_plot_3.png'
    # 保存图像到文件
    plt.savefig(image_path)
    # 返回图像文件路径
    return image_path, prediction_1[0]


def bmi_value(height, weight, gender):
    height = height / 100
    bmi = weight / (height ** 2)
    result = ""
    if gender == "女生":
        if bmi <= 13.6:
            result = "偏低"
        elif bmi <= 19.4:
            result = "正常"
        else:
            result = "偏高"
    else:
        if bmi <= 14.1:
            result = "偏低"
        elif bmi <= 20.1:
            result = "正常"
        else:
            result = "偏高"
    return result
