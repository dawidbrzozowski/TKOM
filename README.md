# Project for TKOM - Own programming language implementation


## Run project demo from file:
python -m interpreting.interpreter --file_path <PATH_TO_FILE>
## or run using default file:
python -m interpreting.interpreter
## You can also run demo from stdin using:
python -m interpreting.interpreter --source_type stdin

## Running demo lexer from file:
python -m lexer.lexer --file_path <PATH_TO_FILE>
## Running demo lexer from stdin:
python -m lexer.lexer --lexer_type stdin

Input your code, when 'stdin code >' prompt shows up.
When you're finished with writing your code - type 'DONE'.

## Project was split into 3 parts: Lexer, Parser, Interpreter. Instructions how to check previous stages below.

## Running demo parser from file:
python -m parsing.parser --file_path <PATH_TO_FILE>
You can also run for default text file using simply python -m parsing.parser

## Running demo parser from stdin:
python -m parsing.parser --source_type stdin

Input your code, when 'stdin code >' prompt shows up.
When you're finished with writing your code - type 'DONE'.