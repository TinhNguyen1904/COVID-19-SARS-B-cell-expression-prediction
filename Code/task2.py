# -*- coding: utf-8 -*-
"""NienLuanCoSoNganh_Task2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14MjJSDewZCn5ZjZj07xbPgCPj1x9BJrB
"""

#cài đặt thư viện
import numpy as np
import pandas as pd

#đọc dữ liệu
data_bcell=pd.read_csv('/content/drive/My Drive/Data Notebooks/input_bcell.csv')
data_sars=pd.read_csv('/content/drive/My Drive/Data Notebooks/input_sars.csv')
data=pd.concat([data_bcell,data_sars])
data.head()
#xử lý tập dữ liệu
data_drop = data.drop(['parent_protein_id','protein_seq','peptide_seq'],axis = 1)
data_drop.head()

data_drop['target'].value_counts()/len(data_drop)*100

data_drop['peptide_length']=data_drop['end_position'] - data_drop['start_position'] + 1

x=data_drop.drop(columns='target')
y=data_drop['target']

#các thuộc tính quan trọng
from sklearn.ensemble import ExtraTreesClassifier
r = ExtraTreesClassifier(random_state=0)
r.fit(x,y)
feature_importance = r.feature_importances_
feature_importance_normalized = np.std([tree.feature_importances_ for tree in 
                                        r.estimators_], 
                                        axis = 0)

# hiên rthij biểu đồ các thuộc tính quan trọng
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
plt.figure(figsize=(10,5))
sns.barplot(feature_importance_normalized,x.columns,color='blue') 
plt.xlabel('Feature Labels') 
plt.ylabel('Feature Importances') 
plt.title('Comparison of different Feature Importances') 
plt.show()

#tính độ dài của peptide_length
data_drop['peptide_length'].value_counts()/len(data_drop)*100

# phân tích dữ liệu thuộc tính
features=["chou_fasman","emini","kolaskar_tongaonkar","parker","peptide_length","isoelectric_point","aromaticity",
            "hydrophobicity","stability"]
plt.figure(figsize=(20,20))
plt.subplots_adjust(hspace=2.0)
j=1
for i in features:
    plt.subplot(4,5,j)
    sns.distplot(data_drop[i])
    j+=1

#xây dựng model
from sklearn.model_selection import train_test_split
X_train,X_valid,Y_train,Y_valid=train_test_split(x,y,stratify=y,test_size=0.3,random_state=0)

#trực quan hóa dữ liệu
from sklearn.preprocessing import MinMaxScaler
d=MinMaxScaler()
d.fit_transform(X_train,Y_train)

d.transform(X_valid)

# Thực hiện rừng ngẫu nhiên
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators=15,criterion="entropy",random_state=0)
forest.fit(X_train,Y_train)

lg_pred=forest.predict(X_valid)
lg_pred

#độ chính xác
roc_auc_score(lg_pred,Y_valid)

#dự đoán tập dữ liệu train
predictions=pd.DataFrame(lg_pred,columns=['validation_pred'])
predictions.head()

predictions.value_counts()/len(data_drop)*100

#đọc tập dữ liệu kiểm tra
data_covid=pd.read_csv('/content/drive/My Drive/Data Notebooks/input_covid.csv')
data_covid.head()

#Xử lý tập dữ liệu kiểm tra
data_covid.drop(columns=['parent_protein_id','protein_seq','peptide_seq'],inplace=True)
data_covid

data_covid.isnull().sum()

data_covid['length']=data_covid['end_position']-data_covid['start_position'] + 1
d.transform(data_covid)

#dự đoán tập dữ liệu test
y_pred=forest.predict(data_covid)
y_pred

y_pred=pd.DataFrame(y_pred,columns=['test_pred'])
y_pred.head()

y_pred.value_counts()/len(data_covid)*100