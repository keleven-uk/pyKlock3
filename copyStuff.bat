@rem  Simple script to copy the required files needed for pyKlock to run.
@rem
@rem   November 2025               <2024> (c) Kevin Scott

@echo OFF

copy LICENSE.txt output\
copy README.md output\
copy docs\history.txt output\

robocopy resources output\resources /s /e


