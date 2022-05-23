" Vim syntax file 
" Language Qs Programming Language
" Maintainer: Nathaniel Ramos
" Latest Revision: 22 May 2022


if exists("b:current_syntax")
  finish
endif

syn keyword qsTodo contained TODO FIXME XXX NOTE
syn match qsComment "!.*$" contains=QsTodo

syn match qsNumber '\d\+' contained display
syn match qsNumber '[-+]\d\+' contained display

syn match qsNumber '\d\+\.\d*' contained display
syn match qsNumber '[-+]\d\+\.\d*' contained display

syn match qsNumber '[-+]\=\d[[:digit:]]*[eE][\-+]\=\d\+' contained display
syn match qsNumber '\d[[:digit:]]*[eE]][\-+]\=\d\+' contained display

syn region qsString start='"' end='"' contained
syn region qsDesc start='"' end='"'

syn match qsHip '\d\{1,6}' nextgroup=qsString
syn match qsFunction    "\h\w*" display contained

syn match qsDecorator     "@" display contained
syn match qsDecoratorName "@\s*\h\%(\w\|\.\)*" display contains=qsDecorator



syn region QsDescBlock start="%" end="%" fold transparent contains=QsNumber, qsFunction, qsConditional, qsRepeat, qsStatement, qsBuiltin, qsOperator, qsComment 


" Keywords
syn keyword qsFunction DEFINE SERVE INPUT 
syn keyword qsConditional IF ELSE 
syn keyword qsRepeat  WHILE
syn keyword qsStatement OUTPUT INIT RUN FORMAT 
syn keyword qsBuiltin BREAK EXIT 
syn keyword qsOperator OR AND 


let b:current_syntax = "qs"

hi def link qsTodo           Todo
hi def link qsComment        Comment 
hi def link qsStatement      Statement
hi def link qsFunction       Function
hi def link qsDecoratorName  Function
hi def link qsConditional    Conditional
hi def link qsString         String
hi def link qsDesc           Define 
hi def link qsNumber         Constant
hi def link qsRepeat         Repeat
hi def link qsOperator       Operator
