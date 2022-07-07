Windows Tools
================================================================================

## icacls

```
C:\>icacls scsiaccess.exe
  // Check or change file permissions.
  // Look for `Everyone` rights.
  // where
  //   F – Full, M – Modify, RX – Read & execute, R – Read, 
  //   W – Write, D – Del, N – None
```

Native to Windows. On older versions, use `cacls`.

## dir - The comprehensive way

```
C:\>dir [X]       // List contents of current dir or dir X
C:\>dir [X] /ah   // List hidden contents of current dir or dir X
C:\>dir [X] /r    // List ADS (alternate data stream) contents of current dir or dir X

C:\>dir \ /s [/r|/ah] | find “XXX” | more
                  // Find a file [ADS|hidden], starting at c:\, with detailed output.
```

Never use just `dir`. Always do `dir`, `dir /r`, and `dir /ah` to see ADS and hidden!




