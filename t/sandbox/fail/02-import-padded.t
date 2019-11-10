use strict;
use warnings;

use SandboxTest {
  DESCRIPTION => <<~'EOF',
      Test for import statements in user-submitted code. (2)
      EOF
  EXPECTED_STDOUT => "NameError: name 'import' is not defined"
};

__DATA__
print("Just a call to print().")

nested = True
if nested:
    import wew
