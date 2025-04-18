#!/bin/bash
mkdir -p ~/.streamlit/

echo "\
[general]
email = \"yeadhukrishna.p@gmail.com\"
" > ~/.streamlit/credentials.toml

echo "\
[server]
headless = true
enableCORS = true
enableXsrfProtection = false
port = \$PORT
" > ~/.streamlit/config.toml

streamlit run ozilly.py
