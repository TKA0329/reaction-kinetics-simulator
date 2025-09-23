import matplotlib.pyplot as plt
import numpy as np
import mplcursors

data = np.outer(range(10), range(1, 5))

fig, ax = plt.subplots()
lines = ax.plot(data)
ax.set_title("Click somewhere on a line.\nRight-click to deselect.\n"
             "Annotations can be dragged.")

mplcursors.cursor(lines)  # or just mplcursors.cursor()

plt.show()