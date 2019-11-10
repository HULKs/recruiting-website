use strict;
use warnings;

use SandboxTest {
  DESCRIPTION => <<~'EOF',
      Test for import statements in user-submitted code. (1)
      EOF
  EXPECTED_STDOUT => "NameError: name 'import' is not defined"
};

__DATA__
import this
