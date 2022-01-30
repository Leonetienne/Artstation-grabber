# Quick-and-dirty artstation sync
This is a personal and untested tool to keep (and update) local copies of artstation profiles via cli.
Project id's are saved in order to not re-download everything. This ensures that only new media will be downloaded in each cronjob instance.
No fancy bs going on. Just a simple script bodged together within 10 minutes at 3 AM.

Also supports to download search results.


Currently only working for images. Feel free to issue a pull request if you want more.

## Setup
Install required pip modules.
```bash
pip3 install requests pyyaml
```
All scripts require Python3. Tested using 3.9.9.

## Running it
Here we have three scripts:

### Grab an artists profile
```bash
grab-artist.py 'mixppl'
```
This will grab one individual profile, in this case the user 'mixppl'. You must use the username in the profiles url! Not the full name!

### Grab search results
```bash
grab-search.py 'Game of Thrones' 100
```
This will grab the first 100 results of the search term 'Game of Thrones'.
If you omit the result limit, **ALL** results will be downloaded! That could be useful, if your search query is very niche. But if you omit it for a popular search term, like 'Game of Thrones', you're in for a ride,
as all approx 12000 projects will be queued for download.

### Automate it
### Invoke downloads / a scan
```bash
grab-all.py
```
This will call `grab-artists.py` and `grab-search.py` on all artists and search terms listed in `to-grab.yaml`.

Files will be saved to `./downloads/{artist_name}/*.{ext}` and `/downloads/search_{search_terms}/*{artist_id}_*.{ext}`.
Logs will be saved to `./logs/{artist_name/search_terms}.txt`.
Download indices (to skip already downloaded projects) are kept in `./already_saved/{artist_name/search_terms}.txt`.

> :warning: Projects already downloaded from an artists-page will be downloaded **again** if they appear in a search term, and vica versa. Artist- and search queries do NOT share download indices!

### Configure what to download
Simply adjust [`to-grab.yaml`](https://github.com/Leonetienne/Artstation-grabber/blob/master/to-grab.yaml) to your needs. Here is an example:
```
--- 
artists: 
  - mixppl
  - shumolly

searches:
 -
  terms: Game of Thrones
  max: 3

 -
  terms: Pirates
  max: 3

 -
  terms: robby rotton
```
The last search term, 'robby rotton' is to show that you can also omit `max`. If you do not want to fetch artists, or searches, at all, just delete that yaml-array entirely.


## A word on power usage
Do not overuse this or you might piss of artstations maintainers. Just because you CAN download 400 gigabytes of images per day doesn't mean that you should!
If you plan on downloading LOADS of stuff, you should add some sleep statements to cut the servers some slack.

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
