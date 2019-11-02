#!/usr/bin/env perl
use Mojolicious::Lite;

use Encode qw(encode);
use File::Temp qw();
use Symbol qw(gensym);

use Capture::Tiny qw(capture_merged);
use Mojo::File qw(path);

sub run_python {

  my $py_unsafe = shift;

  my $interp = './safe-python3';

  my $temp_in = File::Temp->new;
  $temp_in->unlink_on_destroy(1);
  binmode($temp_in, ':encoding(UTF-8)');
  my $temp_in_fn = $temp_in->filename;

  my @cmd = ($interp, "--script=$temp_in_fn",
             '--prologue=prologue.py', '--epilogue=epilogue.py');

  path($temp_in_fn)->spurt(encode('UTF-8', $py_unsafe));

  my $status;
  my $output = capture_merged {
    system(@cmd);
    $status = $?;
  };

  print STDOUT $output, "\n";

  if ($status != 0) {
    printf STDERR "child exited with value %d\n", $status >> 8;
  }

  return $output;
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

app->config(hypnotoad => {listen => ['http://*:80']});

app->start;
