.DEFAULT_GOAL := test
PIP="pip"
SRC_CORE="src"
SRC_TESTS="tests"

define INLINE_AWK
BEGIN {
  FS = ":.*##"
  cyan = "\033[36m"
  white = "\033[0m"
  printf "\nUsage:\n  make %s<target>%s\n\nTargets:\n", cyan, white
}
/^[a-zA-Z_-]+:.*?##/ {
  printf "  %s%-10s%s %s\n", cyan, $$1, white, $$2
}
endef

export INLINE_AWK

.PHONY: help
help:  ## Display this help
	@awk "$$INLINE_AWK" $(MAKEFILE_LIST)

.PHONY: test
test: ## Run automated tests
	@pytest -vv -s $(SRC_TESTS)

.PHONY: auto-style
auto-style:  ## Autopep8 to fix style issues
	@type autopep8 >/dev/null 2>&1 || (echo "Run '$(PIP) install autopep8' first." >&2 ; exit 1)
	@autopep8 -i -r $(SRC_CORE) $(SRC_TESTS)

# If E252 is not disabled in flake8 and pycodestyle, a spurious failure is seen:
# src/lib/policy.py:26:24: E252 missing whitespace around parameter equals

.PHONY: code-style
code-style:  ## Pycodestyle tests
	@type pycodestyle >/dev/null 2>&1 || (echo "Run '$(PIP) install pycodestyle' first." >&2 ; exit 1)
	@pycodestyle --ignore=E252 $(SRC_CORE) $(SRC_TESTS)

.PHONY: code-lint
code-lint:  ## Pylint and Flake8 tests
	@type pylint >/dev/null 2>&1 || (echo "Run '$(PIP) install pylint' first." >&2 ; exit 1)
	@type flake8 >/dev/null 2>&1 || (echo "Run '$(PIP) install flake8' first." >&2 ; exit 1)
	@flake8 --ignore=E252 $(SRC_CORE) $(SRC_TESTS)

.PHONY: type-check
type-check:  ## Mypy tests
	@type mypy >/dev/null 2>&1 || (echo "Run '$(PIP) install mypy' first." >&2 ; exit 1)
	@mypy $(SRC_CORE) $(SRC_TESTS)

.PHONY: lint
lint: code-style code-lint type-check  ## code-style, code-lint and type-check

.PHONY: lint-fix
lint-fix:
	@autopep8 --in-place --aggressive --aggressive -r $(SRC_CORE) $(SRC_TESTS)

.PHONY: build
build:	## Run sam build
	sam build

.PHONY: clean
clean:  ## Delete pycache files
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete

.PHONY: invoke
invoke: build
	sam local invoke -n events/env.json -e $(EVENT)
