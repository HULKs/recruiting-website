package SandboxTest;

use strict;
use warnings;

use Encode qw(encode);
use File::Temp qw();
use JSON::PP qw(decode_json);

use IPC::Run qw(run);
use Test::More;

sub start {

  # Load configuration
  unless (exists $ENV{HULKS_RECRUITING_CONFIG}) {
    die "Missing environment variable: HULKS_RECRUITING_CONFIG";
  }
  my $config = do "$ENV{HULKS_RECRUITING_CONFIG}";

  # Find out who imported this package
  my $caller_pkg = caller;

  # Write a reference to the caller's __DATA__ section
  # into our symbol table
  *PACKAGE_DATA = "${caller_pkg}::DATA";

  # Copy $expectation's contents here
  my $PACKAGE_EXPECTATION = $main::EXPECTED_STDOUT;

  # Read caller's __DATA__ section into $data
  my $data = do {
    local $/ = undef;

    <PACKAGE_DATA>;
  };

  # Cool, done reading.
  close(PACKAGE_DATA) or die "Could not close package data: $!";

  # Is there any data?
  ok(defined $data and $data ne '');

  # Write data to tempfile
  my $temp = File::Temp->new;
  $temp->unlink_on_destroy(1);
  print $temp encode('UTF-8', $data);
  my $temp_fn = $temp->filename;

  # Run sandbox
  my $sandbox_bin = $config->{sandbox}->{binary};
  my $cmd = [ $sandbox_bin, "--script=$temp_fn",
              '--prologue=prologue.py', '--epilogue=epilogue.py' ];
  my ($in, $out, $err);
  run $cmd, \$in, \$out, \$err;

  diag "(stderr) $err" if $err;

  my $result = decode_json($out);

  # Compare sandbox's stdout with expected stdout
  # (*This* is the actual test!)
  is $result->{stdout}, $PACKAGE_EXPECTATION,
      'stdout matches expectation';

  # Cool, done testing.
  done_testing;
}

1;
