# ks_autotest         作者:kangs2008

## 版本：V 2.0
- API测试有俩种方式进行
- 1,通过excel来编写用例，以excel来驱动测试框架，不用写python脚本
- 2,通过写python脚本的方式，进行测试
- log报告文件输出
- WEB UI 测试：极简代码输出，减少python脚本编写工作量。
- 错误自动截图和可按需截图和截图标记

## 项目说明
- 本框架是基于**pytest+allure/html**设计
- excel+api 框架经过多次重构，更符合pytest执行模式，关键字与脚本依赖更少
- excel sheet可多选，行也可以做到可选择，执行脚本更方便，任意
- excel内部常量替换，excel与response之间关联字段替换，都很好的完成
- assert绝对路径，相对路径，整个response，返回值的一部分dict之间的比较都支持

## 技术栈
- requests
- pytest
- pytest-html
- pytest-allure
- openpyxl
- logging
- cv2

## 截图
![allure1 report](./Sn.png "Sn.png")
![allure2 report](./Sn2.png "Sn2.png")