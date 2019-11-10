use strict;
use warnings;

our $DESCRIPTION = <<'EOF';
Test for empty (except for a comment) user-submitted code.
EOF

our $EXPECTED_STDOUT = "";

require "./t/SandboxTest.pm";
'SandboxTest'->start;

__DATA__
# Python comment to prevent Emacs from trimming the data section.
