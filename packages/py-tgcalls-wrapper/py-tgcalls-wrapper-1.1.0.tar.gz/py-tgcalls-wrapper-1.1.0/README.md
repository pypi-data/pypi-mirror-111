# PyTgCalls wrapper

#### Making it easier for you to use [pytgcalls](https://github.com/pytgcalls/pytgcalls).

---

## Features

- No need to care about audio convertion.
- Play directly from URLs, YouTube and local files.
- Get warned if can't be paused or resumed.
- Async + Sync support.

## Requirements

1. FFmpeg
2. YouTube DL

## Full examples

See the [`examples`](./examples) folder.

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

### Streaming

#### YouTube videos

```py
wrapper.stream(-123456789, "https://youtube.com/watch?v=9KAQaKydqA0")
```

### Links

```py
wrapper.stream(-123456789, "http://somewebsite.com/path/to/somefile.webm")
```

#### Local files

```py
wrapper.stream(-123456789, "/path/to/file.mp3")
```

### Controlling

#### Pausing

```py
wrapper.pause(-123456789)
```

#### Resuming

```py
wrapper.resume(-123456789)
```

More to come soon!
