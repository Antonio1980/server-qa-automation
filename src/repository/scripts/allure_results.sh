#!/bin/bash

if [[ ! -d ~/Allure/bin/ ]]; then
  # shellcheck disable=SC2242
  exit "You should install Allure locally first."
fi

~/Allure/bin/allure generate src/repository/allure_results/ -o src/repository/allure_reports/ --clean
cp -r src/repository/allure_reports/history src/repository/allure_results/history
~/Allure/bin/allure generate src/repository/allure_results/ -o src/repository/allure_reports/ --clean
