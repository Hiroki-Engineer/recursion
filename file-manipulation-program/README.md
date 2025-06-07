# How to use file-manipulator

1. Crete reversed file

```sh
just file-manipulator reverse {input path} {output path}
```

2. Copy file

```sh
just file-manipulator copy {input path} {output path}
```

3. Copy content n times

```sh
just file-manipulator duplicate-contents {input path} {n times}
```

4. Replace string

```sh
just file-manipulator replace-string {input path} {old string} {new string}
```
