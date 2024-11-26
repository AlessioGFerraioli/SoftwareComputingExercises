# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:55:56 2020

@author: aless



provo a fare l'esercizio proposto dal prof alla fine delle slide 2.3 random walk

ovvero prendere il random walk che abbiamo fatto a lezione e:
    
allow the user to specify the effect of the various transitions

return the simulation not as a list, but as a dedicated objct that can :
    be sliced over time: my_simulation[0.5:100.0]
    have a plot function dedicated
    automatically estimate the distribution

always include multiple runs of the simulation, an djoin this with point 2

"""



import numpy as np
import pylab as plt
import random as rn

import typing
from enum import Enum

from collections import Counter
import scipy.stats as st

#%%

''' questa parte dobrebbe essere user specified?? ma in che senso'''


#function of decay, returns the probability of decay that will be in our case state (number of particle) times 0.1
def removal(state):
    return state*0.5

# funciton of influx = returns 1 i.e. constant probability of change   also se è 0 ritorna zero
def increase(state):
    return 1 #if state>0 else 0

    

# we create a list of transitions where every element of the list is a function that represent a transition (we treat functions as variables, elements of the list - wooo powerful, vedremo meglio giovedì prossimo)
transitions = [removal, increase]
#we assign names to the element of the list (non è necessario, ma può essere comodo to have separate all the various transition and the effect of the system - i mean maybe ci sotanno due diverse transiztioni che increasano vbuo)
transitions_names = ['removal', 'increase']


#%%


class Transition(Enum):
    INCREASE = 'increase'
    DECREASE = 'removal'
    ABSORPION = 'absorbed'
    RINGTONE = 'ringtone'


class Observation(typing.NamedTuple):
    state: typing.Any     #what state am i at the moment
    time_of_observation: float   #what is the time i got inot the state
    time_of_residency: float    #how long havei stayed
    transition: Transition   #what is the transition that brought me out


#%%

''' questa è la funzione della simulation
n.b. non abbiamo ancora definito le transitions

 '''


def simulation(starting_state, time_limit, transitions, transitions_names):
    observed_states = []
    state = starting_state
    total_time = 0.0


    while total_time < time_limit:
        rates = [f(state) for f in transitions]
        total_rate = sum(rates)
        if total_rate>0:
            time = np.random.exponential(1/total_rate)
            event = rn.choices(transitions_names, weights=rates)[0]
        else:
            time = np.inf
            event = Transition.ABSORPION
        #fino a qui è tutto come il codice precedente
        
               
        # the fixed events overrides the others if they would happen before the chosen time
        time_ringtone = 1.0
        if total_time < time_ringtone and total_time + time > time_ringtone:
            time = time_ringtone - total_time
            event = Transition.RINGTONE
            
        observation = Observation(state, total_time, time, event)
        observed_states.append(observation)

        total_time += time
        
        if event == Transition.INCREASE:
            state += 1
        elif event == Transition.DECREASE:
            state -= 1
        elif event == Transition.ABSORPION or event == Transition.RINGTONE:
            pass
        else:
            raise ValueError("transition not recognized")
    return observed_states


#%%
    
def plot_observations(observation_sequence, ax=None):
    if ax is None:
        ax = plt.gca()
    values = [obs.state for obs in observation_sequence]      # prende i values one at a time
    times = [obs.time_of_observation for obs in observation_sequence]   # prende i times one at a time
    ax.plot(times, values, linestyle='steps-post')      # draws the states, connected by a straight line
    
    
#%%
    
class Result:
   
    
    def __init__(self, starting_state, time_limit, transitions, transitions_names, simulation_runs):
        self.starting_state = starting_state   #initial state of the system
        self.time_limit = time_limit          # max time limit of the simulation, the time at which it stops if nothing else has stopped it before (e.g. an absorption state)
        self.transitions = transitions
        self.transitions_names = transitions_names
        self.observed_states = []             # list of named tuple containing the outcome of the simulation
        self.absorpion_time : float       # time at which the absorption transition happens, i.e. the simulation actually stops
        self.observed_states_w_time = [[],[]]    # 2dim array: first [] is equally spaced times (we define in get_result); second [] is the corresponding state at that time. this allows us to slice our outcome states with respect to time and ask questions such as: "at time = t what was the state?"
        self.simulation_runs = simulation_runs     # number of multiple simulation runs : a good simulation must be ran at least 3 times to ensure there are no problems
   
       
        
    def print_first_k(self, k):
        for observation in self.observed_states[:k]:
            print(observation)
            print()
    
  
    
    def get_result(self):
        # i do the actual simulation 
        self.observed_states = simulation(self.starting_state, self.time_limit, self.transitions, self.transitions_names)
        
        # i save the absorption time, which is the time of observation of the last element of the list observed_states
        self.absorpion_time = self.observed_states[-1].time_of_observation
        
        # i define the first [] of observed_states_w_time as 100 equally spaced times over the interval 0,absorpion time. why 300? because THIS IS SPARTAAAA
        self.observed_states_w_time[0] = np.linspace(0, self.absorpion_time, 100)
        #qua scrivo un piccolo codice per assegnare a ogni tempo di osservazione (prima colonna di observed_state_w_time) il corretto state
        
        #devo viaggiare lungo gli elementi di observed states w time, quindi una riga i alla volta
        #magari domani facciamolo con un np.array viene meglio
        for i in range(len(self.observed_states_w_time[0])):
        #per ogni riga devo vedere quanto è il tempo (quindi l'elemento della prima colonna, riga i)
        #e confrontare questo tempo con il tempo della prima osservazione di observed_states
        #per essere quello che mi interessa, il tempo che sto guardando deve essere compreso tra time of observation e time of obs + time of residency
        #se ciò è vero, devo salvare il corrispondente stato nella riga in cui mi trovo, alla colonna due
            for j in range(len(self.observed_states)):    
                if self.observed_states_w_time[0][i]>=self.observed_states[j].time_of_observation and self.observed_states_w_time[0][i]<self.observed_states[j].time_of_observation + self.observed_states[j].time_of_residency:
                    self.observed_states_w_time[1].append(self.observed_states[j].state)
                    if self.observed_states[j].transition == Transition.ABSORPION:
                        i = 1001
                    break
              
            
          #  if self.observed_states_w_time[1][i] == 0:
           #     break
                  
                    
        
        #una volta fatto ciò devo aggiornare una variabile interna mia che mi tiene conto di quale punto di observed_states mi trovo, così per la prossima riga mi basta cominciare a controllare da quello, non ho bisogno di andare a quelli precedenti
        #cioè, mi tengo il conto e se il tempo (colonna 1, riga i) è ancora lo stesso devo salvare lo stesso state precedente, sennò vuol dire che mi trovo in un successivo state e salvare quello
        
        
    def plot_observations(self, ax=None):
        
        for i in range(self.simulation_runs):
            self.get_result()
        
        if ax is None:
               ax = plt.gca()
        
        values = [obs.state for obs in self.observed_states]      # prende i values one at a time
        times = [obs.time_of_observation for obs in self.observed_states]   # prende i times one at a time
        ax.plot(times, values, linestyle='steps-post')      # draws the states, connected by a straight line    
        
        
        
    def generate_distribution(self):
        distribution = Counter()
        for i in range(len(self.observed_states)-1):
            state = self.observed_states[i].state
            residency_time = self.observed_states[i].time_of_residency
            distribution[state] += residency_time           #qua sommo senza noralizzare
            '''
            print('step n. =', i)
            print('state')
            print(state)
            print('residency_time')
            print(residency_time)
            print()
            print('total residency_time up to now for this state')
            print(distribution[state])
            print()
            print('.......')
            print()
            '''
            
        total_time_observed = sum(distribution.values())     #normalizzo qui alla fine della somma
        for state in distribution:
            distribution[state] /= total_time_observed
        return distribution      
        
    def plot_distribution(self):
        
        distribution = self.generate_distribution()
        
                
        fig, ax = plt.subplots()
        ax.bar(distribution.keys(), distribution.values())     #this is the plot of our values

        # corresponding poisson distribution
        values = np.arange(20)
        pmf = st.poisson(2.5).pmf(values)
        ax.bar(values, pmf, alpha=0.5)        #this is the plot of the corresponding poisson distributoin

        
     
    
#%%

result_test = Result(5, 1000, [removal, increase], [Transition.DECREASE, Transition.INCREASE], 5)

#result_test.get_result()
'''
for observation in result_test[:5]:
    print(observation)
    print()
''' 


result_test.print_first_k(5)

fig, ax = plt.subplots()
result_test.plot_observations()


#%%

result_test.plot_distribution()


#%%

#distribution = result_test.generate_distribution()