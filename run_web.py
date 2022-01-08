import pytest
from Common.handle_config import ReadWriteConfFile
from Common.utils import mDate, mDateTime

ReadWriteConfFile().set_option('report', 'report_dir_folder', mDate()+'_html_api')
ReadWriteConfFile().set_option('report', 'report_file_name', f'report_{mDateTime()}.html')
report_dir = mDate()+'_html_web'
report_file = 'report_' + mDateTime()+'.html'

pytest.main([f'--html=./Report/html_web/{report_dir}/{report_file}', '--self-contained-html'])


