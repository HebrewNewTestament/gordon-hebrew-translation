#!/bin/sh

daniel_url='https://he.wikisource.org/w/index.php?title=%D7%93%D7%A0%D7%99%D7%90%D7%9C_%D7%91%D7%AA%D7%A8%D7%92%D7%95%D7%9D_%D7%A2%D7%91%D7%A8%D7%99_(%D7%92%D7%95%D7%A8%D7%93%D7%95%D7%9F)&action=raw'
ezra_url='https://he.wikisource.org/w/index.php?title=%D7%A2%D7%96%D7%A8%D7%90_%D7%91%D7%AA%D7%A8%D7%92%D7%95%D7%9D_%D7%A2%D7%91%D7%A8%D7%99_(%D7%92%D7%95%D7%A8%D7%93%D7%95%D7%9F)&action=raw'

wget -O daniel.mw "${daniel_url}"
wget -O ezra.mw "${ezra_url}"

[ -d "${HOME}/venv/bin" ] && . "${HOME}/venv/bin/activate"
python3 mw-to-osis.py
