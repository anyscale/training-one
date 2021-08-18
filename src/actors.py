
# Imports
import ray
import time
ray.init(address="auto", namespace="actors")

## Actors
# Actors are remote objects with state and methods.  
# Ray negotiates the relationship between actor references

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

## Instantiating

@ray.remote
class Friend():
    def __init__(self, name):
        self.name = name
        self.friends = set()
    def addFriend(self, other):
        self.friends.add(other)
    def getName(self):
        return self.name
    def display(self):
        return f"{self.name}: {[ray.get(f.getName.remote()) for f in self.listFriends()]}"
    def listFriends(self):
        return self.friends

@ray.remote
def meet(p1, p2):
    p1.addFriend.remote(p2)
    p2.addFriend.remote(p1)

f1 = Friend.remote("Randolph")
f2 = Friend.remote("Dexter")
f3 = Friend.remote("Molecule")
meet.remote(f1,f2)
meet.remote(f1,f3)
labels = [ray.get(x.display.remote()) for x in [f1, f2, f3]]
print(labels)

labels = [ray.get(x.display.remote()) for x in [f1, f2, f3]]
        
## Naming Actors

named_actor = Friend.options(name="Randolph").remote("Randolph's name")

fetch_an_actor = ray.get_actor("Randolph")
    
## Actor Scope

@ray.remote
def spawn():
    f = Friend.options(name="Jo").remote("Jo")

ray.get(spawn.remote())
jo = ray.get_actor("Jo")  # ERROR

# detach it and force evaluation to 'save' it to the container for shared use
@ray.remote
def spawn_really():
    f = Friend.options(name="Bev", lifetime="detached").remote("Bev")

ray.get(spawn_really.remote())
bev = ray.get_actor("Bev")


## Detatched Actors


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
