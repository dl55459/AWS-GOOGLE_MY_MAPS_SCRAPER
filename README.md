Make EC2 instance on AWS:
1) Ubuntu server
2) architecture 64-bit (x86)
3) Create key-pair
4) allow ssh trafic from anywhere

Install all necesary dependencies:
1) sudo apt update
   sudo apt upgrade -y
2) sudo apt install python3 python3-pip -y
3) sudo apt install git -y
4) wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
   echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
   sudo apt update
   sudo apt install google-chrome-stable -y
5) sudo apt install unzip
6) wget https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/linux64/chromedriver-linux64.zip
7) unzip chromedriver-linux64.zip
8) sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
9) sudo apt install python3-venv -y
10) sudo apt install python3-selenium
11) sudo apt install tmux -y

Running session:
to start new session: tmux new -s session_name
to detatch from session: CTRL+B, D
to attach to session: tmux attach -t session_name
to terminate a session: CTRL+C, and input text: exit
