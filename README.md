# derekenos.com-generator
This is a custom static website generator that I built specifically for https://derekenos.com

## Features
- Not a lot of features
- No third-party libraries
- Reasonable accessibility
- Search engines don't hate it
- [OpenGraph](https://ogp.me/) tags are included in [project pages](https://github.com/derekenos/derekenos.com-generator/blob/generic/pages/project-generator.py#L19-L52) to enable rich embeds, e.g.:
![Screenshot from 2021-01-17 16-16-28](https://user-images.githubusercontent.com/585182/104856230-6c213900-58df-11eb-8476-927c2f9d9ad3.png)


## Dependencies
- `Python 3.9`

## Additional `dev.sh` Dependencies
- `bash`
- `inotifywait`

## Included Dependencies

This project includes a couple of my other repos as submodules:
- [htmlephant](https://github.com/derekenos/htmlephant) - Lazy HTML Generator
- [femtoweb](https://github.com/derekenos/femtoweb) - Async HTTP & Web Application Server

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
