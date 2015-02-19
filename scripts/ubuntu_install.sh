# System-wide Dependecies and tools
sudo apt-get install git ipython3 ipython3-notebook gettext python3-pip

# Get the Poireau source
git clone https://github.com/ewjoachim/poireau.git

# Using pip, get virtualenv and virtualenvwrapper
sudo -H pip install virtualenv virtualenvwrapper

# Install virtualenv
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo "export PROJECT_HOME=$HOME/Devel" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

# Create a virtualenv with python3
mkvirtualenv poireau --python=`which python3`

# Install the python requirements
cd poireau/
pip install -r requirements.txt
