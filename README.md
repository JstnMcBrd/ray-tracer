# ray-tracer

A simple [ray tracer](https://en.wikipedia.org/wiki/Ray_tracing_(graphics)) written in [Python](https://www.python.org/).

![program-6-scene-3](https://user-images.githubusercontent.com/28303477/224002637-4f6d5e4d-c5f9-428f-9237-80e46799bcb7.png)

## Licensing

Without a custom license, this code is the direct intellectual property of the original developer. It may not be used, modified, or shared without explicit permission. Please see [GitHub's guide on licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

## Scenes

Scenes are defined in `JSON` files. See a few examples in the [scenes](/scenes/) folder.

Any deviation from the following type definitions will result in assertion errors.

```ts
/** Represents an RGB color. All elements must be between 0 and 1. */
type Color = Array<number>[3];

/** Represents a direction vector. Will throw warnings if not normalized. */
type Direction = Array<number>[3];

/** Represents a location in the scene. */
type Position = Array<number>[3]; 

/** Defines the entire scene. This is the schema you should use for your scene JSON files. */
class Scene {
	/** The position the camera is looking towards. */
	camera_look_at?: Position = [0, 0, 0];

	/** The position the camera is looking from (the camera's position). */
	camera_look_from?: Position = [0, 0, 1];

	/** The "up" direction for the camera. */
	camera_look_up?: Direction = [0, 1, 0];

	/** The angle width of the camera's view. Must be between 0 and 359. */
	field_of_view?: float = 90;

	/** The direction to the directional light source. */
	light_direction?: Direction = [0, 1, 0];

	/** The color of the directional light. */
	light_color?: Color = [1, 1, 1];

	/** The color of the global ambient light. */
	ambient_light_color?: Color = [1, 1, 1];

	/** The color of the scene background. */
	background_color?: Color = [0, 0, 0];

	/** A list of all objects in the scene. */
	objects?: Array<Object>;
};

/** The universal values shared by all objects. */
class Object {
	/** The name of the object. Has no affect on the behavior of the object. */
	name?: string;

	/** The type of the object. Used to differentiate between different classes of objects.
	 * Must be one of the accepted values. See other object classes below. */
	type: string;

	/** The coefficient for ambient lighting. Must be between 0 and 1. */
	ambient_coefficient?: number = 0;

	/** The coefficient for diffuse lighting. Must be between 0 and 1. */
	diffuse_coefficient?: number = 1;

	/** The coefficient for specular lighting. Must be between 0 and 1. */
	specular_coefficient?: number = 0;

	/** The color for diffuse lighting. */
	diffuse_color?: Color = [1, 1, 1];

	/** The color for specular lighting. */
	specular_color?: Color = [1, 1, 1];

	/** The coefficient for specular glossiness. */
	gloss_coefficient?: number = 4;

	/** How reflective the object surface should be. Must be between 0 and 1. */
	reflectivity?: number = 0;
};

/** The specific values necessary for Planes. */
class Plane extends Object {
	/** Defines this object as a Plane. */
	type: string = "plane";

	/** The direction the plane faces. */
	normal: Direction;

	/** Any position on the plane. */
	point: Position = [0, 0, 0];
};

/** The specific values necessary for Polygons. */
class Polygon extends Object {
	/** Defines this object as a Polygon. */
	type: string = "polygon";

	/** A list of vertices in counterclockwise order. Must have at least 3. */
	vertices: Array<Position>;
};

/** The specific values necessary for Spheres. */
class Sphere extends Object {
	/** Defines this object as a Sphere. */
	type: string = "sphere";

	/** The central location of the Sphere. */
	center: Position;

	/** The radius of the Sphere. Must be greater than 0. */
	radius: number;
};

// More types of objects can be added later.
// In the meantime, most kinds of objects can be modeled with Polygons.
```

## Running

You can run the ray tracer with the following command:

```bash
python ./src/main.py
```

The script has many required arguments. Use the `--help` command to see a full list. 

Passing all the arguments through the console every time can quickly get annoying, so this project has support for `dotenv`.

Create a new file called `.env` in the root folder and place any arguments you reuse often. These will act as "default" values.

You may still pass the arguments through the command prompt, and your `.env` values will be ignored.

## Output

For now, this raytracer only formats output as `.ppm` files. [PPM](https://en.wikipedia.org/wiki/Netpbm) images can be difficult to open and view. Support for more commonly-used image encodings is a future goal.
