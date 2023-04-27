import matplotlib.pyplot as plt
import numpy as np

# initial values
kat_walk_radius = 18.25
left_foot_position = np.array([-3, 0])
right_foot_position = np.array([3, 0])

# CREATE THE CIRCLE WHICH IS EDGE OF THE SURFACE
an = np.linspace(0, 2 * np.pi, 200)
fig, axs = plt.subplots()
axs.plot(kat_walk_radius * np.cos(an), kat_walk_radius * np.sin(an), color="red")
axs.set(xlim=(-21, 21), ylim=(-21, 21))
axs.set_title('Position of Feet on the Kat Walk C', fontsize=10)
axs.set_xlabel('X-Axis')
axs.set_ylabel('Z-Axis')

# CRETE MARKERS OF THE LEFT AND RIGHT FOOT
right_foot_marker = axs.plot(right_foot_position[0], right_foot_position[1], marker="^", markersize="20", color="blue", label="Right Foot")
left_foot_marker = axs.plot(left_foot_position[0], left_foot_position[1], marker="^", markersize="20", color="green", label="Left Foot")

# ADD LABELS AND GRID LINES
plt.legend(loc="upper left", fontsize="9")
plt.grid(axis = 'y')
plt.grid(axis = 'x')

# ADD REAL TIME TEXT (though i dont think this is possible dynamically)
plt.text(right_foot_position[0], right_foot_position[1]+1.5, '({}, {})'.format(right_foot_position[0], right_foot_position[1]))
plt.text(left_foot_position[0], left_foot_position[1]+1.5, '({}, {})'.format(left_foot_position[0], left_foot_position[1]))

plt.show()
