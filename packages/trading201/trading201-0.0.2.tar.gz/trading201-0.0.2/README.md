````
envsubst < setup_.cfg > setup.cfg
python38 -m build --wheel
python38 -m twine upload dist/*
python38 -m pip install --upgrade trading201
````