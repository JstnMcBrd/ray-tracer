# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Type-check code with mypy ([#14](https://github.com/JstnMcBrd/ray-tracer/pull/14))
- Support exporting every image type that Pillow supports ([#15](https://github.com/JstnMcBrd/ray-tracer/pull/15))
- Export images all-at-once instead of one pixel at a time ([#15](https://github.com/JstnMcBrd/ray-tracer/pull/15))
- Use native `imap` instead of patched `istarmap` for multiprocessing ([#17](https://github.com/JstnMcBrd/ray-tracer/pull/17))
- Simplify raycasting ([#17](https://github.com/JstnMcBrd/ray-tracer/pull/17))
- Vectorize some calculations with numpy ([#19](https://github.com/JstnMcBrd/ray-tracer/pull/19))
- Use standardized `__main__.py` entrypoint ([#20](https://github.com/JstnMcBrd/ray-tracer/pull/20))
- Clip color in-place to save memory ([#20](https://github.com/JstnMcBrd/ray-tracer/pull/20))
- Lint code with ruff instead of PyLint ([#22](https://github.com/JstnMcBrd/ray-tracer/pull/22))
- Type-check code with ty instead of mypy ([#84](https://github.com/JstnMcBrd/ray-tracer/pull/84))
- Use `time.perf_counter` instead of `datetime.now` ([#85](https://github.com/JstnMcBrd/ray-tracer/pull/85))
- Upgrade to Python 3.14 ([#86](https://github.com/JstnMcBrd/ray-tracer/pull/86))
- Format code with ruff ([#87](https://github.com/JstnMcBrd/ray-tracer/pull/87))
- **Breaking:** manage project with uv ([#88](https://github.com/JstnMcBrd/ray-tracer/pull/88))

### Added

- Add section on Development to README ([#12](https://github.com/JstnMcBrd/ray-tracer/pull/12), [#14](https://github.com/JstnMcBrd/ray-tracer/pull/14))
- Add badges to README ([#21](https://github.com/JstnMcBrd/ray-tracer/pull/21), [#88](https://github.com/JstnMcBrd/ray-tracer/pull/88))
- Add a `.python-version` file ([#22](https://github.com/JstnMcBrd/ray-tracer/pull/22))
- Add contributing agreement to README ([#23](https://github.com/JstnMcBrd/ray-tracer/pull/23))
- Add a `CHANGELOG.md` file ([#73](https://github.com/JstnMcBrd/ray-tracer/pull/73))

### Removed

- **Breaking:** remove `max-color` argument ([#11](https://github.com/JstnMcBrd/ray-tracer/pull/11))
- **Breaking:** remove `output-format` argument ([#15](https://github.com/JstnMcBrd/ray-tracer/pull/15))
- Remove multiprocessing library patch ([#17](https://github.com/JstnMcBrd/ray-tracer/pull/17))
- Remove position offsets when checking shadows/reflections ([#19](https://github.com/JstnMcBrd/ray-tracer/pull/19))
- Remove Docker configuration ([#88](https://github.com/JstnMcBrd/ray-tracer/pull/88))

### Fixed

- Index screen by row,col instead of col,row ([#17](https://github.com/JstnMcBrd/ray-tracer/pull/17))

## [4.0.0] - 2023-06-26

### Changed

- **Breaking:** use `.png` as default output format ([#8](https://github.com/JstnMcBrd/ray-tracer/pull/8))
- **Breaking:** rename `"center"` and `"point"` object attributes to `"position"` ([#8](https://github.com/JstnMcBrd/ray-tracer/pull/8))
- Automatically convert 3-sided polygons to triangles ([#6](https://github.com/JstnMcBrd/ray-tracer/pull/6))
- Reformat code using PyLint ([#7](https://github.com/JstnMcBrd/ray-tracer/pull/7))
- Add default values for `output`, `width`, and `height` ([#7](https://github.com/JstnMcBrd/ray-tracer/pull/7))
- Improve argument parsing ([#7](https://github.com/JstnMcBrd/ray-tracer/pull/7))
- Reorganize README ([#7](https://github.com/JstnMcBrd/ray-tracer/pull/7))
- Improve command line output ([#7](https://github.com/JstnMcBrd/ray-tracer/pull/7))

### Added

- Support circle object type ([#5](https://github.com/JstnMcBrd/ray-tracer/pull/5))
- Support triangle object type ([#6](https://github.com/JstnMcBrd/ray-tracer/pull/6))
- Add progress bar for writing output to file ([#7](https://github.com/JstnMcBrd/ray-tracer/pull/7))
- Add section on versioning to README ([#8](https://github.com/JstnMcBrd/ray-tracer/pull/8))
- Support `.png` output ([#8](https://github.com/JstnMcBrd/ray-tracer/pull/8))

## [3.0.0] - 2023-03-09

### Changed

- **Breaking:** replace `direction_to_light` with `light_direction` for scene definitions ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- **Breaking:** rename all env arguments to match console arguments ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Use multiprocessing for faster rendering ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Apply default values when importing scenes ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Add new example image to README ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Simplify sphere normal calculation ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Use safer `None` comparisons ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))

### Added

- Support polygon object type ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Support plane object type ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Add shadows ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Add reflectivity and recursive raycasting ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Add `progress-bar` argument to disable progress bar for faster rendering ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Add warning message when auto-normalizing scene input vectors ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Add indicator when writing output to file ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Add scene file type definitions to README ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))

### Fixed

- Clamp color values ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Fix inaccurate `camera_look_at` importing ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))
- Fix bug where `field_of_view` could be 360 instead of 0 ([#4](https://github.com/JstnMcBrd/ray-tracer/pull/4))

## [2.0.0] - 2023-02-25

### Changed

- **Breaking:** refactor to use `snack_case` instead of `camelCase` ([#2](https://github.com/JstnMcBrd/ray-tracer/pull/2))
- Reorganize code ([#2](https://github.com/JstnMcBrd/ray-tracer/pull/2))
- Rename project from `CS-455-Ray-Tracer` to `ray-tracer` ([#3](https://github.com/JstnMcBrd/ray-tracer/pull/3))
- Improve example image in README ([#3](https://github.com/JstnMcBrd/ray-tracer/pull/3))

### Added

- Add progress bar to track job progress ([#2](https://github.com/JstnMcBrd/ray-tracer/pull/2))
- Add timer to track efficiency ([#2](https://github.com/JstnMcBrd/ray-tracer/pull/2))

### Fixed

- Fix bug where window was half the size ([#2](https://github.com/JstnMcBrd/ray-tracer/pull/2))

## [1.0.0] - 2023-02-23

### Added

- Add README with licensing and usage ([#1](https://github.com/JstnMcBrd/ray-tracer/pull/1))
- Add argparsing with environment variable alternatives ([#1](https://github.com/JstnMcBrd/ray-tracer/pull/1))
- Implement scene importing system ([#1](https://github.com/JstnMcBrd/ray-tracer/pull/1))
- Implement basic raytracing ([#1](https://github.com/JstnMcBrd/ray-tracer/pull/1))
- Implement basic Phong shading model ([#1](https://github.com/JstnMcBrd/ray-tracer/pull/1))
- Support `.ppm` output ([#1](https://github.com/JstnMcBrd/ray-tracer/pull/1))

[Unreleased]: https://github.com/JstnMcBrd/ray-tracer/compare/v4.0.0...HEAD
[4.0.0]: https://github.com/JstnMcBrd/ray-tracer/compare/v3.0.0...v4.0.0
[3.0.0]: https://github.com/JstnMcBrd/ray-tracer/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/JstnMcBrd/ray-tracer/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/JstnMcBrd/ray-tracer/releases/tag/v1.0.0
