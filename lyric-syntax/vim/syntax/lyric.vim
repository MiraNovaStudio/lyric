" Vim syntax file
" Language: Lyric
" Maintainer: MiraNova Studios (Aeonath)
" Version: 0.3.1
" Description: Syntax highlighting for the Lyric programming language

if exists("b:current_syntax")
  finish
endif

" ------------------------------------------------------------
" Keywords
" ------------------------------------------------------------
syntax keyword lyricKeyword def class var god bin int flt str rex None
syntax keyword lyricKeyword try catch finally fade done raise based on
syntax keyword lyricKeyword public private protected return
syntax keyword lyricControl if else while for return
syntax keyword lyricSpecial self
syntax keyword lyricBuiltin print import
syntax keyword lyricConstant true false

" ------------------------------------------------------------
" Operators and Block Terminators
" ------------------------------------------------------------
syntax match lyricOperator "[+\-*/%=<>!]=\?"
syntax match lyricOperator "[&|]{1,2}"
syntax match lyricSymbol "+++"
syntax match lyricSymbol "fade"

" ------------------------------------------------------------
" Numbers
" ------------------------------------------------------------
syntax match lyricNumber "\v\d+(\.\d+)?"

" ------------------------------------------------------------
" Strings
" ------------------------------------------------------------
syntax region lyricString start=/"/ skip=/\\"/ end=/"/
syntax region lyricString start=/'/ skip=/\\'/ end=/'/

" ------------------------------------------------------------
" Comments
" ------------------------------------------------------------
syntax match lyricComment "#.*$"

" ------------------------------------------------------------
" Highlighting Links
" ------------------------------------------------------------
hi def link lyricKeyword Keyword
hi def link lyricControl Conditional
hi def link lyricSpecial Identifier
hi def link lyricBuiltin Function
hi def link lyricConstant Constant
hi def link lyricNumber Number
hi def link lyricString String
hi def link lyricComment Comment
hi def link lyricOperator Operator
hi def link lyricSymbol Statement

let b:current_syntax = "lyric"

