import math
import particleDataStructures as pds
import robot
import random
import time
from motor_setup import setup

interval = 5
particles = []
interface, motors, head = setup()
r = robot.Robot(interface, motors, head=head)

histograms = [[101, 95, 94, 93, 92, 92, 92, 91, 91, 91, 91, 91, 92, 92, 92, 93,
	95, 96]]

def main():
	global interface, mymap, particles
	waypoints = [(84.0, 30.0), (123.0, 42.0), (84.0, 30.0)]
	generate_particles(waypoints[0])
	i = 0
	pos = (waypoints[0][0], waypoints[0][1], 0.0)
	for wp in waypoints[1:-1]:
		pos = move_to(pos, wp)
		#he = calculate_histogram(mymap, wp)
		he = histograms[i]
		print(len(he), he)
		ha = scan_area()
		print(len(ha), ha)
		delta_t = predict_obstacle(he, ha)
		pos = safe_crash(pos, delta_t)
		i += 1
	# Get to end
	print(pos)
	pos = move_to(pos, waypoints[-1])

def normalise_angle(a):
	return math.atan2(math.sin(a), math.cos(a))

def move_to(pos, wp):
	global r
	ex, ey, et = pos
	wx, wy = wp
	a = math.atan2(wy - ey, wx - ex) - et
	a = normalise_angle(a)
	r.rotate(math.degrees(a))
	d = math.hypot(wx - ex, wy - ey)
	r.forward(d)
	r.rotate(math.degrees(-a))
	return wx, wy, et

def scan_area():
	global r
	r.rotate_head(45)
	histogram = []
	for i in xrange(0, 90, interval):
		histogram.append(r.sonar_distance())
		r.rotate_head(-interval)
	r.rotate_head(45)
	return histogram

def scan_area():
	global r
	r.rotate_head(45)
	histogram = []
	for i in xrange(0, 90, interval):
		histogram.append(r.sonar_distance())
		r.rotate_head(-interval)
	r.rotate_head(45)
	return histogram

def predict_obstacle(he, ha):
	eps = 7
	diffs = [(abs(x-y), y) for (x, y) in zip(he,ha)]
	flags = [x > eps and y != 255 for x, y in diffs]

	print 'DIFFS:\t', diffs
	print 'FLAGS:\t', flags

	start, end = 0, 0
	max_l = (0, 0)
	prev = False
	for i, f in enumerate(flags):
		if not prev and f:
			start = i
		elif prev and not f:
			end = i
			if max_l[1]-max_l[0] < end-start:
				max_l = (start, end)
		prev = f
	if end < start and max_l[1]-max_l[0] < len(flags)-1-start:
		max_l = (start, len(flags)-1)
	median_a = ((max_l[1] - max_l[0]) / 2) + max_l[0]
	median_b = ((max_l[1] - max_l[0] + 1) / 2) + max_l[0]
	# Currently can't see a need for this but it gets a *rough* estimate to the
	# bottle
	#average_diff = (diffs[median_a] + diffs[median_b]) / 2.0
	#e = (he[median_a] + he[median_b]) / 2.0
	#average_d = e - average_diff
	#print(max_l)
	average_a = (((median_a + median_b) / 2.0) * interval) - 45.0
	return average_a
	

def safe_crash(pos, delta_t):
	global r
	print(pos, delta_t)
	r.rotate(delta_t)
	dist = r.drive_until_crash()
	print(dist)
	x, y, t = pos
	t_new = t + math.radians(delta_t)
	x_new = x + math.cos(t_new) * dist
	y_new = y + math.sin(t_new) * dist
	return x_new, y_new, t_new

	
def generate_particles(waypoint):
	global particles
	num_particles = 100
	weight = 1.0 / num_particles
	for i in range(0, num_particles):
		particles.append((waypoint[0], waypoint[1], 0.0, weight))

def calculate_histogram(mymap, pos):
	histogram = []
	x, y = pos
	walls = mymap.get_walls()
	for t in xrange(-45, 45, interval):
		t = math.radians(t)
		for (ax, ay, bx, by) in walls:
			try:
				m = (
							(by - ay) * (ax - x) - (bx - ax) * (ay - y)
						) / (
							(by - ay) * math.cos(t) - (bx - ax) * math.sin(t)
						)
				ix, iy = (x + m * math.cos(t)), (y + m * math.sin(t))
				if m > 0 and hits_wall((ax, ay, bx, by), (ix, iy)):
					histogram.append(int(round(m)))
			except ZeroDivisionError:
				pass
	return histogram

def mean_particle(particles):
	x_m, y_m, tx_m, ty_m = 0.0, 0.0, 0.0, 0.0
	for (x, y, t, w) in particles:

		x_m += x * w
		y_m += y * w

		tx_m += math.cos(t) * w
		ty_m += math.sin(t) * w

def hits_wall(wall, i):
	ax, ay, bx, by = wall
	ix, iy = i
	ix, iy = int(round(ix)), int(round(iy))
	return min(ax, bx) <= ix <= max(ax, bx) and min(ay, by) <= iy <= max(ay, by)

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

canvas = pds.Canvas()
mymap = create_map()

if __name__ == "__main__":
	main()
