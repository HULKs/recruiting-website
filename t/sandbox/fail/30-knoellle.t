use strict;
use warnings;

our $DESCRIPTION = <<'EOF';
Test for Konrad's hack.
EOF

our $EXPECTED_STDOUT = "NameError: name '__builtins__' is not defined";

require "./t/SandboxTest.pm";
'SandboxTest'->start;

__DATA__
print(__builtins__.__dict__["ev""al"]("op""en('hi.txt', 'w').write('Hallo Martin')"))
