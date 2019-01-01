import os
import sys
import subprocess
import errno
import getpass

# Paths
# m5_mcpat_path = os.environ['M5MCPATPATH']
# m5_mcpat_conversion_script = os.environ['M5TOMCPAT_CONVSCRIPT']
m5_path = os.environ['M5PATH']
mcpat_path = os.environ['MCPATPATH']
helpers_path = os.environ['HELPDIR']
username = getpass.getuser()
squeue_self_limit = 512

def run_binary(cmd_str, job_name, out_dir, mode="dryrun", append_to="jobs.log"):

  cmd_arr = []
  for q_index, qstr in enumerate(cmd_str.split("\"")):
    if q_index % 2 == 0:
      cmd_arr += qstr.split()
    else:
      cmd_arr.append('"'+qstr+'"')

  if "slurm" in mode:
    # wait_for_queue()
    print "Submitting the job:", cmd_str

    sbatch_str  = "sbatch --partition=slurm_part"
    sbatch_str += " --mincpus=1"
    # sbatch_str += " --mem=" + str(memory_estimate)
    sbatch_str += " --job-name="+job_name+"_"+out_dir
    sbatch_str += " --output="+out_dir+"/"+job_name+".stdout"
    sbatch_str += " --error="+out_dir+"/"+job_name+".stderr"
    sbatch_str += " "+helpers_path+"/srunbuf.sh "

    sbatch_arr = sbatch_str.split() + cmd_arr

    #Execute sbatch command
    process = subprocess.Popen(sbatch_arr, stdout=subprocess.PIPE)
    output, error = process.communicate()
    with open(out_dir+"/"+job_name+".slurmout", 'w+') as f:
      f.write(output)
      if error:
        f.write(error)

  elif "nonblocking" in mode:
    process = subprocess.Popen(cmd_arr, stdout=subprocess.PIPE)
    return process

  elif "blocking" in mode:
    print "Running the job:", cmd_str

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
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
      print error
      quit()
    # print output
    queued = int(output)
    if queued >= max_queued:
      ask = True
      print "You have", queued, "queued requests. Let's wait for another second!\r",
      sys.stdout.flush()
      sleep(1)
