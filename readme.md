# Quick-and-dirty artstation sync
This is a personal and untested tool to keep (and update) local copies of artstation profiles via cli.
Project id's are saved in order to not re-download everything. This ensures that only new media will be downloaded in each cronjob instance.
No fancy bs going on. Just a simple script bodged together within 10 minutes at 3 AM.

Currently only working for images. Feel free to issue a pull request if you want more.

## Setup
Install required pip modules.
```bash
pip3 install requests pyyaml
```
All scripts require Python3. Tested using 3.9.9.

## Running it
Here we have two scripts:
```bash
grab.py $artist-name
```
This will grab one individual profile, if it is not already downloaded.

---

```bash
grab-all.py
```
This will call `grab.py` on all artists listed in `artists.yaml`.

Files will be saved to `./downloads/{artist_name}/*.{ext}`.
Logs will be saved to `./logs/{artist_name}.txt`.
Download indices (to skip already downloaded projects) are kept in `./already_saved/{artist_name}.txt`.


# LICENSE
```
BSD 2-Clause License

Copyright (c) 2021, Leon Etienne
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
