import pytest
from Common.handle_config import ReadWriteConfFile
from Common.utils import mDate, mDateTime

excel_file_path = r'D:\desk20201127\ks_web_allure\TestDatas'
excel_file_name = 'test_apidata.xlsx'
sheet_names = 't_接'  # 't_接,t_接22'
sheet_rule = 't_'
sheet_kvconfig = 'config'  # 'config,config22'

ReadWriteConfFile().set_option('report', 'report_dir_folder', mDate()+'_html_api')
ReadWriteConfFile().set_option('report', 'report_file_name', f'report_{mDateTime()}.html')
report_dir = mDate()+'_html_api'
report_file = 'report_' + mDateTime()+'.html'

pytest.main([f'--html=./Report/html_api/{report_dir}/{report_file}', '--self-contained-html',
             f'--path={str(excel_file_path)}',f'--name={str(excel_file_name)}',
             f'--sheet={str(sheet_names)}',f'--rule={str(sheet_rule)}',
             f'--conf={str(sheet_kvconfig)}'])


# ReadWriteConfFile().set_option('test_data', 'excel_file_path', excel_file_path)
# ReadWriteConfFile().set_option('test_data', 'excel_file_name', excel_file_name)
# ReadWriteConfFile().set_option('test_data', 'sheet_names', sheet_names)
# ReadWriteConfFile().set_option('test_data', 'sheet_rule', sheet_rule)
# ReadWriteConfFile().set_option('test_data', 'sheet_kcConfig', sheet_kvconfig)
# pytest.main(['--html=./Report/html_api/20220103_html_api/report_.html', '--self-contained-html'])

