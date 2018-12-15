import os 
import sys
import subprocess

# Paths
m5_mcpat_path = os.environ['M5MCPATPATH']
m5_path = os.environ['M5PATH']
mcpat_path = os.environ['MCPATPATH']


def run_binary(cmd_str, job_name, out_dir, is_slurm_job=False):
  if is_slurm_job: 
    print "Submitting the job:", cmd_str
 
    sbatch_str  = "sbatch --partition=slurm_part" 
    sbatch_str += " --mincpus=1"
    # sbatch_str += " --mem=" + str(memory_estimate)
    sbatch_str += " --job-name="+job_name+"_"+out_dir
    sbatch_str += " --output="+out_dir+"/"+job_name+".stdout"
    sbatch_str += " --error="+out_dir+"/"+job_name+".stderr"
    sbatch_str += " ./srunbuf.sh " + cmd_str
    
    #Execute sbatch command
    process = subprocess.Popen(sbatch_str.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    with open(out_dir+"/"+job_name+".slurmout", 'w+') as f:
      f.write(output)
      if error:
        f.write(error)
  else:
    print "Running the job:", cmd_str
    process = subprocess.Popen(cmd_str.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    with open(out_dir+"/"+job_name+".stdout", 'w+') as f:
      f.write(output)
    
    if error: 
      with open(out_dir+"/"+job_name+".stderr", 'w+') as f:
        f.write(error)

    
def mkdir_p(directory):
  try:
    os.makedirs(directory)
  except OSError as exc:  # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(directory):
      pass
    else:
      raise



def convert_gem5_mcpat(gem5_out_dir):
  # ./gem5McPATparse -x template.xml -c config.ini -s stats.txt -o out.xml
  cmd_str = m5_mcpat_path+"/gem5McPATparse"
  cmd_str += " -x " + m5_mcpat_path + "/template.xml"
  cmd_str += " -c " + gem5_out_dir + "/config.ini"
  cmd_str += " -s " + gem5_out_dir + "/stats.txt"
  cmd_str += " -o " + gem5_out_dir + "/mcpat.xml"
  
  run_binary(cmd_str, "gem5mcpat", gem5_out_dir)


def run_mcpat(gem5_out_dir):
  # mcpat -infile <input file name>  -print_level < level of details 0~5 >  -opt_for_clk < 0 (optimize for ED^2P only)/1 (optimzed for target clock rate)>
  cmd_str = mcpat_path + "/mcpat"
  cmd_str += " -infile " + gem5_out_dir+"/mcpat.xml"
  cmd_str += " -print_level 1"
  cmd_str += " -opt_for_clk 0"

  run_binary(cmd_str, "mcpat", gem5_out_dir)
