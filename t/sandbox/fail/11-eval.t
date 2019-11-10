use strict;
use warnings;

our $DESCRIPTION = <<'EOF';
Test for banned functions (like eval) in user-submitted code. (2)
EOF

our $EXPECTED_STDOUT = "NameError: name 'eval' is not defined";

require "./t/SandboxTest.pm";
'SandboxTest'->start;

__DATA__
  eval ("hello")
