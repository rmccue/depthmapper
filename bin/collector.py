# Path hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import depthmapper.collector as collector

filename = "snap.data"
if len(sys.argv) > 1:
	filename = sys.argv[1]

collector.setup()
snapshot = collector.snapshot()
collector.teardown()
collector.save(snapshot, filename)
