use SandboxTest {
  DESCRIPTION => <<~'EOF',
    Test for resource-abusing user-submitted code. (1)
    EOF
  EXPECTED_STDOUT => "Python interpreter timed out, please try again"
};

__DATA__
while True:
    pass
