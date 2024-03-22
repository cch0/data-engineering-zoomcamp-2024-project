
# Variables
TERRAFORM_DIR := terraform
CURRENT_DIR := $(shell pwd)
MAGE_DIR := mage


.PHONY: list
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'


# execute "terraform init"
tf_init:
	 cd $(TERRAFORM_DIR) && terraform init ; cd $(CURRENT_DIR)


# execute "terraform plan"
tf_plan:
	cd $(TERRAFORM_DIR) && terraform plan ; cd $(CURRENT_DIR)


# execute "terraform apply"
tf_apply:
	cd $(TERRAFORM_DIR) && terraform apply ; cd $(CURRENT_DIR)


# execute python script to fetch weather data
fetch:
	python src/weather_data_loader.py


# transform data
transform_raw:
	python src/transform.py


# build mage image
mage_build:
	cd $(MAGE_DIR) && docker compose build ; cd $(CURRENT_DIR)

# spin up mage and postgres containers
mage_up:
	cd $(MAGE_DIR) && docker compose up -d ; cd $(CURRENT_DIR)

# spin down mage and postgres containers
mage_down:
	cd $(MAGE_DIR) && docker compose down; cd $(CURRENT_DIR)



