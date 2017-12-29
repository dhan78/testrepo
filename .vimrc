set nocompatible              " be iMproved, required
filetype off                  " required
syntax on

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

Plugin 'VundleVim/Vundle.vim'
Plugin 'scrooloose/syntastic'
Plugin 'scrooloose/nerdtree'
Plugin 'ctrlpvim/ctrlp.vim'
Plugin 'valloric/youcompleteme'
Plugin 'bling/vim-airline'
Plugin 'tpope/vim-fugitive'
Plugin 'airblade/vim-gitgutter'
Plugin 'rking/ag.vim'
Plugin 'flazz/vim-colorschemes'


call vundle#end()            " required
filetype plugin indent on    " required

set number
set hidden
set relativenumber
set tabstop=4
set smartindent
set shiftwidth=4
set expandtab
set mouse=a
let mapleader=","
:map <F4> :NERDTree<CR>
:map <silent> <F4> :NERDTreeToggle<CR>
nnoremap <leader>rv :source $MYVIMRC<CR>
nnoremap ) :bn<CR>
nnoremap ( :bp<CR>
nnoremap tj :tabprev<CR>
nnoremap tk :tabnext<CR>
" syntastic params
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
set ic
colorscheme CandyPaper

" Highlight all instances of word under cursor, when idle.
" Useful when studying strange source code.
" Type z/ to toggle highlighting on/off.
nnoremap z/ :if AutoHighlightToggle()<Bar>set hls<Bar>endif<CR>
function! AutoHighlightToggle()
    let @/ = ''
    if exists('#auto_highlight')
        au! auto_highlight
        augroup! auto_highlight
        setl updatetime=100
        echo 'Highlight current word: off'
        return 0
    else
        augroup auto_highlight
            au!
            au CursorHold * let @/ = '\V\<'.escape(expand('<cword>'), '\').'\>'
        augroup end
        setl updatetime=100
        echo 'Highlight current word: ON'
        return 1
    endif
endfunction

