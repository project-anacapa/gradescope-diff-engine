# gradescope-diff-engine

An approach to diff-based autograding using Gradescope.

# What these tools provide

The tools in this repo allow you to set up an autograded assignment, or any portion of an autograded assignment, where points are
assigned based on comparing (`diff`'ing) any of the following against known reference output.

* `stdout` (standard output)
* `stderr` (standard error)
* the contents of a specified output file

The author of the assignment provides a github repo containing:
* One or more shell scripts with commands from which stdout,stderr,or output files are captured.
* A reference implementation that is used to create the reference output against which student submissions are compared.

Points are assigned only on the basis of those lines in the script that are immediately preceeded by a comment with a test annotation that specifies what is to be compared.

Here are a few examples (full documentation follows later in this README.md file)

This example runs the program `./lab01` twice.  The first time, the
filename `testdata01.txt` is passed as a command line parameter.
Presumably, the program does some computation over this data, and puts
some output on `stdout`.  The autograding tools will compare the
`stdout` to known reference output, and if it matches, assign 30/30
points to the student's grade.  Otherwise, it will assign 0/30 points
to the student's grade report on Gradescope.  The second time, the
program `./lab01` is run with no command line parameter.  Presumably,
this should produce an error message on `stderr`.  If the correct
error message is produced, 20/20 points are assigned for this test case,
otherwise 0/20 points are assigned.

```
#!/usr/bin/env bash

# @test{"stdout":30, name:"check output of lab01 on testdata01.txt"}
./lab01 testdata01.txt

# @test{"stderr":20, name:"check for error message when ./lab01 is run without an argument"}
./lab01 

```

Here is another example that shows how output to a particular named
file can be captured and tested, and how visibility of tests can be controlled.
It shows running `./lab02 infile1.txt outfile1.txt` and then testing the
contents of `outfile1.txt` against the reference output for that file.   It also shows how the `visibility`
parameter can be specified.  The four options for `visibility`,
namely `hidden`, `after_due_date`, `after_published`, and `visible` (the default)
are documented on [Gradescope's own autograder documentation](https://gradescope-autograders.readthedocs.io/en/latest/specs/#controlling-test-case-visibility).


```
#!/usr/bin/env bash

# @test{"filename":"outfile1.txt", points:25, name:"run ./lab02 infile1.txt outfile1.txt and check output"}
./lab02 infile1.txt outfile1.txt

# @test{"filename":"secretOut1.txt", points:25, name:"run ./lab02 secret test 1","visibility":"after_due_date"}
./lab02 secretIn1.txt secretOut1.txt


```


# Restrictions

In order to keep the tools simple, there are a few restrictions.   These may be relaxed in future versions as time permits.

1.  Line continuations are not supported&mdash;neither for test annotations, nor for the shell commands that immediately follow them.

    That is, both test annotations and the shell command that immediately follows a test annotation must appear on a single line.

2.  Currently, the shell command must be something that is legal to pass to Python 3's `subprocess.Popen` method, using:

   ```python
   subprocess.Popen(shell_command.strip().split(" "))
   ```

   This may restrict the use of certain shell commands, redirection options, and so forth.   Future versions might relax
   this restriction by porting some of the code from Python3 to directly interacting with the bash shell.

# How to use these tools

TBD


