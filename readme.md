# create virtual env
python -m venv .venv

# activate the virtual env
source .venv/Scripts/activate

# install fastapi and packages
pip install -r requirements.txt

# run
fastapi dev 
`uvicorn app.main:app --reload`

# set up database
installed postgres
with 
pass ->   
port -> 5432
