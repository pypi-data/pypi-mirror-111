# PyTgCalls wrapper

#### Making it easier for you to use [pytgcalls](https://github.com/pytgcalls/pytgcalls).

---

## Requirements

1. FFmpeg
2. YouTube DL

## Installation

```bash
pip install py-tgcalls-wrapper
```

## Usage

### Importing

```py
from pytgcalls_wrapper import Wrapper
```

### Initializing

```py
wrapper = Wrapper(pytgcalls)
```

### Playing

Advantages:

- No need to care about audio convertion.
- Play directly from a local file, YouTube and URLs

#### YouTube videos

```py
await wrapper.play(-123456789, "http://youtube.com/watch?v=")
```

#### Local files

```py
await wrapper.play(-123456789, "/path/to/file.mp3")
```

### Controlling

Advantage: You get warned if the request can't be made.

#### Pausing

```py
await wrapper.pause(-123456789)
```

#### Resuming

```py
await wrapper.resume(-123456789)
```

More to come soon!
