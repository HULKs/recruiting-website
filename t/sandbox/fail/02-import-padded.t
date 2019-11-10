use strict;
use warnings;

our $DESCRIPTION = <<'EOF';
Test for import statements in user-submitted code. (2)
EOF

our $EXPECTED_STDOUT = "NameError: name 'import' is not defined";

require "./t/SandboxTest.pm";
'SandboxTest'->start;

__DATA__
print("Just a call to print().")

nested = True
if nested:
    import wew
