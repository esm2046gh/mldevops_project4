#
# * * * * * /mnt/d/ml/mldevops_project4/cronjob_test.sh  >/dev/null 2>&1
#
from datetime import datetime

with open('cronjob_test.txt', 'a+') as a_file:
    now_str = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
    a_file.write(now_str + '. Hello cronjob.\n')
