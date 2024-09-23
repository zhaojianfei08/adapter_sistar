# 1 环境

# 2 数据库

> MySQL

```
39.96.77.96 
3306 
root 
root
```

# 3 框架

flask flask_sqlalchemy

jquery

boostrap

# 4 结构

一个模型文件，对应一个蓝图，每个蓝图，对应一个模板文件夹、一个静态文件夹，视图，配置文件。

# 5 bootstrap支持的表单

Text (<input type="text">)：常规的单行文本输入框。
Password (<input type="password">)：密码输入框，输入内容会以点或星号显示。
Email (<input type="email">)：用于电子邮件地址的输入框，会验证输入的格式是否为有效的邮箱格式。
Number (<input type="number">)：数字输入框，可以限制输入的数字范围（通过 min 和 max 属性）和步长（通过 step 属性）。
URL (<input type="url">)：URL输入框，会验证输入内容是否为有效的URL格式。
Tel (<input type="tel">)：电话输入框，用于输入电话号码。
Search (<input type="search">)：搜索框，通常带有特定样式用于搜索输入。
Date (<input type="date">)：日期选择器，用于选择日期。
Time (<input type="time">)：时间选择器，用于选择时间。
Datetime-local (<input type="datetime-local">)：本地日期和时间选择器，允许用户选择日期和时间。
Month (<input type="month">)：月选择器，用于选择年和月份。
Week (<input type="week">)：周选择器，用于选择特定的一周。
Color (<input type="color">)：颜色选择器，用于选择颜色值。
File (<input type="file">)：文件上传输入框，允许用户选择并上传文件。
Checkbox (<input type="checkbox">)：复选框，允许多选。
Radio (<input type="radio">)：单选按钮，通常和一组其他单选按钮一起使用。
Range (<input type="range">)：滑动条输入，用于从一系列数字中选择一个值。
Hidden (<input type="hidden">)：隐藏输入框，不会在页面上显示，但可以用来传递数据。
Reset (<input type="reset">)：重置按钮，点击后会重置表单中的所有字段为初始状态。
Submit (<input type="submit">)：提交按钮，用于提交表单。
Button (<input type="button">)：通用按钮，用于触发JavaScript动作


# 6 如何配置一个新的单模型的增删改查 

## 步骤 

```python
#1- 复制一个apps下面的文件夹 

#2- 修改里面的config文件

#3-修改models里面的Student类 

#4-修改app类加入蓝图

```


# 7 对于一个一对多模型的模板 

# 一方需要一个下拉列表框，可以多选多方的对象，将多方对象的ID传递到后端，后端给1方增加数据，可以在增加的时候和编辑的时候执行这部分操作

# 如果一方被删除，那么多方被自动设置为Null或者级联删除，看模型配置

# 多方可以选择一方的对象，这个时候必须是单选框，单选之后获取到一方的ID，将该ID付给多方的外键
比如书籍，选择作者后，将选择作者的id赋值给数据的author_id 

