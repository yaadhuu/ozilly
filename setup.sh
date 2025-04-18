#!/bin/bash
mkdir -p ~/.streamlit/

echo "\
[general]
email = \"yeadhukrishna.p@gmail.com\"\n
" > ~/.streamlit/credentials.toml

echo "\
[server]
headless = true
enableCORS=false
port = $PORT
" > ~/.streamlit/config.toml

streamlit run ozilly.py
