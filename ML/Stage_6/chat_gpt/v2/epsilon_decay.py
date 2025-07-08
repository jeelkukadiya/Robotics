import matplotlib.pyplot as plt
import numpy as np

# epilson decay graph
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 2000

steps_done = np.arange(20000)
eps = EPS_END + (EPS_START - EPS_END) * np.exp(-1 * steps_done / EPS_DECAY)
plt.plot(steps_done, eps)
plt.title('Epsilon decay graph')
plt.xlabel('Episode no.')
plt.ylabel('Epsilon')
plt.show()