import subprocess

def ping8888():
      output = subprocess.Popen(["ping", "-c", "6", "8.8.8.8"],
                                text=True,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE
      )

      for line in output.stdout:
            yield line.rstrip()

def trace8888():
      output = subprocess.Popen(["tracepath", "8.8.8.8"],
                                text=True,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE
      )

      for line in output.stdout:
            yield line.rstrip()

def pinggoogle():
      output = subprocess.Popen(["ping", "-c", "6", "google.com"],
                                text=True,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE
      )

      for line in output.stdout:
            yield line.rstrip()

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