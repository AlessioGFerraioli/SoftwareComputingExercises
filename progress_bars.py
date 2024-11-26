# progress bars
from plumbum.cli.terminal import Progress
import time

for i in Progress.range(10):
    time.sleep(0.2)