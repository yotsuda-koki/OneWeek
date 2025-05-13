import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

G = 6.67430e-11

sun_mass = 1.989e30
sun_pos = np.array([0.0, 0.0])

earth_mass = 5.972e24
earth_pos = np.array([1.496e11, 0.0])
earth_vel = np.array([0.0, 29780.0])

dt = 60 * 60
steps = 24 * 365

positions = []

for _ in range(steps):
    r = earth_pos - sun_pos
    distance = np.linalg.norm(r)
    direction = r / distance

    force = - G * sun_mass * earth_mass / distance**2
    acc = force * direction / earth_mass

    earth_vel += acc * dt
    earth_pos += earth_vel * dt

    positions.append(earth_pos.copy())

postions = np.array(positions)

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlim(-2e11, 2e11)
ax.set_ylim(-2e11, 2e11)
earth_dot, = ax.plot([], [], 'bo', label='Earth')
path_line, = ax.plot([], [], 'b-', label='Path')
sun_dot, = ax.plot([], [], 'ro', label='Sun')

xdata, ydata = [], []

def init():
    sun_dot.set_data([sun_pos[0]], [sun_pos[1]])
    earth_dot.set_data([],[])
    path_line.set_data([],[])
    return sun_dot, earth_dot, path_line

def update(frame):
    x, y = positions[frame]
    xdata.append(x)
    ydata.append(y)
    earth_dot.set_data([x], [y])
    path_line.set_data(xdata, ydata)
    return sun_dot, earth_dot, path_line

ani = animation.FuncAnimation(
    fig, update, frames=len(positions), init_func=init, blit=True, interval=1, repeat=True
)

plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.legend()
plt.title('Eartch Orbiting the Sun')
plt.show()