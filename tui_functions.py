import subprocess

#custom ping function, will ping with given address for 6 times at the moment
def pingcustom(address):
      output = subprocess.Popen(["ping", "-c", "6", address],
                                text=True,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE
      )

      for line in output.stdout:
            yield line.rstrip()

#custom ping function, will trace the given address
def tracecustom(address):
      output = subprocess.Popen(["tracepath", address],
                                text=True,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE
      )

      for line in output.stdout:
            yield line.rstrip()