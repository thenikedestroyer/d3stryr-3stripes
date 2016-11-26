# Lets try to keep a revision tracking via commit number.
from subprocess import Popen, PIPE

# $ git rev-list <branch> --count # retrieves full commit count of HEAD (master)
process = Popen(['git', 'rev-list', 'HEAD', '--count'], stdout=PIPE, stderr=PIPE)

 # use .join for O(n) time complexity (concatenation would be O(n^2))
revision = ''.join ([ 'c+', process.communicate () [0].strip () ])

# Set this for parameters checking
hypedSkus = ['BY9612', 'BY1605', 'BY9611']

# Code to indicate a shitty exit from the script
exitCode = 1
