import sys

print("Hello World on Stdout")
print('spam on stderr', file=sys.stderr)

with open('myfile.out', 'w') as out:
    out.write("Hello myfile.out")

