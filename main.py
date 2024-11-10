from utilities import Formation, Team

if __name__ == "__main__": 
    
    allowed_formation = [
        Formation(4, 3, 3),
        Formation(4, 4, 2),
        Formation(5, 3, 2),
        Formation(4, 5, 1),
    ]

    t1 = Team("ManchesterCity", Formation(4, 3, 2))
    t2 = Team("FCDallas", Formation(4, 5, 1))
    t1.load_stats_from_file("./team_data.csv")
    t2.load_stats_from_file("./team_data.csv")