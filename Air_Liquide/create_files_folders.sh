#!/bin/bash

# Create directories
mkdir -p works/air_liquid/data works/air_liquid/deployment works/air_liquid/models works/air_liquid/notebooks works/air_liquid/preprocessing works/air_liquid/utils

# Create files
touch works/air_liquid/data/download_data.py
touch works/air_liquid/deployment/app.py
touch works/air_liquid/deployment/requirements.txt
touch works/air_liquid/models/model.py
touch works/air_liquid/notebooks/exploration_de_donnees.ipynb
touch works/air_liquid/notebooks/validation_et_evaluation.ipynb
touch works/air_liquid/preprocessing/preprocessing.py
touch works/air_liquid/utils/data_loading.py
touch works/air_liquid/utils/model_evaluation.py
touch works/main.py
touch works/README.md
touch works/requirements.txt

# Print success message
echo "All directories and files have been created successfully!"

