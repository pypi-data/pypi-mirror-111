# history-view
A little tool to visually browse your console history.

What it looks like to scan through your history now:
    
![first_bugfixes](https://user-images.githubusercontent.com/479566/124069729-82383700-d9f1-11eb-9ff4-1fffccd0e7b6.gif)

### Arguments

| Argument       | Description                                               |
|----------------|-----------------------------------------------------------|
| `-s, --search` | Filter history by regex.                                  |
| `--c`          | Don't invoke selected command, instead copy to clipboard. |

## Known Issues

- Still uses `subprocess` to invoke. It should be _mostly_ the same given that environment variables are passed in, but a straightforward return of the command is something that would be better.
- Only supports Windows and Powershell.
- Only adds to the long-term history. Not the history of the current shell (available via up/down)

### Addendum

Yes, I am entirely aware that I could get the same affect in powershell with `Get-History`. Not the point!
