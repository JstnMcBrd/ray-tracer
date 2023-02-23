from math import tan
import numpy as np

class Sphere:
	def __init__(self, center, color, radius, kd, ks, kt, kl, ir):
		self.center = center
		self.color = color
		self.radius = radius
		self.kd = kd
		self.ks = ks
		self.kt = kt
		self.kl = kl
		self.ir = ir

spheres = [
	Sphere(np.array([0.0,  6.0,  00.5]), np.array([1.0, 1.0, 1.0]), 0.9, 0.05, 0.2, 0.85, 0.00, 1.7),
	Sphere(np.array([-1.0,  8.0,  00.5]), np.array([1.0, 0.5, 0.2]), 1.0, 0.70, 0.3, 0.00, 0.05, 1.2),
	Sphere(np.array([1.0,  8.0, -00.5]), np.array([0.1, 0.8, 0.8]), 1.0, 0.30, 0.7, 0.00, 0.00, 1.2),
	Sphere(np.array([3.0, -6.0,  15.0]), np.array([1.0, 0.8, 1.0]), 7.0, 0.00, 0.0, 0.00, 0.60, 1.5),
	Sphere(np.array([-3.0, -3.0,  12.0]), np.array([0.8, 1.0, 1.0]), 5.0, 0.00, 0.0, 0.00, 0.50, 1.5)
]

ambient = np.array([0.02, 0.02, 0.02])
black = np.array([0.0, 0.0, 0.0])

def magnitude(A: np.ndarray) -> float:
	return np.sqrt(np.dot(A,A))

def normalized(A: np.ndarray) -> np.ndarray:
	return A / magnitude(A)

def intersect(P: np.ndarray, D: np.ndarray) -> Sphere:
	best = None
	tmin = 1e30
	u = 0.0
	b = 0.0

	for s in spheres:
		positionDifference = s.center - P
		b = np.dot(D, positionDifference)
		u = b**2 - np.dot(positionDifference, positionDifference) + s.radius**2
		u = u**0.5 if u > 0 else 1e31
		u = b - u if b - u > 1e-7 else b + u
		if u >= 1e-7 and u < tmin:
			best = s
			tmin = u
		else:
			tmin = tmin
	
	return best, tmin

def trace(level, P: np.ndarray, D: np.ndarray) -> list:
	d = 0.0
	eta = 0.0
	e = 0.0
	N = np.array([0,0,0])
	color = np.array([0,0,0])
	s = None # sphere
	l = None # sphere
	U = np.array([0.0, 0.0, 0.0])

	level -= 1
	if level == 0:
		return black
	
	s, tmin = intersect(P, D)
	if s == None:
		return ambient
	
	color = ambient

	eta = s.ir

	P = P + tmin*D
	N = normalized(s.center - P)
	d = -1*np.dot(D, N)

	if d < 0:
		N = black - N
		eta = 1 / eta
		d *= -1

	for l in spheres:
		U = normalized(l.center - P)
		e = l.kl * np.dot(N, U)
		if e > 0 and intersect(P, U)[0] == l:
			color = color + e*l.color

	U = s.color
	color[0] *= U[0]
	color[1] *= U[1]
	color[2] *= U[2]
	e = 1 - eta**2 * (1 - d**2)

	return black + s.kl*U + s.kd*color + s.ks*trace(level, P, D + 2*d*N) + s.kt*(trace(level, P, (eta*d - e**0.5)*N + eta*D) if e > 0 else black)

def raytracer(output_file):
	yx = 0
	U = np.array([0.0, 0.0, 0.0])

	output_file.write("P3\n32 32\n255")
	while yx < 32**2:
		U[0] = yx % 32 - 32 / 2
		yx += 1
		U[2] = 32 / 2 - yx / 32
		U[1] = 32 / 2 / tan(25 / 114.5915590261)

		U = black + 255.0*trace(3, black, normalized(U))
		output_file.write(f"{int(U[0])} {int(U[1])} {int(U[2])}\n")

if __name__ == "__main__":
	with open("output.ppm", "w") as output_file:
		raytracer(output_file)
