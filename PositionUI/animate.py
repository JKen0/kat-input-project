import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# initial values
kat_walk_radius = 18.25
update_time = 1000/60
left_foot_position = np.array([-3, 0])
right_foot_position = np.array([3, 0])

an = np.linspace(0, 2 * np.pi, 200)

# Create figure for plotting
fig, ax = plt.subplots()

# This function is called periodically from FuncAnimation
def animate(i):


    left_foot_x = random.uniform(-kat_walk_radius, kat_walk_radius)
    left_upper_bound = np.linalg.norm(kat_walk_radius - left_foot_x)
    left_foot_z = random.uniform(-left_upper_bound, left_upper_bound)

    right_foot_x = random.uniform(-kat_walk_radius, kat_walk_radius)
    right_upper_bound = np.linalg.norm(kat_walk_radius - right_foot_x)
    right_foot_z = random.uniform(-right_upper_bound, right_upper_bound)

    left_foot_position = np.array([round(left_foot_x, 2), round(left_foot_z, 2)])
    right_foot_position = np.array([round(right_foot_x, 2), round(right_foot_z, 2)])

    # CLEAR PREVIOUS PLOTS
    ax.clear()

    # PLOT CIRCLE AND FOOT MARKERS
    ax.plot(kat_walk_radius * np.cos(an), kat_walk_radius * np.sin(an), color="red")
    ax.plot(right_foot_position[0], right_foot_position[1], marker="^", markersize="20", color="blue", label="Right Foot")
    ax.plot(left_foot_position[0], left_foot_position[1], marker="^", markersize="20", color="green", label="Left Foot")

    # ADD LABELS AND GRID LINES
    ax.set(xlim=(-21, 21), ylim=(-21, 21))
    ax.set_title('Position of Feet on the Kat Walk C', fontsize=10)
    ax.set_xlabel('X-Axis')
    ax.set_ylabel('Z-Axis')
    plt.legend(loc="upper left", fontsize="9")
    plt.grid(axis = 'y')
    plt.grid(axis = 'x')

    # PLOT POSITION OF FOOTS IN TEXT FORM
    plt.text(right_foot_position[0], right_foot_position[1]+1.5, '({}, {})'.format(right_foot_position[0], right_foot_position[1]))
    plt.text(left_foot_position[0], left_foot_position[1]+1.5, '({}, {})'.format(left_foot_position[0], left_foot_position[1]))

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, interval=update_time, cache_frame_data=False, save_count=100)
plt.show()