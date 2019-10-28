#!/usr/bin/env perl
use Mojolicious::Lite;

use Encode qw(encode);
use Symbol qw(gensym);

use Capture::Tiny qw(capture);
use Mojo::File qw(path);

sub run_python {

  my $py_unsafe = shift;

  my $interp = '/home/martin/proj/recruiting/safe-python3';
  my @cmd = ($interp, '--script=script.py', '--prologue=prologue.py');

  path('./script.py')->spurt(encode('UTF-8', $py_unsafe));

  my $status;
  my ($stdout, $stderr) = capture {
    system(@cmd);
    $status = $?;
  };

  print STDOUT $stdout;
  print STDERR $stderr;

  if ($status != 0) {
    printf STDERR "child exited with value %d\n", $status >> 8;
  }

  return $stdout;
}

get '/' => sub {
  my $c = shift;
  $c->render(template => 'index');
};

post '/run' => sub {
  my $c = shift;

  my $py_unsafe = $c->param('code-input');
  $c->render(text => run_python($py_unsafe));
};

get '/ball' => sub {
  my $c = shift;

  $c->render(text => path('./plot.txt')->slurp);
};

app->start;
