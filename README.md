# PNBoia API

The PNBoia API serves as a platform for accessing buoy data collected by the National Buoy Program (PNBoia) of the Brazilian Navy Hydrographic Center. This API allows users to retrieve and integrate real-time and historical information from the PNBoia buoys. 

Please refer to the [PNBoia API Documentation (EN)](https://drive.google.com/file/d/1tQPuF1UfDH-IQ-ip1qLdtEwVeK1Tp5G2/view?usp=drive_link) or [PNBoia API Documentation (PT)](https://drive.google.com/file/d/1jtUmtkCTs_HtUcJLE4faqZs4VYlqSQYu/view?usp=drive_link).

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for pnboia_api in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/pnboia_api`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "pnboia_api"
git remote add origin git@github.com:{group}/pnboia_api.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
pnboia_api-run
```

# Install

Go to `https://github.com/{group}/pnboia_api` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/pnboia_api.git
cd pnboia_api
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
pnboia_api-run
```
