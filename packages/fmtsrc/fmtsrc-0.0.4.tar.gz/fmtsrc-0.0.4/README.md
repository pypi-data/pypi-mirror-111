# fmtsrc

This program outputs the input string as a text file by specifying the format such as normalization of Unicode strings, specification of newline characters, etc.

# argument
## os
 Auto select hint of unicode format (Mac:NFD, Windows or Linux: NFC), line separator (Windows:CRLF, Mac or Linux: LF).
 Choose 'Mac' or 'Windows' or 'Linux' (default: environment OS)
 example:
  fmtsrc file='xxx.txt' os='Windows'

## encoding
 The text encoding of the input source.
 example:
  fmtsrc file='xxx.txt' encoding='utf-8'

## unicodeform
 The Unicode combining character.
 MacOSX use NFD, other NFC.
 example:
  fmtsrc url='https://xxx.com/yyy.txt' unicodeform='NFC'

## linesep
 Line separator. This option can replace all line separators as any character.
 MacOS9 or later: LF
 Other MacOS: CR
 Linux: LF
 Windows CR+LF
 example:
  fmtsrc url='https://xxx.com/yyy.txt' linesep='\r\n'
  fmtsrc url='https://xxx.com/yyy.txt' linesep='</br>'

## URL
 URL input source.  Error occurs when file source is used.
 example:
  fmtsrc url='https://xxx.com/yyy.txt'

## file
 File input source. Error occurs when url source is used.
 example:
  fmtsrc file='xxx.txt'

## export
 Export data as a file.
 example:
  fmtsrc file='xxx.txt' export='zzz.txt'
  fmtsrc url='https://xxx.com/yyy.txt' export='zzz.txt'
## e_encodings
 The text encoding of the output file. If not specified, input encoding is applied.
 example:
  fmtsrc url='https://xxx.com/yyy.txt' export='zzz.txt' e_encodings='utf-8'
