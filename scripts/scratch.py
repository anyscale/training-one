
@ray.remote
class A:
    def __init__(self):
        self.n=0
    def count(self):
        self.n += 1
        return f"I have been called {self.n} times."
    def reset(self):
        self.n = 0
