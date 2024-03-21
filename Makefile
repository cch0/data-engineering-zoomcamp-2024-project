
# Variables
TERRAFORM_DIR := terraform
CURRENT_DIR := $(shell pwd)

.PHONY: list
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'


tf_init:
	 cd $(TERRAFORM_DIR) && terraform init ; cd $(CURRENT_DIR)


tf_plan:
	cd $(TERRAFORM_DIR) && terraform plan ; cd $(CURRENT_DIR)

tf_apply:
	cd $(TERRAFORM_DIR) && terraform apply ; cd $(CURRENT_DIR)


