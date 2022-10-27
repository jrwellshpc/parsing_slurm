# This scripts produces RestartCNT, PendingTime, and a % of partitions that jobs are running on.
# It is from the perspective of a school using an institutional cluster.

import subprocess

# This helps calc the averages for RestartCNT and PendingTime
def cal_average(num):
    sum_num = 0
    for t in num:
        if t.isnumeric() is True:
           sum_num = sum_num + int(t)

    avg = sum_num / len(num)
    return avg

# Insert the accounts you want to study under --account below
cmd=["bash", "-c", "/usr/bin/squeue --account <Your Partitions Go Here> --Format='RestartCnt:|','PendingTime:|','Partition'"]
try:
    squeue = subprocess.run(cmd, timeout=10, stdout = subprocess.PIPE)
except subprocess.TimeoutExpired:
    print('Timeout')

# Decode the byte stream above to utf-8
squeueOutput = squeue.stdout.decode("utf-8")

# Split the resulting output out so we can place it into lists.
squeueOutput2 = squeueOutput.splitlines()
temp_squeue=[]

# Said lists
RestartCnt=[]
PendingTime=[]
Partition=[]

# Spin through squeueOutput2 (which is splitlined) to populate our lists
for x in range(len(squeueOutput2)):
    temp_squeue = squeueOutput2[x].strip().split("|")
    RestartCnt.append(temp_squeue[0])
    PendingTime.append(temp_squeue[1])
    Partition.append(temp_squeue[2])

RestartCnt_Average=cal_average(RestartCnt)
PendingTime_Average=cal_average(PendingTime)

# Now, 
ours=0
notours=0

# This is the tricky part. Duplicate the line below with all of 'your' partitions (i.e. your schools')

if Partition.count('Your Partition') > 0: ours += 1

# And then below the partitions your folks can use that aren't yours.

if Partition.count('general') > 0: notours += 1
if Partition.count('gpu') > 0: notours += 1

print('Restarts:' + str(RestartCnt_Average), 'Pending:' + str(PendingTime_Average), '%SEASParts:' + str((ours/(seas+notours)*100)))
