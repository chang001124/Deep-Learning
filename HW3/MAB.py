import numpy as np, math, matplotlib.pyplot as plt
import numpy as np
np.random.seed(42)
k=10
true_probs= np.random.rand(k)
true_probs

class EpsilonGreedy:
    def __init__(self,k,eps):
        self.k=k
        self.eps=eps
        self.counts=np.zeros(k)
        self.values=np.zeros(k)
    def select(self,t):
        if np.random.rand()<self.eps:
            return np.random.randint(self.k)
        return np.argmax(self.values)
    def update(self,arm,r):
        self.counts[arm]+=1
        n=self.counts[arm]
        self.values[arm]+= (r - self.values[arm])/n
class UCB1:
    def __init__(self,k,c):
        self.k=k
        self.c=c
        self.counts=np.zeros(k)
        self.values=np.zeros(k)
    def select(self,t):
        for arm in range(self.k):
            if self.counts[arm]==0:
                return arm
        ucb=self.values + self.c*np.sqrt(np.log(t+1)/self.counts)
        return np.argmax(ucb)
    def update(self,arm,r):
        self.counts[arm]+=1
        n=self.counts[arm]
        self.values[arm]+= (r - self.values[arm])/n
class Softmax:
    def __init__(self,k,tau):
        self.k=k
        self.tau=tau
        self.counts=np.zeros(k)
        self.values=np.zeros(k)
    def select(self,t):
        prefs=np.exp(self.values/self.tau)
        probs=prefs/prefs.sum()
        return np.random.choice(self.k, p=probs)
    def update(self,arm,r):
        self.counts[arm]+=1
        n=self.counts[arm]
        self.values[arm]+= (r - self.values[arm])/n
class Thompson:
    def __init__(self,k):
        self.k=k
        self.alpha=np.ones(k)
        self.beta=np.ones(k)
    def select(self,t):
        samples=np.random.beta(self.alpha, self.beta)
        return np.argmax(samples)
    def update(self,arm,r):
        if r==1:
            self.alpha[arm]+=1
        else:
            self.beta[arm]+=1
def draw(arm):
    return 1 if np.random.rand()<true_probs[arm] else 0
algos={"eps":EpsilonGreedy(k,0.1),"ucb":UCB1(k,2),"soft":Softmax(k,0.1),"ts":Thompson(k)}
n=5000
results={}
for name,alg in algos.items():
    rewards=[]
    for t in range(n):
        arm=alg.select(t)
        r=draw(arm)
        alg.update(arm,r)
        rewards.append(r)
    results[name]=np.array(rewards)
for name,rewards in results.items():
    print(name,rewards.mean())
