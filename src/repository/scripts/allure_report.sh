#!/usr/bin/env bash

if [[ ! -d ~/Tools/Allure/bin/ ]]; then
  # shellcheck disable=SC2242
  exit "You should install Allure locally first."
fi

~/Tools/Allure/bin/allure open src/repository/allure_report/
