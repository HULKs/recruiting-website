use SandboxTest {
  DESCRIPTION => <<~'EOF',
      Make sure evaluate() is fine, even if eval() is blocked.
      (Test word boundaries.)
      EOF
  EXPECTED_STDOUT => <<~'EOF'
      Hello!
      EOF
};

__DATA__
def evaluate(foo):
    print(foo)

evaluate("Hello!")
