# derekenos.com-generator
This is a custom static website generator that I built specifically for https://derekenos.com

## Dependencies
- `Python 3.9`

## Additional `dev.sh` Dependencies
- `bash`
- `inotifywait` 

## To build your own, personalized derekenos.com clone

### Get ready

1. Clone the [generic](https://github.com/derekenos/derekenos.com-generator/tree/generic) branch

```
    git clone --recurse-submodules -b generic https://github.com/derekenos/derekenos.com-generator
```

2. Edit [context.json](https://github.com/derekenos/derekenos.com-generator/blob/generic/context.json) and [static/shared.css](https://github.com/derekenos/derekenos.com-generator/blob/generic/static/shared.css) to your liking

3. Add project (or whatever) thumbnail images to `static/`

    For each `context.projects` item, the following corresponding files must exist in `static/`:
      - `{project.thumb_base_filename}.webp`
      - `{project.thumb_base_filename}.png`

### Build the site

Execute [run.py](https://github.com/derekenos/derekenos.com-generator/blob/generic/run.py) to build the site.

#### Usage
```
$ python3.9 run.py --help
usage: run.py [-h] [--development] [--context-file CONTEXT_FILE] [--serve] [--host HOST] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --development
  --context-file CONTEXT_FILE
  --serve
  --host HOST
  --port PORT

```

The generated output files are written to the `site/` directory.

#### Execute a development build and launch the server

```
python3.9 run.py --context-file=context.json --development --serve 
```

#### Use `dev.sh` for live development
This script executes a development build, starts the server, and watches for local filesystem changes - when a change is detected, it rebuilds the site and triggers a refresh in the browser, allowing you to see changes in real time without having to manually refresh.
```
./dev.sh 
```

#### Execute a production build 
```
python3.9 run.py --context-file=context.json
```

#### What's included in development vs. production

| mode | [Live Dev](https://github.com/derekenos/derekenos.com-generator/blob/generic/includes/live_dev.py) | [Google Analytics](https://github.com/derekenos/derekenos.com-generator/blob/generic/includes/google_analytics.py) |
| --- | --- | --- |
| development | yes | no |
| production | no | yes |
