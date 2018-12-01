# tidyup

Sorts a downloads folder by rules in a YAML file.

## Install

Needs python 3.

    git clone <this repo>
    cd tidyup
    pip3 install --user -e .

## Rules file

Lives at ~/.tidyup.yml unless you pass --config.

    target: ~/Downloads
    rules:
      - name: images
        match: ["*.jpg", "*.jpeg", "*.png", "*.gif"]
        dest: ~/Pictures/unsorted
      - name: pdfs
        match: "*.pdf"
        dest: pdf
      - name: old installers
        match: ["*.exe", "*.msi", "*.deb"]
        older_than: 30
        dest: trash

Each rule is checked seperately, in order. The first one that matches wins.

- match is one glob or a list of globs, case insensitive.
- dest is a folder. Relative paths are relative to target. It gets
  created if it is missing.
- older_than is in days, by modification time.
- dest: trash moves the file to .tidyup-trash inside target. Nothing
  is ever deleted.

Directories and dotfiles are never touched. If a file with the same
name is already in dest the new one becomes "name (1).ext".

## Usage

    tidyup run --dry-run     # show what would move
    tidyup run               # do it
    tidyup run -v            # print every move
    tidyup check             # validate the rules file

## Tests

    pip3 install --user -r requirements-dev.txt
    make test
