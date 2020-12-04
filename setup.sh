mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"pratapvcbz@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = 80\n\
" > ~/.streamlit/config.toml
