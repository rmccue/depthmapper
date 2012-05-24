# Path hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import depthmapper.displayer as displayer

filename = "snap.data"
if len(sys.argv) > 1:
	filename = sys.argv[1]

app = displayer.DisplayApplication()
app.cloud = displayer.load(filename)
app.go()
