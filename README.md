### Context
This project was set as part of my final year module, 'Special Core in Software Engineering and High Performance Computing'.

The aim of this project is to create a package to process data from the ATLAS experiment (https://cds.cern.ch/record/2707171) using cloud technology. 

This work is based on an existing notebook that walks the user through the steps to rediscover the Higgs boson. This is shown in this repository ([HZZAnalysis_Initial.ipynb](https://github.com/kgerrand/CloudComputing_MiniProject/blob/main/HZZAnalysis_initial.ipynb)), but can also be found at https://github.com/atlas-outreach-data-tools/notebooks-collection-opendata/blob/master/13-TeV-examples/uproot_python/HZZAnalysis.ipynb.

### Running the Service
The service can be run by using [docker-compose.yml](https://github.com/kgerrand/CloudComputing_MiniProject/blob/main/docker-compose.yml), which is activated by writing `docker compose up`. This will automatically build all required images and create the associated containers; the number of workers is set to 3 but this can be easily changed within [docker-compose.yml](https://github.com/kgerrand/CloudComputing_MiniProject/blob/main/docker-compose.yml) depending on the user's requirements.