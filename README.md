# derekenos.com-generator
A custom static website generator for https://derekenos.com.

## Features
- ~Not too many features~ Seriously, it's gone off the rails with the Microdata and responsive images stuff.
- No third-party libraries
- Aspires to accessibility and SEO best practices 
- Search engines don't hate it
- Optionally redirect large static files to a cloud object store
- Implements [responsive images](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images)
- Intergrates [Microdata](https://schema.org/docs/gs.html) markup to provide structured data for search engines ([example](https://search.google.com/structured-data/testing-tool/u/0/#url=https%3A%2F%2Fderekenos.com%2Fproject-weather-station))
- Intergrates [OpenGraph](https://ogp.me/) tags for rich embeds, e.g.:

  ![Screenshot from 2021-01-17 16-16-28](https://user-images.githubusercontent.com/585182/104856230-6c213900-58df-11eb-8476-927c2f9d9ad3.png)

## Dependencies
- `Python 3.9`

### Additional `dev.sh` Dependencies
- `bash`
- `inotifywait`

### Additional `process-assets.py` Dependencies
| Dependency | Tested Version | Needed For |
| --- | --- | --- |
| [Gimp](https://www.gimp.org/) | 2.10.22 | image width detection and derivative generation |
| [VLC](https://www.videolan.org/vlc/) | 3.0.8 | video poster image generation |

### Additional Large Static Store Dependencies
| LSS Type | Dependencies |
| --- | --- |
| [S3](https://github.com/derekenos/derekenos.com-generator/blob/c5229b224bb1cbfd53439ae5ec5fd7923cef91f5/lib/large_static_store.py#L53) | [aws-cli](https://aws.amazon.com/cli/) |

## Included Dependencies

This project includes a couple of my other repos as submodules:
- [htmlephant](https://github.com/derekenos/htmlephant) - Lazy HTML Generator
- [femtoweb](https://github.com/derekenos/femtoweb) - Async HTTP & Web Application Server

## To build your own, personalized derekenos.com clone

### 1. Clone the repo
Clone the [generic](https://github.com/derekenos/derekenos.com-generator/tree/generic) branch:
```
git clone --recurse-submodules -b generic https://github.com/derekenos/derekenos.com-generator
```

### 2. Configure
Edit [context.json](https://github.com/derekenos/derekenos.com-generator/blob/generic/context.json) and [static/shared.css](https://github.com/derekenos/derekenos.com-generator/blob/generic/static/shared.css) to your liking.

#### Configure Images
Define an array of project images in the context file as follows:
```
<project>: {
  ...
  "images": [
    {
      "filename": "<original-image-normalized-filename>",
      "name": "<image-name>",
      "description": "<image-description>"
    }
  ]
}
```

Where `<original-image-normalized-filename>` names the original, full-size image file in `static/` (or custom static dir) and conforms to the `normalized_image_filename_template` [defined in `context.json`](https://github.com/derekenos/derekenos.com-generator/blob/dc888fb0eee1d02860b87d82dc3cec48eb3f6dd9/context.json#L82).

For example, given the template:
```
"{item_name}-{asset_id}-{width}px-original{extension}"`
```

A valid filename is:
```
project-static-site-generator-4cb061e3-1146px-original.webp
```

##### Derivatives

The current code does not present original image files, which are assumed to be large and/or not well supported by web browsers, directly. Instead, derivatives of the original, in web-friendly formats (as defined by [prioritized_derivative_image_mimetypes](https://github.com/derekenos/derekenos.com-generator/blob/dc888fb0eee1d02860b87d82dc3cec48eb3f6dd9/context.json#L87-L90)) and a variety of sizes (as defined by [derivative_image_widths](https://github.com/derekenos/derekenos.com-generator/blob/dc888fb0eee1d02860b87d82dc3cec48eb3f6dd9/context.json#L91-L99)), are assumed to have been generated, and will be included as options from which the browser will select at will.

Derivative filenames must have the same `item_name` and `asset_id` as the original file and, as defined by [derivative_image_filename_template](https://github.com/derekenos/derekenos.com-generator/blob/generate-derivatives-integration/context.json#L85), have the format:
```
{item_name}-{asset_id}-{width}px{extension}
```

Given the previous original filename example, a valid derivative filename is:
```
project-static-site-generator-4cb061e3-750px.webp
```

Here's an example of how all derivatives are presented in the source for the first image on [this page](https://derekenos.com/project-derekenos-com-generator):
```
<picture>
  <source
    srcset="https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-1146px.webp 1146w,           
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-1000px.webp 1000w,           
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-750px.webp 750w,             
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-500px.webp 500w,             
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-300px.webp 300w,             
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-100px.webp 100w"
    sizes="90vw"
    type="image/webp">
  <source
    srcset="https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-1146px.jpg 1146w,            
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-1000px.jpg 1000w,            
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-750px.jpg 750w,              
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-500px.jpg 500w,              
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-300px.jpg 300w,              
            https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-100px.jpg 100w"
    sizes="90vw"
    type="image/jpeg">
  <img
    src="https://derekenos-com.nyc3.cdn.digitaloceanspaces.com/project-static-site-generator-4cb061e3-750px.jpg"
    loading="lazy"
    alt="A picture of the Static Site Generator">
</picture>
```
You can see that the first `<source>` offers a bunch of next-gen `webp`s because they're rad. The second `<source>` offers `jpg`s which are not as awesome but are well-supported. The `<img>` at the end serves as a fallback for browsers that don't support the `<picture>` tag.

The `process-assets.py` script can take care of all this nightmare filename normalization and derivative generation for you, and has this sweet `auto` action that accepts:
- the path to a directory of misfitly-named, project-specific images and videos
- the name of a project already defined in `context.json`
- the path to the website generator static asset directory

and automatically does all of:
- copy files to a mysterious temporary location with normalized names
- generate all required derivatives
- update the project's `images` and `videos` fields in `context.json`
- move all the normalized original and derivative files into the static dir

I'm sure I've documented that somewhere in here. :eyes:

#### Configure Videos
Define an array of project videos in the context file as follows:
```
<project>: {
  ...
  videos": [
    {
      "filename": "<original-video-normalized-filename>",
      "name": "<video-name>",
      "description": "<video-description>"
    }
  ]
}
```

Like images, videos are expected to have a name that conforms to a template, as defined by [normalized_video_filename_template](https://github.com/derekenos/derekenos.com-generator/blob/dc888fb0eee1d02860b87d82dc3cec48eb3f6dd9/context.json#L83), like:
```
{item_name}-{asset_id}-original{extension}
```

A valid filename is:
```
project-weather-station-82fc52a8-original.mp4
```

The only required derivative for a video is the poster image, which also has a template, as defined by [derivative_video_poster_filename_template](https://github.com/derekenos/derekenos.com-generator/blob/dc888fb0eee1d02860b87d82dc3cec48eb3f6dd9/context.json#L86), like:
```
{base_filename}-poster.jpg
```
_Why did I not make that `{item_name}-{asset_id}-poster.jpg`? I'll [endeavor to fix](https://github.com/derekenos/derekenos.com-generator/issues/18) this._

A valid poster image filename is:
```
project-weather-station-82fc52a8-original-poster.jpg
```

### 3. Add static assets
Add your images, videos, etc. to `static/`.

### 4. Build
Execute [run.py](https://github.com/derekenos/derekenos.com-generator/blob/generic/run.py) to build the site.

#### Usage
```
$ python3.9 run.py --help
usage: run.py [-h] [--development] [--context-file CONTEXT_FILE] [--serve]
              [--host HOST] [--port PORT] [--sync-large-static]

optional arguments:
  -h, --help            show this help message and exit
  --development
  --context-file CONTEXT_FILE
  --serve
  --host HOST
  --port PORT
  --sync-large-static
```

The generated output files will be written to the `site/` directory.

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


## Large Static Store

To avoid making your static site host angry by jamming up its platters with your gratuitous media, the Large Static Store feature allows you to sync static files that exceed some size threshold to a cloud object store of your choosing.

### Configure the Large Static Store

#### 1. Set the Threshold

The value of [Context.STATIC_LARGE_FILE_THRESHOLD_MB](https://github.com/derekenos/derekenos.com-generator/blob/c5229b224bb1cbfd53439ae5ec5fd7923cef91f5/lib/context.py#L17) determines the size threshold (in MBs) over which static files will be redirected to the remote store.

#### 2. Configure the Store

Define a `large_object_store` property in your context file.

Here's an example of my S3 store config:

```
"large_static_store": {
  "type": "S3",
  "aws_profile": "digitalocean",
  "aws_endpoint": "https://nyc3.digitaloceanspaces.com",
  "s3_url": "s3://derekenos-com/",
  "endpoint": "https://derekenos-com.nyc3.cdn.digitaloceanspaces.com"
},
```

Currently, only the [S3](https://github.com/derekenos/derekenos.com-generator/blob/c5229b224bb1cbfd53439ae5ec5fd7923cef91f5/lib/large_static_store.py#L53) storage class is defined, but it should be fairly straight-forward to define others, making sure that your config specifies `type` + whatever properties the class requires.

### Sync Local Files to the Store

Specifying the `--sync-large-static` CLI option to `run.py` will sync your local, large static files to the remote store.

Example:

```
python3.9 run.py --sync-large-static
```

### Developing Against the Store

Once you've synced your large files to the remote, you can delete the local copy and development builds will continue to work as expected (providing you have network access) by automatically resolving missing local files to their URLs in the remote store. In fact, when you execute a development build (i.e. `run.py --development` or `dev.sh`), if any large files exist both locally and in the remote store, you'll see a warning like the following:

```
$ python3.9 run.py --development
Large, local file "weather_station.mp4" exists in the LSS.
Wrote new files to: site/
```

### The Manifest

During a build, [large_static_store.Store.exists()](https://github.com/derekenos/derekenos.com-generator/blob/c5229b224bb1cbfd53439ae5ec5fd7923cef91f5/lib/large_static_store.py#L50) is invoked to check whether a local, large static file exists in the remote store. For more efficient lookups, the class creates and updates a local manifest file named ([by default](https://github.com/derekenos/derekenos.com-generator/blob/c5229b224bb1cbfd53439ae5ec5fd7923cef91f5/lib/large_static_store.py#L15)) `.lss_manifest.json`.

Calling `Store.exists()` makes a `HEAD` request to the remote store endpoint for a specified path to check whether the object exists.
Response headers for found objects are saved in the manifest to serve as proof of existence and to provide metadata required at build time.

This file has the format:

```
{
  "<store-endpoint>": {
    "<object-key>": {
      <HEAD-response-header>,
      <HEAD-response-header>,
      ...      
  },
  ...
}
```

Example:

```
{
  "https://derekenos-com.nyc3.cdn.digitaloceanspaces.com": {
    "weather_station.mp4": {
      "Date": "Thu, 21 Jan 2021 15:17:59 GMT",      
      "Content-Length": "80709540",
      "Content-Type": "video/mp4",
      "Last-Modified": "Thu, 21 Jan 2021 03:15:50 GMT"
      ...
    }
  }
}
```

If your local manifest is out-of-sync with the remote, simple delete the file and the it will be created anew, dispatching fresh queries to the remote, on the next build.


