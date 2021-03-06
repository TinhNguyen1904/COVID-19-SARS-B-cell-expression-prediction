# -*- coding: utf-8 -*-
"""NienLuanCoSoNganh_Task5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oG1QPCDGFxA4U4GYMkBgfj0avFLPHMzr
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np 
import pandas as pd
import os
import time
import re
import json
import matplotlib.pyplot as plt
import seaborn as sns
import requests    
from bs4 import BeautifulSoup

# %matplotlib inline
sns.set()

json_file = open("/content/drive/My Drive/Data Notebooks/566b5c62fc77292ebe09295d59e7fbf6fc914260.json", "r")

json_data = json.load(json_file)
json_data

json_data["metadata"]

json_data["abstract"]

json_data["body_text"]

json_data["bib_entries"]

#metadata_df = pd.read_csv("metadata.csv")
ARTICLES = pd.read_csv("/content/drive/My Drive/Data Notebooks/metadata.csv")
ARTICLES.head()

##Đã xóa khung dữ liệu (TABLE) ở trên để dễ đọc
Articles1= ARTICLES[['title','publish_time','journal','url','abstract','doi','cord_uid']]
Articles1.head(2)

## Đánh giá khung dữ liệu
## Tìm kiếm NaN
NaNs=Articles1.isnull().sum()
NaNs

# giới hạn những mục nhập có ABSTRACTS
Abstracts=Articles1.copy()
Abstracts.head(2)

#tách từng từ trong cột ABSTRACT
Abstracts['words'] = Abstracts.abstract.str.strip().str.split('[\W_]+')
Abstracts['words']

#tách các từ trong cột trừu tượng và tạo một cột mới
Abs1 = Abstracts[Abstracts.words.str.len() > 0]
Abs1.head(3)

Abs2=Abs1.isnull().sum()
Abs2

"""Câu trả lời từ tóm tắt văn học về:

Thời gian vi rút phát tán sau khi bệnh khởi phát

Thời gian ủ bệnh ở các nhóm tuổi khác nhau

Thời kỳ ủ bệnh của vi rút là gì?

Tỷ lệ bệnh nhân không có triệu chứng

Bệnh nhi không có triệu chứng

Lây truyền không có triệu chứng trong thời gian ủ bệnh

Lịch sử tự nhiên của vi rút từ người bị nhiễm

Thời gian rụng của virus trung bình là gì?

Khoảng thời gian dài nhất của virus là bao lâu?

Biểu hiện

Tải lượng vi rút liên quan như thế nào đến biểu hiện bệnh, bao gồm khả năng xét nghiệm chẩn đoán dương tính?
"""

#xem qua phần tóm tắt với các thuật ngữ cụ thể

##BẢNG TÓM TẮT VỚI 'cỡ mẫu' 
Sample_size=Abs1[Abs1['abstract'].str.contains('sample size')]
Sample_size
##111 bài viết ABSTRACTS hiển thị 'kích thước mẫu' của 51012 mục nhập

##sự lan truyen của virus
Viral_shed=Abs1[Abs1['abstract'].str.contains('viral shedding')]
Viral_shed
###157 bài tóm tắt bao gồm thuật ngữ 'sự lan truyền của virus'

##1. Thời gian vi rút phát tán sau khi bệnh khởi phát
Q1a=Viral_shed[Viral_shed['abstract'].str.contains('viral shedding after')]
Q1a

Q1b=Viral_shed[Viral_shed['abstract'].str.contains('viral shedding lasts')]
Q1b

##Bảng ủ
Incubation=Abs1[Abs1['abstract'].str.contains('incubation')]
Incubation
###610 tóm tắt bao gồm thuật ngữ 'ươm tạo'

# Q2 Thời gian ủ bệnh ở các nhóm tuổi khác nhau

Q2a=Incubation[Incubation['abstract'].str.contains('different age')]
Q2a

Q2b=Incubation[Incubation['abstract'].str.contains('age group')]
Q2b

# Q3 Thời kỳ ủ bệnh của vi rút là gì?
Q3=Incubation[Incubation['abstract'].str.contains('COVID')]
Q3

##Bảng không triệu chứng

Asymptomatic=Abs1[Abs1['abstract'].str.contains('asymptomatic')]
Asymptomatic
###936 tóm tắt bao gồm thuật ngữ 'ủ bệnh'

#Q4. Tỷ lệ bệnh nhân không có triệu chứng
Q4a=Asymptomatic[Asymptomatic['abstract'].str.contains('number of asymptomatic')]
Q4a

Q4b=Asymptomatic[Asymptomatic['abstract'].str.contains('asymptomatic patients')]
Q4b

#Q5. Bệnh nhi không có triệu chứng
Q5a=Asymptomatic[Asymptomatic['abstract'].str.contains('asymptomatic children')]
Q5a

Q5b=Asymptomatic[Asymptomatic['abstract'].str.contains('pediatric')]
Q5b

#Q6 Lây truyền không có triệu chứng trong thời gian ủ bệnh
Q6a=Incubation[Incubation['abstract'].str.contains('transmission during')]
Q6a

Q6b=Incubation[Incubation['abstract'].str.contains('asymptomatic transmission')]
Q6b

##Q7 Lịch sử tự nhiên của vi rút từ người bị nhiễm
Q7a=Abs1[Abs1['abstract'].str.contains('virus history')]
Q7a

Q7b=Abs1[Abs1['abstract'].str.contains('history of the virus')]
Q7b

#8. Thời gian rụng trung bình của virus là gì?
Q8=Viral_shed[Viral_shed['abstract'].str.contains('viral shedding duration')]
Q8

#9. Khoảng thời gian dài nhất của virus là bao lâu?
Q9=Viral_shed[Viral_shed['abstract'].str.contains('longest')]
Q9

#BANG CHUAN DOAN TOM TAT COVID
# xem qua phần tóm tắt để biết các thuật ngữ cụ thể
##
## BẢNG tóm tắt liên quan đến CHẨN ĐOÁN
Diagnostics=Abs1[Abs1['abstract'].str.contains('diagnostics')]
Diagnostics.shape
## Tôi xác định ở đây 651 mục trong số Tóm tắt liên quan đến CHẨN ĐOÁN

#Rút gọn với thuật ngữ corona
corona=Diagnostics[Diagnostics['abstract'].str.contains('corona')]
corona
## Hiển thị 126 bản tóm tắt liên quan đến chẩn đoán

##Tìm kiếm thông qua Tóm tắt với từ CORONA cho CÔNG CỤ
tools=corona[corona['abstract'].str.contains('diagnostic tools')]
tools
##4 kết quả

#tim kiem voi tu test
testing=Diagnostics[Diagnostics['abstract'].str.contains('test')]
testing

#tim kim voi tu covid
COVID=Diagnostics[Diagnostics['abstract'].str.contains('COVID')]
print(COVID.shape)
print("***************************************************************************")
COVID

#tim kim qua tu FDA
FDA=Diagnostics[Diagnostics['abstract'].str.contains('FDA')]
FDA
#8 tóm tắt liên quan đến FDA và chẩn đoán

#tim kim qua tu viral test
ViralTest=Diagnostics[Diagnostics['abstract'].str.contains('viral test')]
ViralTest
#4 tóm tắt