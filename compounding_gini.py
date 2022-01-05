import numpy as np
import matplotlib.pyplot as plt

def gini_coefficient(x: np.ndarray) -> float:
    """
    Calculate the Gini coefficient of a distribution.
    Parameters
    ----------
    x : np.ndarray
        Array of values.
    Returns
    -------
    float
        Gini coefficient.
    """
     # Mean absolute difference
    mad = np.abs(np.subtract.outer(x, x)).mean()
    # Relative mean absolute difference
    rmad = mad/np.mean(x)
    # Gini coefficient
    g = 0.5 * rmad
    return g


SLASING_PROB = 0.1
REWARD = .5
SLASHING_RATE = 0.1

def loop(stakes: np.ndarray) -> np.ndarray:
    # Choose random validator according to stake distribution
    validator = np.random.choice(np.arange(len(stakes)), replace=True, p=stakes/stakes.sum())
    slashed = np.random.binomial(1, SLASING_PROB, size=len(stakes))
    stakes[slashed] *= (1 - SLASHING_RATE)
    if validator not in slashed:
        stakes[validator] += REWARD
    return stakes

def main():
    stakes = np.random.exponential(size=100, scale=1)
    gini = []
    for i in range(100):
        stakes = loop(stakes)
        gini.append(gini_coefficient(stakes))
    plt.plot(gini)
    plt.title('Gini coefficient over time')
    plt.xlabel('Iteration')
    plt.ylabel('Gini coefficient')
    plt.show()

if __name__ == '__main__':
    main()
