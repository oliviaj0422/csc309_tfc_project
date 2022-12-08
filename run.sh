#! /bin/bash
cd tfc_project
python3 manage.py runserver &
cd ..
cd frontend
npm start 
