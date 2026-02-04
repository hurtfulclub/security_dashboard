import subprocess

def pingcustom(address):
      output = subprocess.Popen(["ping", "-c", "6", address],
                                text=True,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE
      )

      for line in output.stdout:
            yield line.rstrip()

def tracecustom(address):
      output = subprocess.Popen(["tracepath", address],
                                text=True,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE
      )

      for line in output.stdout:
            yield line.rstrip()