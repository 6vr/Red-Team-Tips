Markdown Cheatsheet
================================================================================

<br>

<details>
  <summary><b><u>
  Text Styles
  </u></b></summary>

Heading 1
================================================================================

```
Heading 1     -OR-    # Heading 1
=========
```

## Heading 2

```
Heading 2     -OR-    ## Heading 2
---------
```

### Heading 3

```
### Heading 3
```

#### Heading 4

```
#### Heading 4
```

##### Heading 5

```
##### Heading 5     // Really, why use this?
```

###### Heading 6

```
###### Heading 6    // This is ridiculously small.
```

Common text

```
Common text
```

*Emphasized text*

```
*Emphasized text*     -OR-    _Emphasized text_
```

**More emphasized text**

```
**More emphasized text**     -OR-    __More emphasized text__
```

***Most emphasized text***

```
***Most emphasized text***     -OR-    ___Most emphasized text___
```

~~Strikethrough text~~

```
~~Strikethrough tet~~
```

<br>

</details>

<details>
  <summary><b><u>
  Links & Images
  </u></b></summary>

[Text that is a link](http://www.google.com/) 

```
[Text that is a link](http://www.google.com/)
```

<http://example.com/>

```
<http://example.com/>
```

*Image with alt:*

![picture alt](http://www.brightlightpictures.com/assets/images/portfolio/thethaw_header.jpg "Title is optional")

```
![picture alt](http://www.brightlightpictures.com/assets/images/portfolio/thethaw_header.jpg "Title is optional")
```

*Note that you'll often be unable to embed pictures directly into documents written in markdown unless converting to PDF or some other format. You can play with embedding images via MIME and some HTML help, but it's must easier to create an [Imgur](https://imgur.com/) account and link to graphics that you've uploaded privately there.*

<br>

</details>

<details>
  <summary><b><u>
  Tables
  </u></b></summary>


| First Header  | Second Header
| ------------- | -------------
| Content Cell  | Content Cell
| Content Cell  | Content Cell

```
| First Header  | Second Header
| ------------- | -------------
| Content Cell  | Content Cell
| Content Cell  | Content Cell
```

|C1|C2|C3|C4|C5|C6
|---|---|---|---|---|---
|R1 | R1C2 | R1C3 | R1C4 | R1C5 | MegaSizeEntryR1C6
|ThisRowRocks||||Yessss|

```
|C1|C2|C3|C4|C5|C6
|---|---|---|---|---|---
|R1 | R1C2 | R1C3 | R1C4 | R1C5 | MegaSizeEntryR1C6
|ThisRowRocks||||Yessss|
```

<br>

</details>

<details>
  <summary><b><u>
  Lists, Quotes, & Lines
  </u></b></summary>

* Bullet list item 1
    * Nested bullet
        * Sub-nested bullet
        	* Sub-sub-nested bullet etc
* Bullet list item 2

```
* Bullet list item 1
    * Nested bullet
        * Sub-nested bullet
        	* Sub-sub-nested bullet etc
* Bullet list item 2
```

1. A numbered list
    1. A nested numbered list
    2. Which is numbered
    	* And mixed with bullets
    		1. And vice versa
2. Which is numbered

```
1. A numbered list
    1. A nested numbered list
    2. Which is numbered
    	* And mixed with bullets
    		1. And vice versa
2. Which is numbered
```

- [ ] An incomplete task
- [x] A completed task

```
- [ ] An incomplete task
- [x] A completed task
```

> Blockquote
>> Nested blockquote

```
> Blockquote
>> Nested blockquote
```

(Horizontal line, seen below:)
- - - -

```
- - - -
```

<br>

</details>

<details>
  <summary><b><u>
  Foldable Text, Code Blocks, Keyboard Keys, & Emojis
  </u></b></summary>

Foldable text:

<details>
  <summary>Title 1</summary>
  
Contents 1 here  
Contents 1 here  
Contents 1 here  
Contents 1 here  

</details>

<details>
  <summary>Title 2</summary>

Contents 2 here  
Contents 2 here  
Contents 2 here  
Contents 2 here  

</details>

```
<details>
  <summary>Title 1</summary>
  
Contents 1 here  
Contents 1 here  
Contents 1 here  
Contents 1 here  

</details>

<details>
  <summary>Title 2</summary>

Contents 2 here  
Contents 2 here  
Contents 2 here  
Contents 2 here  

</details>
```

Inline code snippet: `code()`

```
`code()`
```

Code blocks. This will get **weird** looking, since I've been using code blocks all this time to show markup. So I'll title these. Take note of the extra line between text and the opening of the code block.

##### What it looks like to the reader:

```javascript
    var specificLanguage_code = 
    {
        "data": {
            "lookedUpPlatform": 1,
            "query": "Kasabian+Test+Transmission",
            "lookedUpItem": {
                "name": "Test Transmission",
                "artist": "Kasabian",
                "album": "Kasabian",
                "picture": null,
                "link": "http://open.spotify.com/track/5jhJur5n4fasblLSCOcrTp"
            }
        }
    }
```

##### How you get it:

```
```javascript  <-- Optional to specify language. Highlights syntax.
    var specificLanguage_code = 
    {
        "data": {
            "lookedUpPlatform": 1,
            "query": "Kasabian+Test+Transmission",
            "lookedUpItem": {
                "name": "Test Transmission",
                "artist": "Kasabian",
                "album": "Kasabian",
                "picture": null,
                "link": "http://open.spotify.com/track/5jhJur5n4fasblLSCOcrTp"
            }
        }
    }
``` <-- This closes the code block
```

Hotkeys are useful to show a reader what to type.

<kbd>ctrl</kbd>+<kbd>A</kbd>, <kbd>ctrl</kbd>+<kbd>K</kbd>

```
<kbd>ctrl</kbd>+<kbd>A</kbd>, <kbd>ctrl</kbd>+<kbd>K</kbd>
```

Common hotkeys list. I usually use words, maybe because I'm lazy.

| Term | Word key | Symbol key
| --- | --- | --- 
| Option | <kbd>option</kbd> | <kbd>⌥</kbd> |
| Control | <kbd>ctrl</kbd> | <kbd>⌃</kbd> |
| Command | <kbd>cmd</kbd> | <kbd>⌘</kbd> |
| Shift | <kbd>shift</kbd> | <kbd>⇧</kbd> |
| Caps Lock | <kbd>caps</kbd> | <kbd>⇪</kbd> |
| Tab | <kbd>tab</kbd> | <kbd>⇥</kbd> |
| Esc | <kbd>esc</kbd> | <kbd>⎋</kbd> |
| Power | <kbd>power</kbd> | <kbd>⌽</kbd> |
| Return | <kbd>enter</kbd> | <kbd>↩</kbd> |
| Delete | <kbd>backspace</kbd> or <kbd>del</kbd> | <kbd>⌫</kbd> |
| Up | <kbd>up</kbd> | <kbd>↑</kbd> |
| Down | <kbd>down</kbd> | <kbd>↓</kbd> |
| Left | <kbd>left</kbd> | <kbd>←</kbd> |
| Right | <kbd>right</kbd> | <kbd>→</kbd> |

Lastly, emojis. Sometimes they render, and sometimes not.

:exclamation: Use emoji icons to enhance text. :+1:  Look up emoji codes at <http://emoji-cheat-sheet.com/>.

```
Code appears between colons :EMOJICODE:
```

<br>

</details>
