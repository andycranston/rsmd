# Really Simple Mark Down (rsmd) to HTML converter

Converts the simple and very basic elements of Mark Down
to HTML.

## What is it for?

In a few words:

> To preview README.md files in a browser before uploading to github

## What elements are currently supported?

* Headings (#, ##, ###, etc.)
* Paragraphs
* Lists (* item)
* Quotes (> text)
* Horizontal rule (---, *** and ___)
* Code segments between ```

## Code

The converter is a small single Python 3 program contained in a file called:

```
rsmd.py
```

## Example usage (Windows)

Assume the `rsmd.py` file has been copied to:

```
C:\pythoncode\rsmd.py
```

Also assume the directory:

```
C:\andyc\projects\rsmd
```

contains a file called:

```
README.md
```

which has mark down to be converted.

Open a Windows command prompt and type:

```
c:
cd \andyc\projects\rsmd
python \pythoncode\rsmd.py
```

The `rsmd.py` program should have created a file called:

```
README.htm
```

in the current directory.

Open a web browser and enter the following URL:

```
file://c:/andyc/projects/rsmd/README.htm
```

## Example usage (UNIX/Linux)

Copy the rsmd.py to a directory in your PATH, remove the ".py" extension and make
the file executable.  For example something similar to:

```
cp rsmd.py /home/andyc/bin
cd /home/andyc/bin
mv rsmd.py rsmd
chmod a+x rsmd
```

Now running:

```
rsmd
```

in a directory will look for a file called:

```
README.md
```

and create the file:

```
README.htm
```

See the note below on command line arguments.

## Command line arguments

The default input file name is `README.md` and the default output file
name is `README.htm`.  Either or both of these can be changed with the command line
options --infile and --outfile respectively.  For example on Windows:

```
python \pythoncode\rsmd.py --infile=moduledoc.md --outfile=moduledoc.html
```

and on UNIX/Linux:

```
rsmd --infile=moduledoc.md --outfile=moduledoc.html
```

## Limitations

It only converts the very basic mark down elements.  Anything else
is just passed through as plain text.

My inline CSS styling is awful :-]

## Warnings

The output file is overwritten without asking for confirmation.

----------------------------
End of README