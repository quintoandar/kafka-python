import os
import coverage
from behave.__main__ import main as behave_main

dir_path = os.path.dirname(os.path.realpath(__file__))

# change dir to make sure data is loaded and saved to the correct directory
os.chdir(dir_path)

MINIMUM_COVERAGE = 75
START_GREEN = '\x1b[1;36;40m'
START_RED = '\x1b[6;30;41m'
END_COLOR = '\x1b[0m'

cov = coverage.Coverage()
cov.start()

print()
print("-----------------------------------------")
print("------------------ TESTS ----------------")
print("-----------------------------------------")
print()
result = behave_main("idempotence_client/tests")
cov.stop()
print()
print("-----------------------------------------")
print("--------------CODE COVERAGE--------------")
print("-----------------------------------------")
print()
cov.save()
total_cover = cov.report()
print()
if total_cover < MINIMUM_COVERAGE:
    print("-----------------------------------------")
    print('---Code coverage requirements %sNOT%s met!---' % (START_RED,
                                                             END_COLOR))
    print("----------Minimum coverage %s%d%%%s!----------" %
          (START_GREEN, MINIMUM_COVERAGE, END_COLOR))
    print("-----------------------------------------")
    print()
print("-----------------------------------------")
print("See full reports at ./htmlcov/index.html")
print("-----------------------------------------")
cov.html_report()
if result != 0:
    exit(result)
if total_cover < MINIMUM_COVERAGE:
    exit(1)
