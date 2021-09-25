import numpy as np
import matplotlib.pyplot as plt

N = 10 # number of periods
p = 0.00 # probability of slashing
s = .05 # slashing penalty (percentage)
R0 = 10

index = np.arange(N) # array with indexes representing id of each staker
bool_array = [True, False]

def constant_reward(stake: int, period: int, total_period: int) -> float:
    """
    # Constant Reward

    Calculates the constant reward for a given stake and period.

    ### Args:
    - stake (int): stake of the chosen staker.
    - period (int): current period.
    - total_period (int): total number of periods.
    """
    return R0

def decreasing_reward(stake: int, period: int, total_period: int) -> float:
    """
    # Decreasing Reward

    Calculates the decreasing reward for a given stake and period.

    ### Args:
    - stake (int): stake of the chosen staker.
    - period (int): current period.
    - total_period (int): total number of periods.
    """
    return R0 * (1 - (period / total_period))

def geometric_reward(stake: int, period: int, total_period: int) -> float:
    """
    # Geometric Reward

    Calculates the geometric reward for a given stake and period.

    ### Args:
    - stake (int): stake of the chosen staker.
    - period (int): current period.
    - total_period (int): total number of periods.
    """
    power = stake / 10
    return R0 * (1 - (period / total_period) ** power)

def simulation(period = 200, reward_function = constant_reward):
    """ 
    # Simulation of Proof Of Stake
    
    Simulates the slashing and reward mechanism of Proof of Stake for a given period.

    ### Args:
    - period (int): number of periods to simulate.
    """
    stakes = np.zeros((period, N))
    stakes[0,:] = np.random.random(N) * 100 + 1
    # stakes[0, 3] = 300
    for t in range(1, period):
        chosen = np.random.choice(index, p = stakes[t-1,:]/np.sum(stakes[t-1,:]))
        stakes[t,:] = stakes[t-1,:]
        if np.random.choice(bool_array, p=[p, 1 - p]) == True: # slash
            stakes[t,chosen] = stakes[t,chosen] * (1-s)
        else:
            r = reward_function(stakes[t,chosen], t, period)
            stakes[t,chosen] = stakes[t,chosen] + r
    return stakes

def delta_first_last(stakes: np.ndarray):
    """
    # Delta Between First and Last

    Calculates the delta between the first and last staker.

    ### Args:
    - stakes (np.ndarray): array of stakes for each period.
    """
    delta = np.zeros(stakes.shape[0])
    for i in range(stakes.shape[0]):
        line = stakes[i,:]
        delta[i] = np.max(line) - np.min(line)
    return delta

def delta_first_second(stakes: np.ndarray):
    """
    # Delta Between First and Second
    
    Calculates the delta between the first and second staker.

    ### Args:
    - stakes (np.ndarray): array of stakes for each period.
    """
    delta = np.zeros(stakes.shape[0])
    for i in range(stakes.shape[0]):
        line = stakes[i,:]
        sorted = np.sort(line)[::-1]
        delta[i] = sorted[0] - sorted[1]
    return delta

def trace_plot(title, x_axis_title, y_axis_title, data):
    plt.figure()
    plt.plot(data)
    plt.title(title)
    plt.xlabel(x_axis_title)
    plt.ylabel(y_axis_title)
    plt.show()

if __name__ == "__main__":
    stakes = simulation(period=100000, reward_function=constant_reward)
    delta_to_last = delta_first_last(stakes)
    delta_to_second = delta_first_second(stakes)
    trace_plot("Evolution of the stake for each mines", "Time", "Stake", stakes)
    trace_plot("Delta to last", "Period", "Delta", delta_to_last)
    trace_plot("Delta to second", "Period", "Delta", delta_to_second)
