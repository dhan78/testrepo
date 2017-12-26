set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

Plugin 'VundleVim/Vundle.vim'
Plugin 'scrooloose/syntastic'
Plugin 'scrooloose/nerdtree'
Plugin 'kien/ctrlp.vim'
Plugin 'valloric/youcompleteme'
Plugin 'bling/vim-airline'
Plugin 'tpope/vim-fugitive'
Plugin 'airblade/vim-gitgutter'
Plugin 'rking/ag.vim'


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
nnoremap tj :tabprev<CR>
nnoremap tk :tabnext<CR>
