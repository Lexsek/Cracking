from z3 import *

# Return a number of Int variables in a list
def initVars(name: str, counter: int) -> list:
    return [Int('%s%d' % (name, i)) for i in range(counter)]

# Add contraints to variables, only letters between 'a' and 'z'
def varConstraint(var, s):
    for v in var:
        s.add(v > 0x60)
        s.add(v < 0x7A)

# InvalidCheck::checkSum(void)
def checksumSum(var):
    checksumEqu = 0
    for v in var:
        checksumEqu += (v - 0x60)
    return checksumEqu

# InvalidCheck::checkProduct(void)
def checksumMul(var):
    checksumEqu = 1
    for v in var:
        checksumEqu *= (v - 0x60)
    return checksumEqu

# Format solution
def formatSolution(model):
    res = []
    for var in str(model)[1:-1].split(','):
        res.append(chr(int(var[var.find('=') + 2:])))
    print("password is : {}".format(''.join(res)))


s = Solver()                       # Create a solver

var = initVars('x', 6)             # Initialize 6 Int variables in a list
varConstraint(var, s)              # Add constraints to var (only lowcase letters)

s.add(checksumSum(var) == 0x2C)    # InvalidCheck::checkSum(void)
s.add(checksumMul(var) == 0x3F48)  # InvalidCheck::checkProduct(void)

if s.check() == sat:               # Check if equation is solvable
    print("Solved !")
    formatSolution(s.model())      # Format the solution
else:
    print("unsat")
