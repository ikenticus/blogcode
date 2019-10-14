# Makefile for instagram-token-scraper. Do you want to...
#
# Install the python module dependencies::
#
#   make install
#
# Deploy the lamba and crontab::
#
#   make deploy
#
# Clean the package of compiled files and deployed archives::
#
#   make clean

bucket = canvas-warehouse
s3path = private/lambda

install:
	pip install -r requirements.txt

deploy:
	# retrieve app information
	$(eval arn := $(shell cat .chalice/deployed/dev.json | jq -r .resources[0].lambda_arn))
	$(eval name = $(word 7,$(subst :, ,$(arn))))

	# clean up before deploying
	rm -f .chalice/deployments/*zip
	chalice deploy --no-autogen-policy

	# add drivers to archive
	$(eval archive := $(shell ls -1 .chalice/deployments/*zip))
	mv -f $(archive) $(name).zip
	zip -rp $(name).zip drivers/

	# push archive to S3
	aws s3 cp $(name).zip s3://$(bucket)/$(s3path)/$(name).zip

	# update Lambda to use archive
	aws lambda update-function-code --function-name $(name) --region us-east-1 --s3-bucket $(bucket) --s3-key $(s3path)/$(name).zip

clean:
	find . -iname *__pycache__* -exec rm \-rf {} \;
	find . -iname *pyc -exec rm {} \;
	rm -rf .chalice/deployment*
