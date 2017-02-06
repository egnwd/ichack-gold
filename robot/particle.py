import robot 
import random
import math
import time
import numpy as np
from motor_setup import setup
import particleDataStructures as pds


def main():		
	global interface

	interface.terminate()


def run_waypoint(waypoints):
	global r, canvas, mymap
	mymap.draw()

	particles = []
	num_particles = 100
	weight = 1.0 / num_particles
	for i in range(0, num_particles):
		particles.append((waypoints[0][0], waypoints[0][1], 0.0, weight))

	for (wx, wy) in waypoints[1:]:
		while True:
			ex, ey, et = mean_particle(particles)
			a = math.atan2(wy - ey, wx - ex) - et
			a = normalise_angle(a)
			r.rotate(math.degrees(a))
			particles = angle_update(particles, a)
			particles = sonar_update(particles, r.sonar_distance())
			canvas.draw_particles(particles)

			ex, ey, _ = mean_particle(particles)
			d = math.hypot(wx - ex, wy - ey)
			chunk = min(d,20.0)
			ax, ay, _ = mean_particle(particles)
			r.forward(chunk)
			particles = line_update(particles, chunk)
			particles = sonar_update(particles, r.sonar_distance())
			canvas.draw_particles(particles)
			bx, by, _ = mean_particle(particles)
			canvas.draw_line((ax, ay, bx, by))
			if chunk < 20:
				break


def mean_particle(particles):
	x_m, y_m, tx_m, ty_m = 0.0, 0.0, 0.0, 0.0
	for (x, y, t, w) in particles:

		x_m += x * w
		y_m += y * w

		tx_m += math.cos(t) * w
		ty_m += math.sin(t) * w

	return x_m, y_m, math.atan2(ty_m, tx_m)


def calc_likelihood(x, y, t, z):
	sigma = 2.0
	k = 0.02
	a = 5.0
	m, incidence = calc_ground_truth(x, y, t)
	return a * math.exp(-((z - m) ** 2) / (2.0 * (sigma ** 2))) + k, incidence


def calc_ground_truth(x, y, t):
	walls = mymap.get_walls()
	m_cur = float("inf")
	wall_cur = None
	for (ax, ay, bx, by) in walls:
		m = (
					(by - ay) * (ax - x) - (bx - ax) * (ay - y)
				) / (
					(by - ay) * math.cos(t) - (bx - ax) * math.sin(t)
				)
		ix, iy = (x + m * math.cos(t)), (y + m * math.sin(t))
		if m > 0 and m < m_cur and hits_wall((ax, ay, bx, by), (ix, iy)):
			m_cur = m
			wall_cur = (ax, ay, bx, by)
	incidence = math.pi
	if wall_cur != None:
		incidence = calc_incidence(wall_cur, t)
	return m_cur, incidence


def hits_wall(wall, i):
	ax, ay, bx, by = wall
	ix, iy = i
	return min(ax, bx) <= ix <= max(ax, bx) and min(ay, by) <= iy <= max(ay, by)


def calc_incidence(wall, t):
	ax, ay, bx, by = wall
	beta = math.acos((
			math.cos(t) * (ay - by) + math.sin(t) * (bx - ax)
		) / (
			math.sqrt(((ay - by) ** 2) + ((bx - ax) ** 2))
		))
	return beta


def run_robot():
	global r, canvas
	mymap.draw()

	particles = []
	num_particles = 10
	weight = 1.0 / num_particles
	for i in range(0, num_particles):
		particles.append((0.0, 0.0, 0.0, weight))

	d = 10
	steps = 4
	a = math.pi / 2
	sides = 4
	for i in range(0, sides):
		for j in range(0, steps):
			r.forward(d)
			particles = line_update(particles, d)
			canvas.draw_particles(particles)
		r.rotate(math.degrees(a))
		particles = angle_update(particles, a)
		canvas.draw_particles(particles)


def sonar_update(particles, z):
	theta_max = math.radians(43.0)
	skip_threshold = len(particles) / 2
	skip_count = 0
	particles_new = []
	for (x, y, theta, w) in particles:
		likelihood, incidence = calc_likelihood(x, y, theta, z)
		w_new = w * likelihood
		particles_new.append((x, y, theta, w_new))
		if incidence > theta_max:
			skip_count += 1
			if skip_count > skip_threshold:
				return particles
	w_total = sum([particle[3] for particle in particles_new])
	particles_norm = [(x, y, t, w / w_total) for (x, y, t, w) in particles_new]
	w_cum = np.cumsum([particle[3] for particle in particles_norm])
	particles_resamp = []
	for _ in range(len(particles_norm)):
		r = random.random()
		i = cdf_search(w_cum, r)
		x, y, t, _ = particles_norm[i]
		particles_resamp.append((x, y, t, 1.0 / len(particles_norm)))
	return particles_resamp

def cdf_search(w_cum, r):
	l_ptr = 0
	r_ptr = len(w_cum)
	while r_ptr - l_ptr > 1:
		m_ptr = (l_ptr + r_ptr) // 2
		w = w_cum[m_ptr]
		if w < r :
			l_ptr = m_ptr
		else:
			r_ptr = m_ptr
	return l_ptr


def line_update(particles, d):
	particles_new = []
	mu = 0
	sigma_e = 0.1
	sigma_f = 0.01
	for (x, y, theta, w) in particles:
		e = random.gauss(mu, sigma_e)
		f = random.gauss(mu, sigma_f)
		x_new = x + (d + e) * math.cos(theta)
		y_new = y + (d + e) * math.sin(theta)
		theta_new = normalise_angle(theta + f)
		particles_new.append((x_new, y_new, theta_new, w))
	return particles_new


def angle_update(particles, a):
	particles_new = []
	mu = 0
	sigma_g = 0.02
	for (x, y, theta, w) in particles:
		g = random.gauss(mu, sigma_g)
		theta_new = normalise_angle(theta + a + g)
		particles_new.append((x, y, theta_new, w))
	return particles_new


def normalise_angle(a):
	return math.atan2(math.sin(a), math.cos(a))

def create_map():
	global canvas
	walls = []
	# Definitions of walls
	# a: O to A
	# b: A to B
	# c: C to D
	# d: D to E
	# e: E to F
	# f: F to G
	# g: G to H
	# h: H to O
	walls.append((0,0,0,168));        # a
	walls.append((0,168,84,168));     # b
	walls.append((84,126,84,210));    # c
	walls.append((84,210,168,210));   # d
	walls.append((168,210,168,84));   # e
	walls.append((168,84,210,84));    # f
	walls.append((210,84,210,0));     # g
	walls.append((210,0,0,0));        # h
	return pds.Map(canvas, walls)


interface, motors = setup()
r = robot.Robot(interface, motors)
canvas = pds.Canvas()
mymap = create_map()

if __name__ == "__main__":
	main()

