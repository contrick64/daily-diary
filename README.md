# Daily Journal

`daily.py` is a command-line utility for managing a daily journal. It provides several functionalities such as creating a new entry, adding to an existing entry, wrapping text, and opening the journal in an editor.

## Usage

You can use the `daily.py` script from the command line as follows:

```bash
python daily.py [command] [options]
```
The available commands are:

- `write`: Write an entry to today's file, create it if not exists.
- `add`: Add an entry inline. Requires the -m/--mood and -e/--entry options.
- `edit`: Edit today's entry without adding any headers.

The available options are:

- `-w/--wrap-file`: Wrap the entire contents of today's file.

For the add command, these are required:

- `-m/--mood`: The mood character and word(s) to be included, like `+ motivated joyous`
- `-e/--entry`: The text to be entered into your diary.

## Contributing
This is the first repository I am creating with the intent of inviting contributions and turning into a proper package. Please feel free to suggest features, make PRs, or report bugs as you see fit.

I will also accept suggestions on how best to accept suggestions...

## License
This project is licensed under the GPLv3 License.