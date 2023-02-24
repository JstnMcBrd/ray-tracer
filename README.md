# CS-455-Ray-Tracer

A simple ray tracer written in [Python](https://www.python.org/).

![output](https://user-images.githubusercontent.com/28303477/221062912-4e55338d-c347-46fc-9588-7e2aef5c7d73.png)

## Licensing

Without a custom license, this code is the direct intellectual property of the original developer. It may not be used, modified, or shared without explicit permission. Please see [GitHub's guide on licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

## Scenes

Scenes are defined in `JSON` files. See a few examples in the [scenes](/scenes/) folder.

Any deviation from the schema will result in assertion errors.

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
