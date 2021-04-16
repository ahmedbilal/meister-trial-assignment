## Setup

```bash
virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
./manage.py migrate
sh ./bootstrap.sh
```