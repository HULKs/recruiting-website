use SandboxTest {
  DESCRIPTION => <<~'EOF',
    Test for user-submitted code generating a huge response.
    EOF
  EXPECTED_STDOUT => "Response too large, please emit fewer characters"
};

__DATA__
print("abcd"*2000000)