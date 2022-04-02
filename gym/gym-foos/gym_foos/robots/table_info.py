rods=[[0,1,3,5],[7,6,4,2]]
rodm=[3,2,3,5,5,3,2,3]
rodp=[1,1,2,1,2,1,2,2]
goal_width = 0.4
goal_offset = .02
ball_width = .04

metersPerInch = 0.0254
goalieDistance =   8.125*metersPerInch
twomanDistance =   9.500*metersPerInch
fivebarDistance =  4.750*metersPerInch
threemanDistance = 7.250*metersPerInch

tableWidth = 48 * metersPerInch
tableDepth = 27 * metersPerInch
tableHeight = 6.25 * metersPerInch #4.25 * metersPerInch
wall = 1 * metersPerInch
goalWidth = 8.25 * metersPerInch
goalHeight = 3 * metersPerInch
rodDistance = 6 * metersPerInch
rodLength = 60 * metersPerInch
rodDiameter = 3/8 * metersPerInch
manWidth = 1 * metersPerInch
manDepth = 0.5 * metersPerInch
manHeight = 4.0 * metersPerInch
manOffset = 1.0 * metersPerInch

def tran_limit(numMen, manDistance):
    tableDepth = 27 * metersPerInch
    manWidth = 1 * metersPerInch
    menWidth = (numMen - 1) * manDistance + manWidth
    return (tableDepth - menWidth) / 2

tran_limits = [ tran_limit(3, goalieDistance),
                tran_limit(2, twomanDistance),
                tran_limit(3, threemanDistance),
                tran_limit(5, fivebarDistance),
                tran_limit(5, fivebarDistance),
                tran_limit(3, threemanDistance),
                tran_limit(2, twomanDistance),
                tran_limit(3, goalieDistance) ]