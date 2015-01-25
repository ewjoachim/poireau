
# This is the Poireau configuration file. It may contain several parameters
# you will want to keep secret, so keep it somewhere safe on you disk.

# To have the parameters loaded by poireau, call a copy of this script
# with your modifications in the shell that will launch Poireau

# Poireau has sensible (develepment) replacements for each of these settings
# if not present.

export POIREAU_DEBUG=0  # or 1
export POIREAU_SECRET_KEY="<Replace this with a long random generated string !>"
export POIREAU_CHOIR_NAME="Name of your choir"
export POIREAU_SONGS_FOLDER="/path/to/your/song/files/"
export POIREAU_ALLOWED_HOSTS="comma,separated,list,of,hostnames,and,ips"
export POIREAU_ADMINS="John:john@doe.com,Jane:jane@doe.com"

# Json string. All parameters are optionnal (remove the keys you don't use)
export POIREAU_MAIL_SETTINGS='{
	"host": "localhost",
	"user": "",
	"password": "",
	"tls": false,
	"port": 25
}'


export PYTHONHASHSEED="random"
