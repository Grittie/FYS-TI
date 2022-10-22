## Install:

### Setup een python venv (Optioneel)

```sh
python3 -m venv .env
source ./.env/bin/activate
```
Als een een venv gaat gebruiken moet je niet vergeten om het altijd te activeren.
Hiervoor is het handig om `alias va='source ./.env/bin/activate'` in jouw `bashrc` te zetten, 
dan kan je gewoon `va` typen het is klaar.
Je kan ook `alias vc='python3 -m venv .env'` er onder zetten om makkelijk een venv te maken.

### Installer de dependencies

```sh
pip3 install -r requirements.txt
```