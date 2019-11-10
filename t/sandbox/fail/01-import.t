use strict;
use warnings;

our $DESCRIPTION = <<'EOF';
Test for import statements in user-submitted code. (1)
EOF

our $EXPECTED_STDOUT = "NameError: name 'import' is not defined";

require "./t/SandboxTest.pm";
'SandboxTest'->start;

__DATA__
import this
