# ray-tracer

A simple [ray tracer](https://en.wikipedia.org/wiki/Ray_tracing_(graphics)) written in [Python](https://www.python.org/).

![program-6-scene-3](https://user-images.githubusercontent.com/28303477/224002637-4f6d5e4d-c5f9-428f-9237-80e46799bcb7.png)

## Licensing

Without a custom license, this code is the direct intellectual property of the original developer. It may not be used, modified, or shared without explicit permission. Please see [GitHub's guide on licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

## Scenes

Scenes are defined in `JSON` files. See a few examples in the [scenes](/scenes/) folder.

Any deviation from the following type definitions will result in assertion errors.

```ts
type Color = Array<number>[3];					// all elements must be between 0 and 1
type Direction = Array<number>[3];				// will throw warnings if not normalized
type Position = Array<number>[3]; 

class Scene {
	camera_look_at?: Position = [0, 0, 0];
	camera_look_from?: Position = [0, 0, 1];
	camera_look_up?: Position = [0, 1, 0];
	field_of_view?: float = 90;					// must be between 0 and 359
	light_direction?: Direction = [0, 1, 0];
	light_color?: Color = [1, 1, 1];
	ambient_light_color?: Color = [1, 1, 1];
	background_color?: Color = [0, 0, 0];
	objects?: Array<Object>;
};

class Object {
	name?: string;
	type: string;								// must be one of the accepted values, see below
	ambient_coefficient?: number = 0;			// must be between 0 and 1
	diffuse_coefficient?: number = 1;			// must be between 0 and 1
	specular_coefficient?: number = 0;			// must be between 0 and 1
	diffuse_color?: Color = [1, 1, 1];
	specular_color?: Color = [1, 1, 1];
	gloss_coefficient?: number = 4;
	reflectivity?: number = 0;					// must be between 0 and 1
};

class Plane extends Object {
	type: string = "plane";
	normal: Direction;
	point: Position = [0, 0, 0];
};

class Polygon extends Object {
	type: string = "polygon";
	vertices: Array<Position>;					// must have at least 3
};

class Sphere extends Object {
	type: string = "sphere";
	center: Position;
	radius: number;								// must be greater than 0
};

// More types of objects can be added later
// In the meantime, most kinds of objects can be modeled with polygons
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
