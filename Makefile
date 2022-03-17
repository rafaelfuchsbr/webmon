start:
	docker-compose up

test:
	pip list --disable-pip-version-check | grep -E 'pytest' >> /dev/null

	if [ $? -ne 0 ]
	then
		pip3 install pytest
	fi

	PYTHONPATH=./app pytest
	if [ $? -ne 0 ]
	then
		echo "Error while running tests. Will not proceed with next steps."
	fi