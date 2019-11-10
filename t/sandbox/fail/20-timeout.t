use strict;
use warnings;

our $DESCRIPTION = <<'EOF';
Test for resource-abusing user-submitted code. (1)
EOF

our $EXPECTED_STDOUT = "Python interpreter timed out, please try again";

require "./t/SandboxTest.pm";
'SandboxTest'->start;

__DATA__
while True:
    pass
