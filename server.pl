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

app->start;
__DATA__

@@ index.html.ep
% layout 'default';
% title 'Python Exec Test';
<h1>Python Exec Test</h1>
<form>
  <textarea name="code-input" placeholder="code here"></textarea>
  <button type="submit">run</button>
</form>
  <pre class="code-output">output goes here...</pre>

<script>
 var showResults = (evt) => {
   document.querySelector(".code-output").innerText =
     evt.target.responseText;
 };

 window.addEventListener("load", () => {
   var runForm = document.querySelector("form");
   var runButton = document.querySelector("button");

   runButton.addEventListener("click", (evt) => {
     evt.preventDefault();

     var fd = new FormData(runForm);

     var req = new XMLHttpRequest();
     req.addEventListener("load", showResults);
     req.open("POST", "/run");
     req.send(fd);
   });
 });
</script>

@@ layouts/default.html.ep
<!DOCTYPE html>
<html>
  <meta charset="utf-8">
  <head><title><%= title %></title></head>
<style>
.code-stdcombined {
  font-family: monospace;
 }
</style>
  <body><%= content %></body>
</html>
