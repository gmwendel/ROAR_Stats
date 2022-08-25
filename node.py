import subprocess
import re


class Node:
    def __init__(self, name):
        #Definitions
        self.name = name  # Node name, e.g.
        self.n_gpus = None  # Number of total GPUs on node
        self.gpu_type = None  # GPU Type on node (Assumes one type)
        self.n_cpus = None  # Number of total CPUs on node
        self.n_ram = None  # Total physical RAM in GB
        self.used_gpus = None  # Used GPUs on node
        self.used_cpus = None  # Used CPUs on node
        self.used_ram = None  # Used RAM on node in GB
        self.jobs = None  # Jobs currently running on node
        #Actions
        self._read_system_properties()  # acquire n_gpus,gpu_type,n_cpus, and n_ram
        self.update_state() #Get system stats on init

    def print_stats(self):
        print("{}: \t CPU: {}/{} \t RAM: {}G/{}G \t GPU: {}/{} \t {}.".format(self.name, self.used_cpus, self.n_cpus,
                                                                           self.used_ram, self.n_ram, self.used_gpus,
                                                                           self.n_gpus, self.gpu_type))

    def print_stats_verbose(self):

    def update_state(self):
        # Used to update the current state of the node (How many CPU, GPU, RAM)
        self.used_cpus = 0
        self.used_gpus = 0
        self.used_ram = 0
        # First grabs current jobs
        self.jobs = self._read_jobs()
        if len(self.jobs) > 0:
            for job in self.jobs:
                # Read utilization for each job running on node
                self.used_cpus += self._read_used_cpu(job)
                self.used_gpus += self._read_used_gpu(job)
                self.used_ram += self._read_used_ram(job)

    def _read_used_cpu(self, job):
        # Takes job number as input and returns number of CPUs used
        cmd = subprocess.run("qstat -f {} | grep 'req_information.lprocs.0'".format(job),
                             shell=True, stdout=subprocess.PIPE)
        out = cmd.stdout.decode('utf-8')
        return int(out.split(' ')[-1])

    def _read_used_gpu(self, job):
        # Takes job number as input and returns number of GPUs used
        cmd = subprocess.run("qstat -f {} | grep 'req_information.gpus.0'".format(job),
                             shell=True, stdout=subprocess.PIPE)
        out = cmd.stdout.decode('utf-8')
        if len(out) > 5:
            # Ensure a GPU was requested
            return int(out.split(' ')[-1])
        else:
            # If no GPU Requested grep will return nothing
            return 0

    def _read_used_ram(self, job):
        # Takes job number as input and returns RAM used in GB
        cmd = subprocess.run("qstat -f {} | grep 'req_information.total_memory.0'".format(job),
                             shell=True, stdout=subprocess.PIPE)
        out = cmd.stdout.decode('utf-8')
        ram = out.split(' ')[-1].strip()
        if ram[-2:] == 'kb':
            n_ram = int(ram[:-2]) / 1024 ** 2  # convert from kilobytes to gigabytes
            return round(n_ram, 1)
        else:
            raise ValueError(
                "expects string in form #kb, run qstat -f {} | grep 'req_information.total_memory.0' to check what happened".format(
                    job))

    def _read_jobs(self):
        cmd = subprocess.run("pbsnodes -a {} | grep 'jobs ='".format(self.name), shell=True, stdout=subprocess.PIPE)
        out = cmd.stdout.decode('utf-8')
        if len(out)>5:
            jobnames = out.split('.torque01.util.production.int.aci.ics.psu.edu,')
            jobs = [jobname.split("/")[-1] for jobname in jobnames]
            jobs[-1] = jobs[-1].strip()  # Remove \n from last job
            return jobs
        else:
            return []

    def _read_system_properties(self):
        self.n_gpus = self._read_n_gpus()
        if self.n_gpus > 0:  # only try to read gpu type if they exist
            self.gpu_type = self._read_gpu_type()
        self.n_cpus = self._read_n_cpus()
        self.n_ram = self._read_n_ram()

    def _read_n_gpus(self):
        cmd = subprocess.run("pbsnodes -a {} | grep 'gpus'".format(self.name), shell=True, stdout=subprocess.PIPE)
        out = cmd.stdout.decode('utf-8')
        if len(out)<1:
            return 0
        else:
            n_gpus = out.split(" ")[-1]
            return int(n_gpus)

    def _read_gpu_type(self):
        cmd = subprocess.run("pbsnodes -a {} | grep 'gc_'".format(self.name), shell=True, stdout=subprocess.PIPE)
        out = cmd.stdout.decode('utf-8').split("\n")
        gpu_type = out[0].split(",")[3]
        return gpu_type

    def _read_n_cpus(self):
        cmd = subprocess.run("pbsnodes -a {} | grep 'total_threads'".format(self.name), shell=True,
                             stdout=subprocess.PIPE)
        out = cmd.stdout.decode('utf-8')
        n_cpus = out.split(" ")[-1]
        return int(n_cpus)

    def _read_n_ram(self):
        cmd = subprocess.run("pbsnodes -a {} | grep 'physmem'".format(self.name), shell=True, stdout=subprocess.PIPE)
        out = cmd.stdout.decode('utf-8').split(",")
        for line in out:
            if re.search('physmem', line):
                ram = line.split("=")[-1]
                if ram[-2:] == 'kb':
                    n_ram = int(ram[:-2]) / 1024 ** 2  # convert from kilobytes to gigabytes
                    return round(n_ram, 1)
                else:
                    raise ValueError(
                        "expects string in form #kb, run pbsnodes -a {}} | grep 'physmem' to check what happened".format(
                            self.name))
