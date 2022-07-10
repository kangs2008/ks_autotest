import pytest
from Common.handle_config import ReadWriteConfFile
from Common.utils import mDate, mDateTime
from pathlib import Path

excel_file_path = r'E:\git_\ks_autotest\TestDatas'
excel_file_name = 'test_apidata.xlsx'
sheet_names = 't_接'  # 't_接,t_接22'

report_dir = mDate() + '_html_api'
report_file = 'report_' + mDateTime() + '.html'
ReadWriteConfFile().set_option('report', 'report_dir_folder', mDate() + '_html_api')
ReadWriteConfFile().set_option('report', 'report_file_name', f'report_{mDateTime()}.html')

report_path = Path().joinpath('./Report', report_dir)
if not Path(report_path).exists():
    Path(report_path).mkdir(parents=True, exist_ok=True)


pytest.main([f'--html={Path(report_path).absolute()}/{report_file}', '--self-contained-html',
             f'--path={str(excel_file_path)}',f'--name={str(excel_file_name)}',
             f'--sheet={str(sheet_names)}'])


# ReadWriteConfFile().set_option('test_data', 'excel_file_path', excel_file_path)
# ReadWriteConfFile().set_option('test_data', 'excel_file_name', excel_file_name)
# ReadWriteConfFile().set_option('test_data', 'sheet_names', sheet_names)
# ReadWriteConfFile().set_option('test_data', 'sheet_rule', sheet_rule)
# ReadWriteConfFile().set_option('test_data', 'sheet_kcConfig', sheet_kvconfig)
# pytest.main(['--html=./Report/html_api/20220103_html_api/report_.html', '--self-contained-html'])

