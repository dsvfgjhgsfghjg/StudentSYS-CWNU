# 学生管理系统

## 环境准备

1. 运行` pip install -r requirements.txt` 

2. 在database.py中修改自己的MySQl账户名和密码。

3. 在数据库创建指定数据库。创建方法如下。

   ```sql
   CREATE DATABASE student_db;
   USE student_db;
   CREATE TABLE students (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       age INT NOT NULL,
       grade VARCHAR(10) NOT NULL
   );
   
   
   ```

## 运行

使用`Python ./main.py`运行该程序