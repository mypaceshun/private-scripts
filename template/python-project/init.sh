#!/usr/bin/env bash
PYTHON3=${PYTHON3:-python3}
POETRY=${POETRY:-${PYTHON3} -m poetry}

BASE_DOWNLOAD_URL="https://raw.githubusercontent.com/mypaceshun/private-scripts/master/template/python-project/"

function usage() {
  echo "$0 [TARGET]"
  echo ""
  echo "Init Python project directory for mypaceshun"
  echo ""
  echo "  TARGET      init directory (default: current directory)"
  echo ""
  echo "Environment variables"
  echo "  PYTHON3      your python3 command path (default: python3)"
  echo "  POETRY       your poetry command path (default: PYTHON3 -m poetry)"
  exit 0
}

TARGET="."
if [ 0 -lt $# ]; then
  if [ $1 == "-h" -o $1 == "--help" ]; then
    usage
  fi
  TARGET=$1
fi

echo "PYTHON3 is [${PYTHON3}]"
echo "POETRY is [${POETRY}]"
echo "TARGET is [${TARGET}]"

if [ ! -e ${TARGET} ]; then
  mkdir -vp ${TARGET}
elif [ ! -d ${TARGET} ]; then
  echo "${TARGET} is not Directory!!"
  exit 1
fi

function download_template() {
  template_path=$1
  dest=${2:-.}
  template_url="${BASE_DOWNLOAD_URL}${template_path}"
  (cd ${dest} && curl -OL ${template_url})
}

function init_directory() {
  ${POETRY} init
  ${POETRY} add click rich
  ${POETRY} add -D flake8 pyproject-flake8 isort autoflake black mypy pytest pytest-cov poethepoet pre-commit
  download_template "template/.pre-commit-config.yaml"
  mkdir -vp src/ tests/
  ${POETRY} run pre-commit install
  add_file="pyproject_additional_config.toml"
  tmp_dir=`mktemp -d`
  download_template "template/${add_file}" ${tmp_dir}/
  cat ${tmp_dir}/${add_file} >> pyproject.toml
  mkdir -vp .github/workflows/
  download_template "template/main.yml" .github/workflows/
  ${POETRY} add -D sphinx
  mkdir -vp pre-docs
  ${POETRY} run sphinx-quickstart pre-docs --sep -l ja --ext-autodoc --ext-doctest --ext-githubpages --no-makefile --no-batchfile
}

(cd ${TARGET} && init_directory)
