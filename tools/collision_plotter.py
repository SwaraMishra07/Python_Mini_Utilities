import numpy as np
import matplotlib.pyplot as plt

def simulate_collision( m1 , v1i , m2 , v2i , e):
    # m1 , m2 : masses of the objects
    # v1i , v2i : initial velocities of the objects
    # e : coefficient of restitution (0 to 1)
    # Using the restitution formula and conservations of momentum

    v1f = ((m1 - e *m2)* v1i + (1 + e) * m2 * v2i) / (m1+m2)
    v2f = ((m2 - e *m1)* v2i + (1 + e) * m1 * v1i) / (m1+m2)

    return v1f , v2f

def plot_collision( m1, v1i , m2 , v2i , e, x1_initial, x2_initial):

    v1f , v2f = simulate_collision(m1 , v1i , m2 , v2i , e)

    time = np.linspace(0,10,100) # Time range

    x1_before = x1_initial + v1i * time
    x2_before = x2_initial + v2i * time
    x1_after = x1_initial + v1f * time
    x2_after = x2_initial + v2f * time

    plt.figure(figsize=(10,5))

    # Position Plot
    plt.plot(time , x1_before , 'r--', label = 'Mass 1 (Before Collision)')
    plt.plot(time , x2_before , 'b--', label = 'Mass 2 (Before Collision)')
    plt.plot(time , x1_after , 'r' ,label = "Mass 1 (After Collision)")
    plt.plot(time , x2_after , 'b' ,label = "Mass 2 (After Collision)")
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Position before and after collision")
    plt.legend()
    plt.grid()
    print(f"Final velocities after collision : v1f = {v1f:.2f} m/s , v2f = {v2f:.2f} m/s")
    plt.show()
# Taking user input

m1= float(input("Enter mass of object 1 (kg):"))
v1i = float(input("Enter initial velocity of object 1(m/s) :"))
m2= float(input("Enter mass of object 2 (kg):"))
v2i = float(input("Enter initial velocity of object 2(m/s) :"))
e = float(input("Enter coefficient of restitution ( 0 to 1):"))
x1_initial = float(input("Enter initial position of object 1 (m):"))
x2_initial = float(input("Enter initial position of object 2 (m):"))
plot_collision(m1, v1i , m2 , v2i, e , x1_initial, x2_initial)