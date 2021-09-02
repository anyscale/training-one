## Notebook Two Actors

# Imports
import ray
import time
ray.init(address="auto", namespace="actors")

## Actors are remote objects with state and methods.  
# You create an actor by instantiating a remote object

# This actor counts how many times it has been invoked
@ray.remote
class Counter():
    def __init__(self, name):
        self.name = name
        self.n = 0
    def work(self):
        self.n += 1
        print(f"Counter {self.name} has been called {self.n} times.")
        return self.n

a = Counter.remote("a")
a.work.remote()
a.work.remote()
a.work.remote()
a.work.remote()
print(f"I did a total of {ray.get(a.work.remote())} calls.")

# We'll make a few copies of it to demonstrate
a = Counter.remote("a")
b = Counter.remote("b")
c = Counter.remote("c")

a.work.remote()
a.work.remote()
b.work.remote()
c.work.remote()
c.work.remote()
c.work.remote()

# As with tasks, there are certain things you cannot do with Actors:

# x = Counter()

# x = Counter.remote()
# x.work()

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

# A task to introduce two people to each other
@ray.remote
def meet(p1, p2):
    p1.addFriend.remote(p2)
    p2.addFriend.remote(p1)

f1 = Friend.remote("Randolph")
f2 = Friend.remote("Dexter")
f3 = Friend.remote("Molecule")
meet.remote(f1,f2)
meet.remote(f1,f3)

# Let's take a look at the values
ray.get(f1.getName.remote())

# let's see if everyone is hooked up
labels = [ray.get(x.display.remote()) for x in [f1, f2, f3]]
labels
        

## Actors can interact
# Pass object references between actor methods.  Actors know to operate
# on the remote object

@ray.remote
class Rock:
    def __init__(self):
        self.location = 0
    def move(self):
        self.location += 1
    def locate(self):
        return f"{self.location} feet from home."

@ray.remote
class RockPusher:
    def push_the_rock(self, rock):
        rock.move.remote()
        ray.get(rock.locate.remote())  # force evaluation

rock = Rock.remote()
pusherA = RockPusher.remote()
pusherB = RockPusher.remote()

pusherA.push_the_rock.remote(rock)
pusherA.push_the_rock.remote(rock)
pusherB.push_the_rock.remote(rock)
pusherA.push_the_rock.remote(rock)
pusherA.push_the_rock.remote(rock)

#time.sleep(1)
ray.get(rock.locate.remote())
        



## Naming Actors
@ray.remote
class Shouter():
    def __init__(self, words):
        self.words = "HEY " + words + "!"
    def shout(self):
        return self.words
    def work(self):
        self.words += "THERE!"
        return self.words
named_actor = Shouter.options(name="Randolph").remote("YOU")
ray.get(named_actor.shout.remote())

r2 = ray.get_actor("Randolph")
ray.get(r2.work.remote())

    
## Actor Scope

@ray.remote
def spawn():
    f = Friend.options(name="Jo").remote("Jo")

ray.get(spawn.remote())
try:
    jo = ray.get_actor("Jo")  # ERROR
except ValueError as e:
    print(e)

## Detach an actor and it will stick around (in the active namespace)
@ray.remote
def spawn_really():
    f = Friend.options(name="Bev", lifetime="detached").remote("Bev")

ray.get(spawn_really.remote())
bev = ray.get_actor("Bev")




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
print(ray.get(sup.work.remote()))  


## PATTERN Signal Actor
# This actor's purpose is to make sure it blocks until some important resource is ready

from ray.test_utils import SignalActor

@ray.remote
def wait_and_go(signal):
    ray.get(signal.wait.remote())

    print("go!")
    return "I went."

signal = SignalActor.remote()
tasks = [wait_and_go.remote(signal) for _ in range(4)]
print("ready...")
# Tasks will all be waiting for the signals.
print("set..")
ray.get(signal.send.remote())

# Tasks are unblocked.
ray.get(tasks)
