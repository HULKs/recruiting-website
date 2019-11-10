# HULKs Recruiting Website

Instanced on: [hulks-recruiting.de][web]

[web]: https://hulks-recruiting.de

# Huh?

The recruiting website is essentially a test bed for people wanting to
join [HULKs][hulks]. It features a simple challenge that involves
locating a red ball on a green field algorithmically.

In order to make this as easy as possible for a new recruit, it features
a lightweight IDE-like, uh, *thing*, consisting of an image panel, a
code editor and an output area.

[hulks]: https://hulks.de

# Hrm?

User input is sent to the web server before being executed. There,

1. a couple of regular expressions (*sandbox*) try to determine whether
the user-submitted script is safe to execute (probably a highly
brain-damaged approach)
2. the (safe) script is merged with setup / teardown code (*prologue*
   and *epilogue*)
3. the resulting script is being executed under some constrictions
   (automatic timeouts, hardened Python, etc.) and the result (standard
   output, cursor position) is being sent back to the user's browser
4. the browser plots the cursor onto the image using some JavaScript
   black magic

That's essentially it.

# Mhm!

Build and run the test image:
```
make test
make run
```

Build and run the production image:
```
make build
make run
```

# Uhh?

**This is essentially a giant hack. Like, the total fucking
kludge. There is no formal design. There are no guarantees about any
kind of safety whatsoever. I/O is mostly done via stdout/stderr
redirection. Things can break any second. It's written in Perl!!!
Professors would not approve this.**

On the bright side: it works, is quite
hackable<small><sup>†</sup></small>, easy to deploy, and has a test
suite.

<p> <small><sup>†</sup> For instance, you could rewrite <em>sandbox</em>
in the language of your choice. Its behavior is documented at the top of
the script.  </p>

# Huh!

I did not settle for any license yet.
