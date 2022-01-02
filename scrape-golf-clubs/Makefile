MKDIR = mkdir
PIPENV = pipenv
RM = rm
RSYNC = rsync

BUILD_DIR = target
TEST_DIR = tests
MODULES = src/
BUILD_REQS = $(BUILD_DIR)/requirements.txt


install:
	$(PIPENV) install --dev --ignore-pipfile

clean:
	$(PIPENV) --rm
	$(RM) -rf $(BUILD_DIR)

$(BUILD_DIR):
	$(MKDIR) -p $@

$(BUILD_REQS): $(BUILD_DIR)
	$(PIPENV) install --deploy --ignore-pipfile
	$(PIPENV) lock --requirements > $@

copy: $(BUILD_DIR)
	for mod in $(MODULES); do \
		$(RSYNC) -a $$mod/ $(BUILD_DIR)/ ; \
	done

replace-lxml:
	$(RM) -rf $(BUILD_DIR)/lxml
	$(RSYNC) -a static/ $(BUILD_DIR)/

build: $(BUILD_REQS) copy
	$(PIPENV) run pip install \
	--isolated --disable-pip-version-check \
	--target $(BUILD_DIR)/ --requirement $(BUILD_REQS)
	make replace-lxml

lint:
	$(PIPENV) run black src/

lint-check:
	$(PIPENV) run black --check src/

test:
	PYTHONPATH=../../ $(PIPENV) run python -m pytest $(TEST_DIR) -v
