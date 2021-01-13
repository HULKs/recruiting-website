# Hello `World!`

First paragraph: *italic*, **bold**, ***italic and bold***

```dockerfile
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    iproute2 inotify-tools \
    && rm -Rf /var/lib/apt/lists/*

CMD tail -f /dev/null
```

<x-button image="ubuntu:latest" command="date" label="Output current date" />

<x-image-viewer file="/data/output.png" mime="image/png" />

<x-terminal image="ubuntu:latest" command="/bin/bash" working-directory="/data" />

<x-text-editor file="/data/output.txt" />

<x-text-viewer file="/data/output.txt" />

## C++ code

```cpp
class Foo {
public:
    explicit Foo(const std::string &temp);
};
```

## Image

![The Office](source.gif)
