import os
import sys
import subprocess
import errno
import getpass
import time 
from time import sleep
# from paramiko import SSHClient
import socket
hostname = socket.gethostname()

# Paths
# m5_mcpat_path = os.environ['M5MCPATPATH']
# m5_mcpat_conversion_script = os.environ['M5TOMCPAT_CONVSCRIPT']
m5_path = os.environ.get('M5PATH')
mcpat_path = os.environ.get('MCPATPATH')
helpers_path = os.environ.get('HELPDIR')
username = getpass.getuser()
squeue_self_limit = 800

def run_binary(cmd_str, job_name, out_dir, mode="dryrun", append_to="jobs.log", prereq=-1, is_ramulator=False, is_local=False, exclude_nodes=[]):

  cmd_arr = []
  for q_index, qstr in enumerate(cmd_str.split("\"")):
    if q_index % 2 == 0:
      cmd_arr += qstr.split()
    else:
      cmd_arr.append('"'+qstr+'"')

  if "slurm" in mode:
    # wait_for_queue()
    #print "Submitting the job:", cmd_str

    mkdir_p(out_dir)

    sbatch_str  = "sbatch --partition=slurm_part"
    sbatch_str += " --mincpus=1"
    # sbatch_str += " --mem=" + str(memory_estimate)
    sbatch_str += " --job-name="+job_name+"_"+out_dir
    sbatch_str += " --output="+out_dir+"/"+job_name+".stdout"
    sbatch_str += " --error="+out_dir+"/"+job_name+".stderr"
    if prereq >= 0:
      sbatch_str += " --dependency=afterok:"+str(prereq)
    if is_local:  
      exclude_nodes = []
      for i in range(10):
        if hostname != "kratos"+str(i):
          exclude_nodes.append("kratos"+str(i))

    if len(exclude_nodes) > 0:
      sbatch_str += " --exclude="+",".join(exclude_nodes)

    if is_ramulator:
        sbatch_str += " "+helpers_path+"/run_ramulator.sh "
    else: 
        sbatch_str += " "+helpers_path+"/srunbuf.sh "

    sbatch_arr = sbatch_str.split() + cmd_arr
    #print sbatch_arr
    # quit()
    #Execute sbatch command
    process = subprocess.Popen(sbatch_arr, stdout=subprocess.PIPE)
    output, error = process.communicate()
    #with open(out_dir+"/"+job_name+".slurmout", 'w+') as f:
    #  f.write(output)
    #  if error:
    #    f.write(error)
    sleep(1)
    jobid = str(output).split(" ")[-1]
    return jobid    

  elif "nonblocking" in mode:
    process = subprocess.Popen(cmd_arr, stdout=subprocess.PIPE)
    return process

  elif "blocking" in mode:
    print("Running the job:", cmd_str)
    mkdir_p(out_dir)

    if "/panzer/" in out_dir:
        mkdir_p(out_dir.replace("/panzer/", "/local/"))

    if "/local/" in out_dir:
        mkdir_p(out_dir.replace("/local/", "/panzer/"))

    process = subprocess.Popen(cmd_arr, stdout=subprocess.PIPE)
    process.wait()
    output, error = process.communicate()

    with open(out_dir+"/"+job_name+".stdout", 'w+') as f:
      f.write(output)

    if error:
      with open(out_dir+"/"+job_name+".stderr", 'w+') as f:
        f.write(error)

  elif "dryrun" in mode:
    with open(append_to, "a+") as f:
        f.write(cmd_str + " &\n")

def mkdir_p(directory):
  try:
    os.makedirs(directory)
  except OSError as exc:  # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(directory):
      pass
    else:
      raise

def remote_mkdir_p(directory):
  #cmd = helpers_path + "/kratos_mkdir_p.sh " + directory
  #run_binary(cmd, "mkdir", directory, mode="blocking", append_to="jobs.log", is_ramulator=False)
  ssh = SSHClient()
  ssh.load_system_host_keys()
  for i in [0,1,2,3,4,5,7,8,9]:
    ip = "10.1.212.16"+str(i)
    ssh.connect('yaglikca@'+ip+":22")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('mkdir -p '+directory)
    print(ssh_stdout)
    print(ssh_stderr)

def remote_mkdir(directory):
  for kratosid in range(10):
    cmdstr = "ssh yaglikca@kratos"+str(kratosid)+" \"mkdir -p " + directory + "\""
    print(cmdstr)
    process = subprocess.Popen(cmdstr.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output) 
    if error:
      print(error)
      quit()


def convert_gem5_mcpat(gem5_out_dir):
  if "GEM5ToMcPAT.py" in m5_mcpat_conversion_script:
    convert_gem5_to_cmcpat(gem5_out_dir)
  else:
    convert_gem5_to_mcpat(gem5_out_dir)


def convert_gem5_to_mcpat(gem5_out_dir):
  # ./gem5McPATparse -x template.xml -c config.ini -s stats.txt -o out.xml
  cmd_str = m5_mcpat_conversion_script # m5_mcpat_path+"/gem5McPATparse"
  cmd_str += " -x " + m5_mcpat_path + "/template.xml"
  cmd_str += " -c " + gem5_out_dir + "/config.ini"
  cmd_str += " -s " + gem5_out_dir + "/stats.txt"
  cmd_str += " -o " + gem5_out_dir + "/mcpat.xml"

  run_binary(cmd_str, "gem5mcpat", gem5_out_dir)


def convert_gem5_to_cmcpat(gem5_out_dir):
  # GEM5ToMcPAT.py [options] <gem5 stats file> <gem5 config file (json)> <mcpat template file>
  cmd_str = m5_mcpat_conversion_script
  cmd_str += " " + gem5_out_dir + "/stats.txt"
  cmd_str += " " + gem5_out_dir + "/config.json"
  cmd_str += " " + gem5_out_dir + "/mcpat_template.xml"
  cmd_str += " -o " + gem5_out_dir + "/mcpat.xml"

  run_binary(cmd_str, "gem5mcpat", gem5_out_dir)


def run_mcpat(gem5_out_dir):
  # mcpat -infile <input file name>  -print_level < level of details 0~5 >  -opt_for_clk < 0 (optimize for ED^2P only)/1 (optimzed for target clock rate)>
  cmd_str = mcpat_path + "/mcpat"
  cmd_str += " -infile " + gem5_out_dir+"/mcpat.xml"
  cmd_str += " -print_level 1"
  cmd_str += " -opt_for_clk 0"

  run_binary(cmd_str, "mcpat", gem5_out_dir)

def wait_for_queue():
  max_queued = squeue_self_limit
  ask = True
  while ask:
    ask = False
    cmd = "squeue -u " + username + " -t pending | wc -l"
    # cmd = "./num_pending_jobs.sh"
    print(cmd.split())
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
      print(error)
      quit()
    print(output)
    queued = int(output)
    if queued >= max_queued:
      ask = True
      print("You have", queued, "queued requests. Let's wait for another second!\r", end=' ')
      sys.stdout.flush()
      sleep(1)
