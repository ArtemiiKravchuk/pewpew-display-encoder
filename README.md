# PewPewLive Display Encoder

![glebi's level preview, screenshot by jf](https://jpcdn.it/img/871568d0f51c32374273aaa9524671ad.png)

Script for encoding images into format, supported by glebi's display level in PewPewLive.

Converts image to black and white and resizes it before encoding, all automatically

### Installation

Create virtual environment, install dependancies:

```bash
py -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage

You can run the script, specifying the image as a command line argument:

```bash
py main.py image.jpg
```

Using config file is optional, but recommended if you want to change some settings. Config file can be created with `config.example.json` as an example.

Here is a description of all the possible settings, you can change in `config.json`:

```json
{
  "logs_path": "/logs",  // where to save the logs, default: null (dont save them)
  "input_path": "image.jpg",  // input image (as of now, overwrite the argument)
  "size_factor": 10,  // screen size will be `(x * 14; 1200 // x)`
  "conversion_settings": {
    "resize": {
      "mode": "resize"  // can be "resize" or "crop"
    }
  }
}
```

### License

Copyright 2024 Artemii Kravchuk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
