import pandas
import math
from triangulation import Triangle, ANGLE_UNIT_RAD
from collections import defaultdict
import random
import matplotlib.pyplot as plt


class Solver:
    def __init__(self, triangles):
        self.triangles = triangles
        self.solved_vertices = defaultdict(list) # L'ensemble des coordonnées déjà découvertes ? Ou des cotés déjà découverts ? 

    def solve(self, bootstrap):
        #assert(len(bootstrap) == 2) # Comment tot

        self._update_positions(bootstrap)
        self._solve_loop()

    def _update_positions(self, pos_dic):
        for v, pos in pos_dic.items():
            if v in self.solved_vertices.keys():
                raise ValueError("%s should not be in solved_vertices" % v)
            self.solved_vertices[v] = pos
        
            eligible = [t for t in self.triangles if not t.isSolved() and v in t.sommets]
            for t in eligible:
                if v in t.positions.keys():
                    raise ValueError("%s should not already be set in the triangle %s" % (v, str(t)))
                t.setPosition(v,*pos)


    def _solve_loop(self):
        while True:    
            # Randomly pick a triangle to solve
            pending = self.triangles.apply(lambda t: t.isSolvable() and not t.isSolved())
        
            # Stop when nothin is left to solve
            if not pending.any():
                break

            tpick = self.triangles.loc[pending].sample(n=1).iloc[0]

            # Get the positions to be solved
            unknown_pos = tpick.sommets - tpick.positions.keys()

            tpick.solve()

            # Update the solved_vertices and triangles vertices with the newly computed positions
            update = {k: v for k,v in tpick.positions.items() if k in unknown_pos}
            self._update_positions(update)


def to_decimal(d,m,s): return d + m/60. + s/3600.

def to_radians(dec): return dec * math.pi / 180.

def make_triangle(group):
    vertices = list(group["nom du point"])
    angles = list(group["rads"])
    t = Triangle(vertices)
    t.setAngles(angles, unit=ANGLE_UNIT_RAD) 
    return t

def verniquet_own_solution(angles_data):

    triangles = list(data.groupby(angles_data.index // 3).apply(make_triangle))
    
    triangles[0].setPosition("Observatoire", Y=0.00541)
    triangles[0].setPosition("Piramide", Y = 20)
    triangles[0].solve()

    triangles[1].setPosition("Observatoire", Y=0.00541)
    triangles[1].setPosition("Piramide", Y = 20)
    triangles[1].solve()

    triangles[2].setPosition("Piramide", Y = 20)
    triangles[2].setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
    triangles[2].solve()

    triangles[3].setPosition("Observatoire", Y=0.00541)
    triangles[3].setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
    triangles[3].solve()

    triangles[4].setPosition("Piramide", Y = 20)
    triangles[4].setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
    triangles[4].solve()

    triangles[5].setPosition("Observatoire", Y=0.00541)
    triangles[5].setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
    triangles[5].solve()

    triangles[6].setPosition("Observatoire", Y=0.00541)
    triangles[6].setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
    triangles[6].solve()

    triangles[7].setPosition("Piramide", Y = 20)
    triangles[7].setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
    triangles[7].solve()

    triangles[8].setPosition("Observatoire", Y=0.00541)
    triangles[8].setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
    triangles[8].solve()

    triangles[9].setPosition("St Sulpice", X = -0.611685, Y = 5.703124)
    triangles[9].setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
    triangles[9].solve()

    triangles[10].setPosition("St Sulpice", X = -0.611685, Y = 5.703124)
    triangles[10].setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
    triangles[10].solve()

    triangles[11].setPosition("Observatoire", Y=0.00541)
    triangles[11].setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
    triangles[11].solve()

    triangles[12].setPosition("Observatoire", Y=0.00541)
    triangles[12].setPosition("St Sulpice", X = -0.611685, Y = 5.703124)
    triangles[12].solve()

    triangles[13].setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
    triangles[13].setPosition("St Sulpice", X = -0.611685, Y = 5.703124)
    triangles[13].solve()

    triangles[14].setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
    triangles[14].setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
    triangles[14].solve()

    triangles[15].setPosition("Piramide", Y = 20)
    triangles[15].setPosition("St Sulpice", X = -0.611685, Y = 5.703124)
    triangles[15].solve()

    triangles[16].setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
    triangles[16].setPosition("St Sulpice", X = -0.611685, Y = 5.703124)
    triangles[16].solve()

    triangles[17].setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
    triangles[17].setPosition("Piramide", Y = 20)
    triangles[17].solve()

    triangles[18].setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
    triangles[18].setPosition("Porte St Denis", X = 4.175919, Y = 13.001454)
    triangles[18].solve()

    output = defaultdict(list)
    for t in triangles:
        for v, pos in t.positions.items():
            output[v].append(pos)

    # Arithmetic mean
    for v, pos in output.items():
        x  =[p[0] for p in pos]
        y  =[p[1] for p in pos]
        yield v, sum(x) / len(x), sum(y) / len(y)



if __name__ == "__main__":
    data = pandas.read_csv("angles_orientes.dat", skiprows=1)
    
    # Convert angles to radians
    # We care only about augmented angles
    data["rads"] = data[["d","m","s"]].apply(lambda a: to_radians(to_decimal(a[0], a[1], a[2])),  axis=1)

    # Feed the solver all the triangles
    N = 10
    
    x = defaultdict(list)
    y = defaultdict(list)

    for i in range(N):
        # Pack rows by 3 to create triangles from vertices and augmented angles
        triangles = data.groupby(data.index // 3).apply(make_triangle)
        triangles.index += 1 # Match index with the column "num_triangle" from data

        s = Solver(triangles)
        
        s.solve({"Observatoire": [0,0.00541],"Piramide" : [0,20]})

        for k, v in s.solved_vertices.items():
            x[k].append(v[0])
            y[k].append(v[1])

    # VERNIQUET's OWN SOLUTION
    # FIXME what if the solution is already in the computed set ?
    for k, pos_x, pos_y in verniquet_own_solution(data):
        x[k].append(pos_x)
        y[k].append(pos_y)

    x = pandas.DataFrame(x)
    y = pandas.DataFrame(y)


    # ~~~~~~~~~~~~~~~~~~~~
    # PLOT
    
    # Center x 
    # x=(x-x.mean())/x.std()
    xm = x.mean()
    x = x-xm

    # Center y
    # y=(y-y.mean())/y.std()
    ym = y.mean()
    y = y-ym
    
    # Plot
    fig, axes = plt.subplots(1,2) 
    x.boxplot(ax=axes[0],sym='+', flierprops={"markersize":3})
    y.boxplot(ax=axes[1],sym='+', flierprops={"markersize":3})

    for k, vx, vy in verniquet_own_solution(data):
        xpos = x.columns.get_loc(k) + 1
        axes[0].plot(xpos, vx - xm.iloc[xpos-1], 'r.', alpha=0.5)
        axes[1].plot(xpos, vy - ym.iloc[xpos-1], 'r.', alpha=0.5)


    axes[0].title.set_text('X')
    axes[1].title.set_text('Y')
    axes[0].tick_params('x',labelrotation=45)
    axes[1].tick_params('x',labelrotation=45)

    plt.tight_layout()
    plt.show()
