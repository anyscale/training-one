## Actor

@ray.remote
class Counter():
    def __init__(self):
        self.n = 0
    def work(self):
        self.n += 1
        print(f"I've been called {self.n} times.")
        return self.n

a = Counter.remote()
a.work.remote()
a.work.remote()
a.work.remote()
a.work.remote()
print(f"I did a total of {ray.get(a.work.remote())} calls.")

    
## PATTERN Tree of Actors
# https://docs.ray.io/en/master/ray-design-patterns/tree-of-actors.html

@ray.remote(num_cpus=1)
class Worker:
    def work(self):
        return "done"

@ray.remote(num_cpus=1)
class Supervisor:
    def __init__(self):
        self.workers = [Worker.remote() for _ in range(3)]
    def work(self):
        return ray.get([w.work.remote() for w in self.workers])

sup = Supervisor.remote()
print(ray.get(sup.work.remote()))  # outputs ['done', 'done', 'done']
