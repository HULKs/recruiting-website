# Hello `World!`

```dockerfile
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    iproute2 inotify-tools \
    && rm -Rf /var/lib/apt/lists/*

CMD tail -f /dev/null
```

## Test

Foo

<x-text file="/test.txt" />

<x-image file="/image.png" />

<x-button command="echo Hello World!">Print Hello World</x-button>

<x-editor type="text" file="/test.txt" />

<x-terminal working-directory="/" />

## C++ code

```cpp
class Foo {
public:
    explicit Foo(const std::string &temp);
};
```

## Image

![The Office](source.gif)
