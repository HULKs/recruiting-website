package SandboxTest;

use strict;
use warnings;

use Encode qw(encode);
use File::Temp qw();
use JSON::PP qw(decode_json);

use IPC::Run qw(run);
use Test::More;

# Perl's DATA filehandle is apparently not open during BEGIN, so let's
# roll our own parser.
sub get_data {

  my $filename = shift;

  open(my $fh, '<:encoding(UTF-8)', $filename)
      or die "Could not open $filename: $!";
  my @lines = <$fh>;
  close($fh)
      or die "Could not close $filename: $!";

  # Throw lines including __DATA__ away
  while (local $_ = shift @lines) {
    last if /^__DATA__$/;
  }

  return join "\n", @lines;
}

sub import {

  # my %test = (shift)->%*;
  my $package = shift;
  my %test = (shift)->%*;

  # Load configuration
  unless (exists $ENV{HULKS_RECRUITING_CONFIG}) {
    die "Missing environment variable: HULKS_RECRUITING_CONFIG";
  }
  my $config = do "$ENV{HULKS_RECRUITING_CONFIG}";

  # Find out who imported this package
  my ($caller_pkg, $caller_file) = caller;

  # Read caller's __DATA__ section into $data
  my $data = get_data($caller_file);

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

  # Remove newline
  chomp $test{DESCRIPTION};

  # Compare sandbox's stdout with expected stdout
  # (*This* is the actual test!)
  is $result->{stdout}, $test{EXPECTED_STDOUT}, $test{DESCRIPTION};

  # Cool, done testing.
  done_testing;
}

1;
