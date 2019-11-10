use SandboxTest {
  DESCRIPTION => <<~'EOF',
    Test for empty (except for a comment) user-submitted code.
    EOF
  EXPECTED_STDOUT => ""
};

__DATA__
# Python comment to prevent Emacs from trimming the data section.
