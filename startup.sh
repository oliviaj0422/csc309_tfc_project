cd tfc_project/
python3 -m pip install virtualenv
virtualenv -p `which python3.10` venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
cd ..
cd frontend/
npm install
cd ..


