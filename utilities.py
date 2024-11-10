class Formation():
    
    def __init__(self, d, m, a):
        self.d = d
        self.m = m
        self.a = a
        self.name = f"{d}-{m}-{a}"
    
    def __repr__(self):
        return f"Formation({self.name})"

f1 = Formation(4, 3, 3)
print(f1)