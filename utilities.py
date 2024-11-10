import math
import pandas as pd

class Formation():
    
    def __init__(self, d, m, a):
        self.d = d
        self.m = m
        self.a = a
        self.name = f"{d}-{m}-{a}"
    
    def __repr__(self):
        return f"Formation({self.name})"

class Team(): 
    
    def __init__(self, team_name: str, formation: Formation):
        self.team_name = team_name
        self.formation = formation

        # Stats from file for attack, defense, midfield
        self.d = None
        self.m = None
        self.a = None
    
    def load_stats_from_file(self, filename: str) -> None:
        data = pd.read_csv(filename)
        
        self.d = s(self.team_name, "DefenseStat", data)
        self.m = s(self.team_name, "MidfieldStat", data)
        self.a = s(self.team_name, "AttackStat", data)
    
    def __repr__(self): 
        return f"{self.team_name} playing {self.formation}"
        
def diminishing_returns(x: int) -> float:
    return 1 - math.e ** (-0.7 * x)  

def utility(G1: int, G2: int, t1: Team, t2: Team) -> float:
    a_1 = t1.a * diminishing_returns(t1.formation.a)
    a_2 = t2.a * diminishing_returns(t2.formation.a)
    d_1 = t1.d * diminishing_returns(t1.formation.d)
    d_2 = t2.d * diminishing_returns(t2.formation.d)

    return G1 - G2 + a_1 * (1 / d_2) + d_1 * (1/ a_2)

def s(t: str, p: str, data: pd.DataFrame) -> float: 
    row = data.loc[data['TeamName'] == t]
    if not row.empty:
        try: 
            return float(row[p].iloc[0]) / 100
        except KeyError: 
            raise Exception(f"Could not find {p} for team: {t}")
    raise Exception(f"Could not find data for team: {t}")

if __name__ == "__main__":
    
    t1 = Team("ManchesterCity", Formation(4, 3, 3))
    t2 = Team("FCDallas", Formation(4, 4, 2))
    t1.load_stats_from_file("./team_data.csv")
    t2.load_stats_from_file("./team_data.csv")

    print(utility(0, 0, t1, t2))
    print(utility(0, 0, t2, t1))
    
    print(t1)