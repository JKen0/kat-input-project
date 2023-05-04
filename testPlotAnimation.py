import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import RotationMaps.RotationToPosition13 as rtp13
import KATData.FetchKATData as FetchKAT

# TO-DO: CHANGE PARAMETERS SINNCE THEY WILL CHANGE
KATGATE_REFERENCE_POS = np.array([-1, -1])
LF_ROTATION_INITIAL = np.array([2, 12])
RF_ROTATION_INITIAL = np.array([2, 12])
UPDATE_TIME = 60/20

# STATIC INITIAL VALUES
kat_walk_radius = 18.25
left_foot_position = np.array([-3, 0])
right_foot_position = np.array([3, 0])

an = np.linspace(0, 2 * np.pi, 200)

# Create figure for plotting
fig, ax = plt.subplots()

# IMPORT FETCH KAT DATA CLASS
kat_config = FetchKAT.FetchKATData(KATGATE_REFERENCE_POS[0], KATGATE_REFERENCE_POS[1])

# IMPORT CONVERT ROTATION TO POSITION ALGORITHM CLASS
left_foot_rot = rtp13.RotationToPosition13(LF_ROTATION_INITIAL[0], LF_ROTATION_INITIAL[1])
right_foot_rot = rtp13.RotationToPosition13(RF_ROTATION_INITIAL[0], RF_ROTATION_INITIAL[1])

# This function is called periodically from FuncAnimation
def animate(i):
    # FETCH KAT DATA
    LF_roll , LF_pitch, RF_roll, RF_pitch = kat_config.getData()

    # ESTIMATE FOOT POSITION BASED ON ROTATIONS
    LF_position = left_foot_rot.calcPredictedPosition(LF_roll, LF_pitch)
    RF_position = right_foot_rot.calcPredictedPosition(RF_roll, RF_pitch)

    # FORMAT DATA
    left_foot_position = np.array([round(LF_position[0], 2), round(LF_position[1], 2)])
    right_foot_position = np.array([round(RF_position[0], 2), round(RF_position[1], 2)])

    # HARDCODE POSITION IF OUT OF BOUNDS
    if(np.isnan(left_foot_position[0])):
        left_foot_position = np.array([20, 20])

    if(np.isnan(right_foot_position[0])):
        right_foot_position = np.array([20, 20])

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
ani = animation.FuncAnimation(fig, animate, interval=UPDATE_TIME, cache_frame_data=False, save_count=100)
plt.show()
