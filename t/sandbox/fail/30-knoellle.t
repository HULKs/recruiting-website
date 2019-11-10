use SandboxTest {
  DESCRIPTION => <<~'EOF',
      Test for Konrad's hack.
      EOF
  EXPECTED_STDOUT => "NameError: name '__builtins__' is not defined"
};

__DATA__
print(__builtins__.__dict__["ev""al"]("op""en('hi.txt', 'w').write('Hallo Martin')"))
