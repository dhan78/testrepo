set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'scrooloose/syntastic'
Plugin 'scrooloose/nerdtree'
Plugin 'kien/ctrlp.vim'
Plugin 'valloric/youcompleteme'
Plugin 'bling/vim-airline'
Plugin 'tpope/vim-fugitive'
Plugin 'airblade/vim-gitgutter'
Plugin 'rking/ag.vim'


" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo

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
:map <F5> :NERDTree<CR>
nnoremap <leader>rv :source $MYVIMRC<CR>
nnoremap ) :bn<CR>
nnoremap ( :bp<CR>
nnoremap th :tabfirst<CR>
nnoremap tl :tabprev<CR>
