cd xxx
@echo off
chcp 65001
set str=%date:~3,4%%date:~8,2%%date:~11,2%_html_api
set str2=report_%date:~3,4%%date:~8,2%%date:~11,2%_%time:~0,2%%time:~3,2%%time:~6,2%.html
echo 报告路径：%str%
echo 报文件径：%str2%
rem xxxx
set excel_file_path = D:\desk20201127\ks_web_allure\Datas
set excel_file_name = test_apidata.xlsx
set sheet_names = t_接
rem 't_接,t_接22'
set sheet_rule = t_
set sheet_kvconfig = config
rem 'config,config22'
cd D:\desk20201127\ks_web_allure
python -m pytest --html=./Report/Html_api/%str%/%str2% --self-contained-html --path=%excel_file_path% --name=%excel_file_name% --sheet=%sheet_names% --rule=%sheet_rule% --conf=%sheet_kvconfig%

pause