# stds

## Motivation

This is a small package that provides 3 high-level APIs to interact elegantly with stdin, stdout and stderr:

    - stdin
    - stderr
    - stdout

## Usage

You can use it as such:

``` 
if __name__ == "__main__":
    stdin | print
    "This prints out stuff on stdout" | stdout
    "This prints out stuff on stderr" | stderr
```
